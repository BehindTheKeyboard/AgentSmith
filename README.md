# Agent Smith — Matrix Chat

A browser-based conversation with Agent Smith, powered by an Ollama model and a FastMCP tool server. Smith can investigate possible candidates for the One, scan for fictional Matrix anomalies, and check for nearby agents. The interface streams replies and displays a Matrix-style scan terminal.

The project is a starting point for experimenting with AI agents, tool calling, persistent tool memory, and a custom chat interface. Scans are fictional game events, not real network scans. Most additional agents, locations, and activities are original fiction inspired by The Matrix.

## What runs where?

| Component | Purpose | Default address |
| --- | --- | --- |
| Ollama | Runs the language model locally, or connects to Ollama Cloud | `http://127.0.0.1:11434` |
| MCP server | Exposes scan and investigation tools | `http://127.0.0.1:8080/mcp` |
| Chat client server | Serves the web page and coordinates model/tool calls | `http://127.0.0.1:8000` |

The Python “client” is also the web server. Keep it and the MCP server running in separate terminals.

## Requirements and setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and [Ollama](https://ollama.com/download). Use the Python version required by the repository's `pyproject.toml` or `.python-version` file.

From the project root (`Agent/`), install the declared dependencies:

```bash
uv sync
```

Choose one model option below. Use a model that supports tool calling; model quality affects how reliably Smith follows instructions and uses tools.

## Option A: Self-host the model locally

Start the Ollama application. If it is not already serving the API, run this in a separate terminal and leave it open:

```bash
ollama serve
```

In another terminal, download and test the model:

```bash
ollama run qwen3:8b
```

After it responds, enter `/bye` to leave the test chat. Keep the Ollama service running; the Python client will request the model when needed.

In `src/client/client.py`, use:

```python
MODEL_NAME = "qwen3:8b"
OLLAMA_SERVER_URL = "http://127.0.0.1:11434"
MCP_SERVER_URL = "http://127.0.0.1:8080/mcp"
```

The model runs on your computer. Available RAM/VRAM, model size, and context length affect speed. The first response can take longer while the model loads. `ollama list` shows downloaded models; `ollama ps` shows loaded models.

## Option B: Use an Ollama Cloud model

This option keeps the same local Ollama connection in the Python client, but Ollama sends model requests to its cloud service. It requires internet access and an Ollama account; account limits or charges may apply.

With Ollama running, sign in and test a cloud model:

```bash
ollama signin
ollama run gpt-oss:120b-cloud
```

Enter `/bye` after the test. Change the settings in `src/client/client.py` to:

```python
MODEL_NAME = "gpt-oss:120b-cloud"
OLLAMA_SERVER_URL = "http://127.0.0.1:11434"
```

Keep the MCP URL unchanged. Keep local Ollama running as the gateway. Model prompts and tool results included in the conversation are sent to the cloud provider.

Direct cloud access is also possible with `ollama.AsyncClient(host="https://ollama.com", headers={"Authorization": "Bearer ..."})`, but it requires changing client initialization and supplying an API key from an environment variable. Merely changing the model name does not configure another provider. OpenAI or other APIs require an appropriate client adapter, including tool-call and streaming handling.

## Run the project

Run each terminal's commands from the project root. Start the MCP server first.

### Terminal 1 — MCP server

```bash
cd src/mcp_server
uv run -m server
```

### Terminal 2 — chat client server

```bash
cd src/client
uv run -m client
```

Open [the chat page](http://127.0.0.1:8000) in your browser. Use this address rather than opening `index.html` directly. The client currently reads its web assets relative to its working directory, so launching it from `src/client` matters.

Try:

- “My name is Adam.”
- “Where am I? What is going on?”
- “Scan the Matrix near the Forty-One Restaurant.”
- “Are any other agents looking for you?”
- “What did your previous agent scan find?”

A name is optional with the updated message flow. Typing `exit` or `quit` ends the interaction but does not stop the servers. Press `Ctrl+C` in each terminal to stop them.

## Main files

| Path | Purpose |
| --- | --- |
| `src/client/client.py` | FastAPI routes, model settings, Smith's prompt, sessions, tool loop |
| `src/client/chat.js` | Chat requests, streamed replies, scan terminal |
| `src/client/styles.css` | Chat appearance and animations |
| `src/mcp_server/server.py` | MCP server startup and logging configuration |
| `src/mcp_server/tools.py` | Tool implementations and memory helpers |
| `src/mcp_server/matrix_data.py` | Detection rules, anomalies, agents, environments, activities |
| `src/logs/` | Timestamped client and MCP log files |

## Memory and customization

The current memory helpers store `agent_memory.json` and `one_memory.json` beside `tools.py`. These files survive server restarts. Conversation history and session names are held in memory and do not survive a client-server restart. Opening a fresh browser page creates a new session with the current frontend.

Edit `matrix_data.py` to expand the fiction. Location aliases are resolved by the helper in `tools.py`; readable display names keep internal IDs out of Smith's replies. Recent-activity filtering reduces immediate repeats but resets with the MCP process.

- After changing tools or data, restart the MCP server.
- After changing model settings, the system prompt, or client Python, restart the client server and start a new chat.
- After adding tools or changing tool names/parameters, restart both servers so the client reloads tool schemas.
- After changing JavaScript or CSS, refresh the browser; use a hard refresh if cached assets persist.

Use these local ignore entries to keep generated logs and game memory out of commits:

```gitignore
.venv/
__pycache__/
*.pyc
src/logs/
src/mcp_server/agent_memory.json
src/mcp_server/one_memory.json
.env
```

This is a development app without user authentication. Binding to `0.0.0.0` allows connections on available network interfaces; bind to `127.0.0.1` for access only from your computer. Keep API keys out of browser code and source control. Debug logs and memory files may contain conversation details.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `All connection attempts failed` | Read the MCP terminal for startup errors. Confirm it is running and its URL matches `MCP_SERVER_URL`. |
| `No module named server` or `client` | Launch from the respective directory shown above. |
| Cannot find `matrix_data` | With the current launch layout, use `from matrix_data import ...` in `tools.py`. |
| Model not found | Verify `MODEL_NAME` exactly matches the local model or cloud model tag. |
| Ollama port already in use | Ollama may already be running. Check `ollama list` before starting another service. |
| “Agent Smith is typing…” for a long time | Check the latest client log for MCP initialization, Ollama progress, thinking-only chunks, or a tool wait. |
| First question becomes the user's name | Ensure `chat.js` sends the actual first message with `streamResponse(text)`. |
| Logging format error | Use placeholders: `logger.info("Location: %s", location)`. |
| Location cannot be matched | Check aliases and preserve uncertainty; “near a restaurant” is not a confirmed named restaurant. |

Logs use a new timestamped file on each launch. Set `level=logging.DEBUG` in each entry point for detailed diagnostics. Check the MCP log for tool errors and the client log for model/stream errors.

## References

- [uv project setup](https://docs.astral.sh/uv/guides/projects/)
- [Ollama Python client and cloud API](https://github.com/ollama/ollama-python)
- [Ollama authentication and cloud sign-in](https://github.com/ollama/ollama/blob/main/docs/api/authentication.mdx)
- [Qwen3 local Ollama setup](https://github.com/QwenLM/Qwen3)
