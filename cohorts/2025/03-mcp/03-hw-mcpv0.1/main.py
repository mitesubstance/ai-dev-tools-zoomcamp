from fastmcp import FastMCP

from scrape import count_word, fetch_markdown

mcp = FastMCP("Demo 🚀")


def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


def scrape_web(url: str) -> str:
    """Fetch a web page (via Jina Reader) and return it as markdown."""
    return fetch_markdown(url)


def count_word_on_page(url: str, word: str) -> int:
    """Fetch a page (via Jina Reader) and count whole-word occurrences of `word`.

    Counting is case-insensitive and uses word boundaries (so `data` won't match
    `database`).
    """
    text = fetch_markdown(url)
    return count_word(text, word)


# Register tools. Using the function-call form keeps the underlying Python
# functions callable (the decorator form replaces them with FunctionTool).
_add_tool = mcp.tool(add)
_scrape_web_tool = mcp.tool(scrape_web)
_count_word_on_page_tool = mcp.tool(count_word_on_page)


if __name__ == "__main__":
    mcp.run()
