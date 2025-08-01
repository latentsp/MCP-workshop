from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    """
    Returns a simple greeting.
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run() 