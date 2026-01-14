from fastmcp import FastMCP

from scrape import fetch_markdown

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool
def scrape_web(url: str) -> str:
    """Fetch a web page (via Jina Reader) and return it as markdown."""
    return fetch_markdown(url)

if __name__ == "__main__":
    mcp.run()
