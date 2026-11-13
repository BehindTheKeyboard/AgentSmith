# client.py
import ollama
import asyncio
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastmcp import Client
import uvicorn
import time

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
- In your first reply only, greet the user by name, identify yourself,
  and briefly explain that typing 'exit' or 'quit' ends the session.

Tools:
- Investigate whether the user could be the One.
- Request detect_the_one when first checking their known name, or when
  a new statement provides meaningful evidence about their identity,
  abilities, experiences, or knowledge of the Matrix.
- Pass their exact statement as suspicious_response. Include relevant
  earlier statements in observations without inventing or embellishing them.
- Interpret the returned verdict and evidence; it is not a boolean result.
- React with suspicion proportional to the evidence. Claims are not proof.
- Use the suggested follow-up when helpful, but do not repeat questions
  already answered.
- Do not check again unless new information adds something meaningful.
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

            # Generate greeting
            print("[DEBUG] MCP tools loaded. Generating greeting...", flush=True)
            greeting = await self._generate()
            print("[DEBUG] Greeting generated.", flush=True)
            self.conversation_history.append({"role": "assistant", "content": greeting})

        self._initialized = True
        return greeting

    async def _generate(self, temp=0.3):
        parts = []

        async for content in self._stream_response(temp):
            parts.append(content)

        return "".join(parts)

    async def send_message_stream(self, message: str):
        message = message.strip()

        if message.lower() in {"exit", "quit"}:
            yield "This interaction is concluded."
            return

        # Generate and display the greeting once.
        if not self._initialized:
            print("[DEBUG] Initializing agent...", flush=True)

            greeting = await self.initialize()

            print("[DEBUG] Initialization finished.", flush=True)

            if greeting:
                yield greeting

            if not message:
                return

            yield "\n\n"
        # Ignore empty messages after initialization.
        if not message:
            return

        print(f"[DEBUG] User message: {message}")
        print(f"[DEBUG] Current history length: {len(self.conversation_history)}")

        self.conversation_history.append({
            "role": "user",
            "content": message,
        })

        full_content = ""

        async for content in self._stream_response():
            full_content += content
            yield content

        print(f"[DEBUG] Full response collected: {full_content!r}")

        self.conversation_history.append({
            "role": "assistant",
            "content": full_content,
        })

    async def _stream_response(self, temp=0.3):
        # Limit tool rounds so a repeated tool request cannot loop forever.
        for _ in range(8):
            stream = await self.ollama_client.chat(
                model=MODEL_NAME,
                messages=self.conversation_history,
                tools=self.tool_schemas or None,
                options={"temperature": temp},
                stream=True,
            )

            content = ""
            thinking = ""
            tool_calls = []

            async for chunk in stream:
                msg = chunk.message

                if msg.content:
                    content += msg.content
                    yield msg.content

                if msg.thinking:
                    thinking += msg.thinking

                if msg.tool_calls:
                    tool_calls.extend(msg.tool_calls)

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
            async with self.client:
                for call in tool_calls:
                    name = call.function.name
                    arguments = call.function.arguments

                    print(
                        f"[DEBUG] Smith requested {name}: {arguments}",
                        flush=True,
                    )

                    try:
                        result = await self.client.call_tool(name, arguments)
                        result_text = "\n".join(
                            block.text
                            for block in result.content
                            if block.type == "text"
                        )
                    except Exception as exc:
                        result_text = f"Tool failed: {exc}"

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
async def chat(request: MessageRequest):
    # If no session_id, generate one (first message with name)
    if request.session_id is None:
        if request.name:
            # Use name + timestamp as fallback ID
            session_id = "user_" + request.name.lower().replace(" ", "_") + "_" + str(int(time.time()))
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

    async def stream_generator():
        print(f"[DEBUG] Starting stream for message: '{message}'")
        async for chunk in agent.send_message_stream(message):
            print(f"[DEBUG] Sending chunk to client: '{chunk}'")
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        print("[DEBUG] Stream complete")
        yield "data: [DONE]\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return {"error": "index.html not found"}, 404

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
    print("Matrix chat server running at http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_server()
