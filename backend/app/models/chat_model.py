"""
Curio AI — Chat Models.

Defines request/response schemas for the /chat endpoint
and the universal ResponseEnvelope used across all endpoints.
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar

from pydantic import BaseModel, Field

from app.utils.helpers import utc_now

T = TypeVar("T")


# ═══════════════════════════════════════════════════════════════════
#  Universal Response Envelope
# ═══════════════════════════════════════════════════════════════════

class ErrorDetail(BaseModel):
    """Structured error info inside the envelope."""
    code: str
    message: str
    details: Optional[Any] = None


class ResponseEnvelope(BaseModel, Generic[T]):
    """
    Consistent response wrapper used by ALL endpoints.

    Success:  { "success": true,  "data": {...},  "error": null }
    Failure:  { "success": false, "data": null,   "error": {...} }
    """
    success: bool = True
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None
    request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=utc_now)


# ═══════════════════════════════════════════════════════════════════
#  Chat Request / Response
# ═══════════════════════════════════════════════════════════════════

class ChatRequest(BaseModel):
    """Payload for POST /chat — user sends a teaching message."""
    session_id: str = Field(description="Active session identifier")
    user_message: str = Field(description="The user's explanation / teaching text")
    context: Optional[str] = Field(
        default=None,
        description="Optional concept name or topic context",
    )
    mode: Literal["teach", "quiz", "review"] = Field(
        default="teach",
        description="Interaction mode",
    )


class AIFlags(BaseModel):
    """Flags set by the AI to signal pedagogical events."""
    needs_example: bool = Field(default=False)
    detected_gap: bool = Field(default=False)


class ChatResponse(BaseModel):
    """Response from the AI student after processing a teaching message."""
    session_id: str
    ai_message: str = Field(description="The AI student's response text")
    ai_intent: str = Field(
        description="AI's intent: question, challenge, hint, mistake, acknowledgment, etc.",
    )
    followups: List[str] = Field(
        default_factory=list,
        description="Suggested follow-up questions or prompts",
    )
    flags: AIFlags = Field(default_factory=AIFlags)
    updated_state_summary: Optional[str] = Field(
        default=None,
        description="Brief summary of session state changes",
    )
