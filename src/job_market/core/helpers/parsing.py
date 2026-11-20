"""Helpers for turning API markup into readable text."""

import html
import re

_BLOCK_TAGS = re.compile(
    r"<\s*/?\s*(?:article|div|h[1-6]|li|ol|p|section|tr|ul|br)\b[^>]*>",
    re.IGNORECASE,
)
_HIDDEN_CONTENT = re.compile(
    r"<\s*(script|style)\b[^>]*>.*?<\s*/\s*\1\s*>",
    re.IGNORECASE | re.DOTALL,
)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_TAG = re.compile(r"<[^>]+>")


def html_to_text(markup: str) -> str:
    """Extract text while keeping paragraph and list-item boundaries."""
    text = markup.replace("\r", " ").replace("\n", " ")
    text = _HIDDEN_CONTENT.sub("", text)
    text = _COMMENT.sub("", text)
    text = _BLOCK_TAGS.sub("\n", text)
    text = html.unescape(_TAG.sub("", text))
    text = re.sub(r"[^\S\n]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\n{2,}", "\n", text).strip()
