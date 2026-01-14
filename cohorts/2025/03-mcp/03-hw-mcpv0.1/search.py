"""Q5: Download FastMCP docs, index markdown files with minsearch, and search.

This script:
- downloads https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip (if missing)
- reads only .md and .mdx files from the zip
- normalizes file paths by stripping the leading "fastmcp-main/"
- indexes docs with minsearch (content + filename)
- provides a `search(query)` function returning top 5 results

Run:
    uv run python search.py
"""

from __future__ import annotations

import io
import os
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import requests
from minsearch import Index


ZIP_URL = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
ZIP_BASENAME = "fastmcp-main.zip"
ZIP_ROOT_PREFIX = "fastmcp-main/"


@dataclass(frozen=True)
class Doc:
    filename: str
    content: str


def _download_zip(*, target_path: Path) -> Path:
    """Download the FastMCP repo zip if it's not already present."""
    target_path.parent.mkdir(parents=True, exist_ok=True)

    if target_path.exists() and target_path.stat().st_size > 0:
        return target_path

    resp = requests.get(ZIP_URL, timeout=60)
    resp.raise_for_status()
    target_path.write_bytes(resp.content)
    return target_path


def _iter_docs_from_zip(zip_path: Path) -> Iterable[Doc]:
    """Yield Doc objects for each .md/.mdx file inside the zip."""
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue

            name = info.filename
            lower = name.lower()
            if not (lower.endswith(".md") or lower.endswith(".mdx")):
                continue

            if name.startswith(ZIP_ROOT_PREFIX):
                name = name[len(ZIP_ROOT_PREFIX) :]

            # read as UTF-8, replacing invalid bytes to avoid crashes
            with zf.open(info) as f:
                raw = f.read()
            text = raw.decode("utf-8", errors="replace")
            yield Doc(filename=name, content=text)


def build_index(*, zip_path: Path | None = None) -> Index:
    """Build and return a fitted minsearch index over FastMCP markdown docs."""
    if zip_path is None:
        zip_path = Path("data") / ZIP_BASENAME

    _download_zip(target_path=zip_path)

    docs = [doc.__dict__ for doc in _iter_docs_from_zip(zip_path)]
    index = Index(text_fields=["content"], keyword_fields=["filename"])
    index.fit(docs)
    return index


def search(query: str, *, index: Index | None = None, limit: int = 5) -> list[dict]:
    """Search the FastMCP docs index and return top results."""
    if index is None:
        index = build_index()

    # minsearch Index.search supports num_results
    results = index.search(query, num_results=limit)
    return results


def main() -> None:
    idx = build_index()
    results = search("demo", index=idx, limit=5)
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r.get('filename')}")


if __name__ == "__main__":
    main()

