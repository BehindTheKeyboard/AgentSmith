from mcp.server.fastmcp import FastMCP

def register_resources(mcp: FastMCP):

    @mcp.resource(
        uri="example://hello",
        name="Hello Resource",
        description="Simple static resource"
    )
    def hello_resource() -> str:
        return "Hello from MCP resource!"
