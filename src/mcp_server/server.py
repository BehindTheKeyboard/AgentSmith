from fastmcp import FastMCP
from tools import register_tools
from resources import register_resources

mcp = FastMCP(
    name="Matrix"
)

register_resources(mcp)
register_tools(mcp)

def main():
    print(f"[MCP SERVER] {mcp.name} is starting...")
    print("[MCP SERVER] Waiting for MCP connections (Ollama)...\n")
    
    # Modern / recommended way
    mcp.run(
        transport="http",
        host="127.0.0.1",   # localhost only (safer on Windows)
        port=8080
    )
    
    print("[MCP SERVER] Server has stopped.")

if __name__ == "__main__":    
    main()