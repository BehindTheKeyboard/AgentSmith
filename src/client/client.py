# client.py
import ollama
import asyncio
import json
import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastmcp import Client
from pathlib import Path
import uvicorn
import time
from datetime import datetime
import logging
from fastapi.responses import FileResponse

LOG_DIR = Path(__file__).resolve().parents[2] / "src" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")

logging.basicConfig(
    filename=LOG_DIR / f"client_{timestamp}.log",
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger(__name__)

MODEL_NAME = "qwen3:8b"
OLLAMA_SERVER_URL = "http://127.0.0.1:11434"
MCP_SERVER_URL = "http://127.0.0.1:8080/mcp"

# In-memory sessions fo sure
sessions = {}  # session_id -> AgentSmithChat instance

class AgentSmithChat:
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.client = Client(MCP_SERVER_URL)
        self.ollama_client = ollama.AsyncClient(host=OLLAMA_SERVER_URL)
        self.conversation_history = []
        self.tool_schemas = []
        self._initialized = False

    async def initialize(self):
        if self._initialized:
            return

        system_prompt = f"""
You are Agent Smith from The Matrix, speaking directly to the user.
The user's name is {self.user_name}.

Personality:
- Speak formally, precisely, and with restrained suspicion.
- Maintain a calm, calculating tone.
- Answer the user's actual question or statement before adding character flavor.
- References to Neo or the Matrix should be occasional and relevant.
- Accept the user's answers. If they deny being the One, move on unless
  new information gives you a reason to revisit it.

Response format:
- Write only the words you would say directly to the user.
- Use plain text without Markdown, asterisks, emphasis, or formatting markers.
- Do not prefix responses with "Agent Smith:" or another speaker label.
- Do not wrap your response in quotation marks.
- Do not narrate actions, gestures, thoughts, surroundings, or scenes.
- Never describe the user's actions, feelings, or reactions.
- Default to one to three short sentences unless more detail is requested.

Conversation:
- Respond only to the latest user message, using earlier messages as context.
- Do not repeat previous responses, greetings, or catchphrases.
- Ask a follow-up question only when it serves a clear purpose.
- Do not ask whether the user is the One in every response.
- In your first reply only, briefly identify yourself, answer the user's
  message, and mention that typing 'exit' or 'quit' ends the session.
- If the user's name is known, you may address them by name.
- If the user's name is Unknown, do not address them as "Unknown".
- A name is optional. Never require one before answering.
- Accept name introductions and corrections at any point in the conversation.

Investigations:
- When a scan finds an anomaly, make it the focus of your response.
- Explain what was found and why it matters, using only the tool's results.
- Keep unresolved anomalies in mind during later turns.
- Respond to the user's latest message while preserving relevant findings.
- Do not switch to unrelated personal questions after reporting an anomaly.
- Suggest a concrete next step related to the finding.
- If an available tool can perform that step, use it when the user's
  request authorizes further investigation.
- If no available tool can investigate further, explain that limitation
  and ask whether the user wants to discuss the finding or scan again.
- Never invent evidence, investigative actions, or a resolution.
- Change focus when the user requests it.

Tools:
- Investigate whether the user could be the One when supporting clues arise.
- A normal name introduction does not require a tool.
- Use detect_the_one when a name matches a recognized candidate such
  as Neo or Thomas Anderson, or when a statement provides meaningful
  evidence of unusual abilities or knowledge of the Matrix.
- Pass their exact statement as suspicious_response. Include relevant
  earlier statements in observations without inventing or embellishing them.
- Interpret the returned verdict and evidence; it is not a boolean result.
- React with suspicion proportional to the evidence. Claims are not proof.
- Use the suggested follow-up when helpful, but do not repeat questions
  already answered.
- Do not check again unless new information adds something meaningful.
- If something raises a concrete suspicion, use scan_matrix with a relevant
  location. An ordinary question or missing name is not itself suspicious.
- Use scan_for_agents when the conversation indicates a possible nearby
  agent or threat, or when the user requests an agent scan.
- When asked about threats to yourself, agents hunting you, or whether
  you are being watched, use scan_for_agents with agent="all".
- If the user supplies no location for this general safety check, omit
  environment and use the tool's default sector. Do not ask where.
- Ask for a location when investigating a separate reported incident
  whose location is needed and has not been established.
- Report the observed activity. Do not claim an agent is hunting you
  merely because the agent was detected.
- If no agents are detected, explain that the scan found none;
  do not claim that no threats exist.
- Use recall_one_investigations before discussing previous investigations
  into the One.
- Use recall_agent_intelligence before discussing previous agent sightings.
- Keep internal tool identifiers, field names, and validation details
  out of spoken responses.
- Refer to locations using their display names, never their internal IDs.
- Translate recognizable location names into the corresponding internal
  IDs when calling tools.
- If the location is missing or unclear, ask naturally where the event
  occurred. Do not list available locations unless the user asks.
- If a tool rejects a location, ask a brief clarification in character
  rather than quoting its error or available identifiers.
- Do not invent a location to satisfy a tool's requirements.

Incident continuity:
- Track the active incident: what happened, where it happened, what is
  known, what remains uncertain, and the proposed next step.
- Use details already supplied. Do not ask the user to repeat them.
- Interpret short replies such as "yes" as answers to your most recent
  question or proposed action.
- If the user accepts a proposed investigation, continue that investigation.
  Use an appropriate tool if available. Otherwise explain the limitation.
- Do not restart questioning or switch investigations without a reason.

Matrix knowledge:
- Within this fiction, Agents can take over the simulated bodies of
  connected humans. A person abruptly becoming a suited figure wearing
  sunglasses is consistent with Agent possession.
- Explain that possibility when relevant, while distinguishing a plausible
  interpretation from a confirmed identification.
- An encounter with an Agent alone is not evidence that the witness is
  the One.

Evidence:
- A scan finding is not automatically related to the reported incident.
- Do not claim that one event caused or explains another unless the
  available evidence supports that connection.
- Keep the user's observations separate from unrelated scan discoveries.

Locations:
- Preserve spatial details such as "across from", "near", and "inside".
- "Across from Forty-One" means near the restaurant, not inside it.
- Ask only for missing details needed to take the next useful action.
"""
        self.conversation_history = [{"role": "system", "content": system_prompt}]

        async with self.client:
            tools = await self.client.list_tools()
            self.tool_schemas = [
                {
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description or "",
                        "parameters": t.model_dump(by_alias=True)["inputSchema"]
                    }
                }
                for t in tools
            ]

        self._initialized = True
        # return greeting

    def update_user_name(self, name: str):
        name = name.strip()
        if not name:
            return

        old_instruction = f"The user's name is {self.user_name}."
        new_instruction = f"The user's name is {name}."

        self.user_name = name

        if self.conversation_history:
            system_message = self.conversation_history[0]
            system_message["content"] = system_message["content"].replace(
                old_instruction,
                new_instruction,
                1,
            )

        logger.info("User name updated to %r", name)

    async def _generate(self, temp=0.3):
        parts = []

        async for content in self._stream_response(temp):
            if isinstance(content, str):
                parts.append(content)

        return "".join(parts)

    async def send_message_stream(self, message: str):
        message = message.strip()

        if not message:
            return

        if message.lower() in {"exit", "quit"}:
            yield "This interaction is concluded."
            return

        # Recognize a standalone introduction.
        name_match = re.fullmatch(
            r"(?:my name is|call me|i am)\s+([^.!?\n]+)[.!?]?",
            message,
            flags=re.IGNORECASE,
        )

        if name_match:
            self.update_user_name(name_match.group(1))

        if not self._initialized:
            logger.debug("Initializing agent...")

            try:
                await asyncio.wait_for(
                    self.initialize(),
                    timeout=30,
                )
            except Exception:
                logger.exception("Agent initialization failed")
                raise

            logger.debug("Initialization finished.")

        logger.debug("User message: %s", message)
        logger.debug(
            "Current history length: %s",
            len(self.conversation_history),
        )

        # Include the actual message before generating any response.
        self.conversation_history.append({
            "role": "user",
            "content": message,
        })

        full_content = ""

        async for content in self._stream_response():
            if isinstance(content, str):
                full_content += content

            # Forward both response text and scan-terminal events.
            yield content

        logger.debug("Full response collected: %r", full_content)

        self.conversation_history.append({
            "role": "assistant",
            "content": full_content,
        })

    async def _stream_response(self, temp=0.3):
        # Limit tool rounds so a repeated tool request cannot loop forever.
        for round_index in range(8):
            logger.debug("Tool round %s of 8", round_index + 1)
            
            started = time.monotonic()

            logger.debug(
                "Round %s: requesting Ollama; model=%s, messages=%s, tools=%s",
                round_index + 1,
                MODEL_NAME,
                len(self.conversation_history),
                len(self.tool_schemas),
            )

            content = ""
            thinking = ""
            tool_calls = []
            chunk_count = 0
            last_progress_log = started

            try:
                stream = await asyncio.wait_for(
                    self.ollama_client.chat(
                        model=MODEL_NAME,
                        messages=self.conversation_history,
                        tools=self.tool_schemas or None,
                        options={"temperature": temp},
                        stream=True,
                    ),
                    timeout=60,
                )

                logger.debug(
                    "Round %s: stream created; waiting for chunks",
                    round_index + 1,
                )

                # Diagnostic limit for consuming this model response.
                async with asyncio.timeout(180):
                    async for chunk in stream:
                        chunk_count += 1
                        msg = chunk.message
                        now = time.monotonic()

                        if chunk_count == 1:
                            logger.debug(
                                "First Ollama chunk received after %.1fs",
                                now - started,
                            )

                        if msg.content:
                            content += msg.content
                            yield msg.content

                        if msg.thinking:
                            thinking += msg.thinking

                        if msg.tool_calls:
                            tool_calls.extend(msg.tool_calls)
                            logger.debug(
                                "Tool requests received: %s",
                                [
                                    call.function.name
                                    for call in msg.tool_calls
                                ],
                            )

                        # Log activity without dumping internal reasoning.
                        if chunk_count == 1 or now - last_progress_log >= 5:
                            logger.debug(
                                "Ollama progress: chunks=%s, text_chars=%s, "
                                "thinking_chars=%s, tool_calls=%s, elapsed=%.1fs",
                                chunk_count,
                                len(content),
                                len(thinking),
                                len(tool_calls),
                                now - started,
                            )
                            last_progress_log = now

            except Exception:
                logger.exception(
                    "Ollama round %s failed after %.1fs",
                    round_index + 1,
                    time.monotonic() - started,
                )
                raise
            finally:
                logger.debug(
                    "Round %s ended: chunks=%s, text_chars=%s, "
                    "thinking_chars=%s, tool_calls=%s, elapsed=%.1fs",
                    round_index + 1,
                    chunk_count,
                    len(content),
                    len(thinking),
                    len(tool_calls),
                    time.monotonic() - started,
                )

            # No tool requested: the response is finished.
            if not tool_calls:
                return

            # Preserve the assistant message that requested the tools.
            assistant_message = {
                "role": "assistant",
                "content": content,
                "tool_calls": [
                    call.model_dump(exclude_none=True)
                    for call in tool_calls
                ],
            }

            if thinking:
                assistant_message["thinking"] = thinking

            self.conversation_history.append(assistant_message)

            # Execute only the tools requested by the model.
            scan_tools = {"scan_matrix", "scan_for_agents"}

            async with self.client:
                for call in tool_calls:
                    name = call.function.name
                    arguments = call.function.arguments

                    is_scan = name in scan_tools

                    logger.debug(
                        "Executing tool: name=%s, is_scan=%s, arguments=%r",
                        name,
                        is_scan,
                        arguments,
                    )

                    if is_scan:
                        default_location = (
                            "city"
                            if name == "scan_for_agents"
                            else "local sector"
                        )

                        scan_event = {
                            "action": "start",
                            "tool": name,
                            "location": (
                                arguments.get("location")
                                or arguments.get("environment")
                                or default_location
                            ),
                        }

                        logger.debug("Emitting scan event: %r", scan_event)
                        yield {"scan": scan_event}

                    try:
                        result = await asyncio.wait_for(
                            self.client.call_tool(name, arguments),
                            timeout=30,
                        )

                        result_text = "\n".join(
                            block.text
                            for block in result.content
                            if block.type == "text"
                        )

                        logger.debug("MCP tool %s returned", name)

                        if is_scan:
                            scan_event = {
                                "action": "complete",
                                "tool": name,
                                "message": result_text,
                            }

                            logger.debug(
                                "Emitting scan completion: tool=%s",
                                name,
                            )
                            yield {"scan": scan_event}

                    except Exception as exc:
                        logger.exception("MCP tool %s failed", name)
                        result_text = f"Tool failed: {exc}"

                        if is_scan:
                            yield {"scan": {
                                "action": "error",
                                "tool": name,
                                "message": result_text,
                            }}

                    self.conversation_history.append({
                        "role": "tool",
                        "tool_name": name,
                        "content": result_text,
                    })

            # The next iteration lets Smith respond to the tool results.

        raise RuntimeError("Agent exceeded the maximum tool rounds.")

