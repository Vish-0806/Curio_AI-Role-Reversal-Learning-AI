"""
Curio AI — Response Formatter Service.

Transforms raw AI output (dict) into a typed ChatResponse.
Provider-agnostic: does not depend on any AI service.

Extension points:
- Add response post-processing (sentiment analysis, content filtering)
- Add response caching
- Add A/B test variant selection
"""

from typing import Any, Dict, List, Optional

from app.config.constants import MAX_AI_RESPONSE_LENGTH
from app.models.chat_model import AIFlags, ChatResponse
from app.utils.helpers import safe_truncate
from app.utils.logger import get_logger

logger = get_logger(__name__)


def format_response(
    session_id: str,
    raw_output: Dict[str, Any],
    max_length: int = MAX_AI_RESPONSE_LENGTH,
) -> ChatResponse:
    """
    Build a ChatResponse from raw AI output dict.

    Expected raw_output keys:
        - ai_message (str): The AI's response text
        - ai_intent (str): Intent classification
        - followups (list[str]): Suggested follow-ups
        - flags (dict): {needs_example: bool, detected_gap: bool}

    Missing keys are filled with safe defaults.

    Args:
        session_id: The active session ID
        raw_output: Dict from the AI provider
        max_length: Max length for ai_message

    Returns:
        Validated ChatResponse
    """
    # Extract with safe defaults
    ai_message = raw_output.get("ai_message", "I'm not sure how to respond to that.")
    ai_intent = raw_output.get("ai_intent", "acknowledgment")
    followups = raw_output.get("followups", [])
    flags_raw = raw_output.get("flags", {})

    # Enforce message length
    if len(ai_message) > max_length:
        ai_message = safe_truncate(ai_message, max_length)
        logger.warning(
            "AI response truncated",
            extra={"session_id": session_id, "original_length": len(ai_message)},
        )

    # Normalize followups
    if not isinstance(followups, list):
        followups = []
    followups = [str(f) for f in followups if f][:5]  # Max 5 followups

    # Build flags
    flags = AIFlags(
        needs_example=bool(flags_raw.get("needs_example", False)),
        detected_gap=bool(flags_raw.get("detected_gap", False)),
    )

    return ChatResponse(
        session_id=session_id,
        ai_message=ai_message,
        ai_intent=ai_intent,
        followups=followups,
        flags=flags,
    )
