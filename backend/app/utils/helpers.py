"""
Curio AI — Common Helper Functions.

Pure utility functions with no side effects and no external dependencies.
"""

import re
import uuid
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return the current UTC time (timezone-aware)."""
    return datetime.now(timezone.utc)


def generate_id(prefix: str = "cur") -> str:
    """
    Generate a unique ID with a prefix.

    Examples:
        generate_id("sess")  -> "sess-a1b2c3d4"
        generate_id("turn")  -> "turn-e5f6g7h8"
        generate_id()        -> "cur-i9j0k1l2"
    """
    short_uuid = uuid.uuid4().hex[:12]
    return f"{prefix}-{short_uuid}"


def safe_truncate(text: str, max_length: int, suffix: str = "…") -> str:
    """
    Truncate text to max_length, appending suffix if truncated.

    Args:
        text: Input text
        max_length: Maximum allowed length (including suffix)
        suffix: String appended when truncation occurs

    Returns:
        Original text if within limit, truncated text otherwise
    """
    if not text or len(text) <= max_length:
        return text
    cutoff = max_length - len(suffix)
    if cutoff <= 0:
        return text[:max_length]
    return text[:cutoff] + suffix


def sanitize_text(text: str) -> str:
    """
    Minimal text sanitization for user input.

    - Strips leading/trailing whitespace
    - Collapses multiple spaces/newlines
    - Removes null bytes and control characters (except newline/tab)
    """
    if not text:
        return ""
    # Remove null bytes and most control chars
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    # Collapse multiple whitespace (preserve single newlines)
    text = re.sub(r"[^\S\n]+", " ", text)
    # Collapse multiple newlines into max 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
