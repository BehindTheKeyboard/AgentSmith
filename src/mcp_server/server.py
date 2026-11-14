from fastmcp import FastMCP
from resources import register_resources
from pathlib import Path
import logging
from datetime import datetime

LOG_DIR = Path(__file__).resolve().parents[2] / "src" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")

logging.basicConfig(
        filename=LOG_DIR / f'mcp_server_{timestamp}.log', 
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        encoding="utf-8",
)
logger = logging.getLogger(__name__)

from tools import register_tools

mcp = FastMCP(
    name="Matrix"
)

register_resources(mcp)
register_tools(mcp)

def main():
    
    logger.info("%s is starting...", mcp.name)
    logger.info("Waiting for MCP connections (Ollama)...")
    
    # Modern / recommended way
    mcp.run(
        transport="http",
        host="127.0.0.1",   # localhost only (safer on Windows)
        port=8080
    )
    
    logger.info("MCP Server has stopped.")

if __name__ == "__main__":    
    main()