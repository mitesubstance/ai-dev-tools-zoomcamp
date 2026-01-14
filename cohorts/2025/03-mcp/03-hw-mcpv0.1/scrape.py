"""Utilities for fetching web pages as markdown via Jina Reader.

Jina Reader URL format:
    https://r.jina.ai/<original_url>

Example:
    https://r.jina.ai/https://datatalks.club/
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def _normalize_url(url: str) -> str:
    """Normalize user input into a URL string with scheme.

    Jina requires the full URL (including scheme) after `https://r.jina.ai/`.
    """
    url = url.strip()
    if not url:
        raise ValueError("url must be a non-empty string")

    # If someone passes just a domain, assume https.
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"

    return url


def fetch_markdown(url: str, *, timeout: int = 30) -> str:
    """Fetch a page via Jina Reader and return its markdown content."""
    url = _normalize_url(url)
    jina_url = f"https://r.jina.ai/{url}"

    # Jina Reader (and/or GitHub behind it) can intermittently return 429/503.
    # Add a small retry/backoff so the homework script is reliably runnable.
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        backoff_factor=1.0,
        raise_on_status=False,
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))

    resp = session.get(
        jina_url,
        timeout=timeout,
        headers={
            # Be polite and explicit. Some endpoints treat unknown UAs differently.
            "User-Agent": "ai-dev-tools-zoomcamp-mcp-homework/0.1",
        },
    )

    # After retries, still fail fast if status isn't OK.
    resp.raise_for_status()
    return resp.text


def count_word(text: str, word: str) -> int:
    """Count occurrences of a word (case-insensitive, word boundaries)."""
    if not word:
        raise ValueError("word must be non-empty")

    pattern = re.compile(rf"\\b{re.escape(word)}\\b", flags=re.IGNORECASE)
    return len(pattern.findall(text))
