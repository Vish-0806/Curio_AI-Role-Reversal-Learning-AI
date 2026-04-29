"""
Curio AI — Prompt Payload Builder.

Builds a provider-agnostic prompt payload from session state,
user message, and interaction mode. This is the central place
to craft the AI's behavior as a "curious student."

Extension points:
- Add conversation summarization (currently a placeholder)
- Add per-topic custom system prompts
- Add multi-language support
- Version prompt templates for A/B testing
"""

from typing import Any, Dict, List, Optional

from app.config.constants import (
    DEFAULT_MODE,
    HISTORY_WINDOW_FOR_PROMPT,
    SYSTEM_PROMPTS,
)
from app.models.session_model import ConversationTurn, SessionState
from app.utils.logger import get_logger

logger = get_logger(__name__)


def build_prompt_payload(
    session_state: SessionState,
    user_message: str,
    mode: str = DEFAULT_MODE,
    context: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Build a provider-agnostic prompt payload.

    The payload is a dict that any AI client can consume.
    It contains:
        - system_prompt: Instructions for AI student behavior
        - conversation_history: Recent turns for context
        - user_message: The current teaching message
        - output_schema: JSON format instructions
        - metadata: Mode, topic, context info

    Args:
        session_state: Current session with conversation history
        user_message: The user's current teaching message
        mode: Interaction mode (teach, quiz, review)
        context: Optional concept name or topic context

    Returns:
        Dict payload ready for any AI provider
    """
    # ── 1. Select system prompt ──────────────────────────────────
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS[DEFAULT_MODE])

    # Add topic context if available
    topic = context or session_state.topic
    if topic:
        system_prompt += f"\n\nThe current topic is: {topic}"

    # ── 2. Build conversation history ────────────────────────────
    history = _compact_history(
        session_state.conversation,
        window_size=HISTORY_WINDOW_FOR_PROMPT,
    )

    # ── 3. Output schema instructions ────────────────────────────
    output_instructions = (
        "\n\nYou MUST respond with valid JSON matching this exact schema:\n"
        "{\n"
        '  "ai_message": "your response text",\n'
        '  "ai_intent": "question|challenge|hint|mistake|acknowledgment|summary|follow_up",\n'
        '  "followups": ["optional follow-up question 1", "..."],\n'
        '  "flags": {\n'
        '    "needs_example": true/false,\n'
        '    "detected_gap": true/false\n'
        "  }\n"
        "}\n"
        "Do NOT include any text outside the JSON object."
    )

    full_system_prompt = system_prompt + output_instructions

    # ── 4. Assemble payload ──────────────────────────────────────
    payload = {
        "system_prompt": full_system_prompt,
        "conversation_history": history,
        "user_message": user_message,
        "metadata": {
            "mode": mode,
            "topic": topic,
            "session_id": session_state.session_id,
            "turn_count": len(session_state.conversation),
        },
    }

    logger.info(
        "Prompt payload built",
        extra={
            "session_id": session_state.session_id,
            "mode": mode,
            "history_turns": len(history),
        },
    )

    return payload


def _compact_history(
    conversation: List[ConversationTurn],
    window_size: int,
) -> List[Dict[str, str]]:
    """
    Compact conversation history for the prompt.

    Currently: return last N turns as simple role/content dicts.
    Future: add summarization of older turns.

    Args:
        conversation: Full conversation history
        window_size: Number of recent turns to include

    Returns:
        List of {"role": ..., "content": ...} dicts
    """
    recent = conversation[-window_size:] if len(conversation) > window_size else conversation

    history = []

    # Placeholder for future summarization:
    # If conversation is longer than window, prepend a summary
    if len(conversation) > window_size:
        history.append({
            "role": "system",
            "content": f"[Summary of {len(conversation) - window_size} earlier turns — summarization not yet implemented]",
        })

    for turn in recent:
        history.append({
            "role": turn.role,
            "content": turn.text,
        })

    return history