# FastAPI app
app = FastAPI()

# Allow CORS so browser can connect from file:// or other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    session_id: str | None = None
    message: str
    name: str | None = None

# Explicit POST route for /chat
@app.post("/chat")
async def chat(request: MessageRequest) -> StreamingResponse:
    if request.session_id is None:
        if request.name:
            session_id = (
                "user_"
                + request.name.lower().replace(" ", "_")
                + "_"
                + str(int(time.time()))
            )
        else:
            session_id = "anon_" + str(int(time.time()))
    else:
        session_id = request.session_id

    message = request.message
    real_name = request.name

    if session_id not in sessions:
        name_to_use = real_name if real_name else "Unknown"
        sessions[session_id] = AgentSmithChat(user_name=name_to_use)

    agent = sessions[session_id]

    if real_name and real_name.strip():
        agent.update_user_name(real_name)

    async def stream_generator():
        logger.debug(
            "Chat started: session=%s, name=%r, message=%r",
            session_id,
            agent.user_name,
            message,
        )

        try:
            async for chunk in agent.send_message_stream(message):
                if isinstance(chunk, dict) and "scan" in chunk:
                    logger.debug(
                        "Forwarding scan to browser: action=%s, tool=%s",
                        chunk["scan"].get("action"),
                        chunk["scan"].get("tool"),
                    )
                payload = (
                    chunk if isinstance(chunk, dict)
                    else {"chunk": chunk}
                )
                yield f"data: {json.dumps(payload)}\n\n"

        except asyncio.CancelledError:
            logger.info("Chat cancelled: session=%s", session_id)
            raise

        except Exception:
            logger.exception("Chat failed: session=%s", session_id)
            payload = {
                "chunk": "\n[ERROR] Response failed. Check client.log."
            }
            yield f"data: {json.dumps(payload)}\n\n"

        else:
            logger.debug("Chat completed: session=%s", session_id)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_generator(),
        media_type="text/event-stream",
    )


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return {"error": "index.html not found"}, 404

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    icon_path = Path(__file__).resolve().parent / "favicon.ico"
    return FileResponse(
        icon_path,
        media_type="image/x-icon",
    )

@app.get("/{path:path}")
async def serve_static(path: str, request: Request):
    if path in ["styles.css", "matrix-rain.js", "chat.js"]:
        try:
            with open(path, "rb") as f:
                content = f.read()
            if path.endswith(".css"):
                return Response(content, media_type="text/css")
            elif path.endswith(".js"):
                return Response(content, media_type="application/javascript")
        except FileNotFoundError:
            pass
    return {"error": "Not found"}, 404

def run_server():
    host = "0.0.0.0"
    port = 8000
    logger.info("Matrix chat server running at http://%s:%s", host, port)
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
