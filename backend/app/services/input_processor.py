"""
Curio AI — Input Processor Service.

Cleans and validates user teaching text before it reaches the AI.
Provider-agnostic: does not depend on any AI service.

Extension points:
- Add profanity filtering
- Add language detection
- Add topic-relevance checking
"""

from dataclasses import dataclass, field
from typing import List

from app.config.constants import MAX_USER_MESSAGE_LENGTH
from app.utils.error_handler import CurioValidationError
from app.utils.helpers import sanitize_text, safe_truncate
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ProcessedInput:
    """Result of processing user input."""
    clean_text: str
    original_length: int
    was_truncated: bool = False
    warnings: List[str] = field(default_factory=list)


def process_input(
    raw_text: str,
    max_length: int = MAX_USER_MESSAGE_LENGTH,
) -> ProcessedInput:
    """
    Clean and validate user input text.

    Steps:
        1. Check for empty input
        2. Sanitize (remove control chars, collapse whitespace)
        3. Enforce max length with truncation
        4. Collect warnings for the caller

    Args:
        raw_text: Raw user message
        max_length: Maximum allowed length

    Returns:
        ProcessedInput with clean text and any warnings

    Raises:
        CurioValidationError: If input is empty after cleaning
    """
    if not raw_text or not raw_text.strip():
        raise CurioValidationError(
            message="Message cannot be empty",
            details={"field": "user_message"},
        )

    original_length = len(raw_text)
    warnings: List[str] = []

    # Step 1: Sanitize
    clean = sanitize_text(raw_text)

    # Step 2: Check post-sanitization emptiness
    if not clean:
        raise CurioValidationError(
            message="Message is empty after sanitization",
            details={"field": "user_message"},
        )

    # Step 3: Enforce max length
    was_truncated = False
    if len(clean) > max_length:
        clean = safe_truncate(clean, max_length)
        was_truncated = True
        warnings.append(
            f"Message was truncated from {original_length} to {max_length} characters"
        )
        logger.warning(
            "Input truncated",
            extra={"original_length": original_length, "max_length": max_length},
        )

    # Step 4: Informational warnings
    if len(clean) < 20:
        warnings.append("Very short message — consider providing more detail")

    return ProcessedInput(
        clean_text=clean,
        original_length=original_length,
        was_truncated=was_truncated,
        warnings=warnings,
    )
