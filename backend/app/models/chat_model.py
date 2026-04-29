"""
Curio AI — Chat Models.

Defines request/response schemas for the /chat endpoint
and the universal ResponseEnvelope used across all endpoints.
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, field_validator

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
    session_id: str = Field(
        description="Active session identifier",
        examples=["507f1f77bcf86cd799439011"]
    )
    user_message: str = Field(
        description="The user's explanation / teaching text",
        examples=["V equals I times R, which means voltage equals current multiplied by resistance"]
    )
    context: Optional[Union[str, Dict[str, Any]]] = Field(
        default=None,
        description="Optional concept name or topic context (accepts string or dict)",
        examples=[
            {"key": "value", "topic": "Ohm's Law"},
            "V = IR"
        ]
    )
    mode: Literal["teach", "quiz", "review"] = Field(
        default="teach",
        description="Interaction mode",
        examples=["teach", "quiz", "review"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "session_id": "507f1f77bcf86cd799439011",
                    "user_message": "Explain Ohm's Law - voltage equals current times resistance",
                    "context": {"topic": "electrical_engineering", "level": "beginner"},
                    "mode": "teach"
                },
                {
                    "session_id": "507f1f77bcf86cd799439012",
                    "user_message": "What is photosynthesis?",
                    "context": "photosynthesis",
                    "mode": "teach"
                },
                {
                    "session_id": "507f1f77bcf86cd799439013",
                    "user_message": "Explain the water cycle",
                    "context": None,
                    "mode": "quiz"
                }
            ]
        }
    }

    @field_validator("context", mode="before")
    @classmethod
    def convert_context_to_dict(cls, v):
        """Convert string context to dict format, preserve dict inputs."""
        if isinstance(v, str):
            return {"value": v}
        return v


class AIFlags(BaseModel):
    """Flags set by the AI to signal pedagogical events."""
    needs_example: bool = Field(default=False)
    detected_gap: bool = Field(default=False)


class ChatResponse(BaseModel):
    """Response from the AI student after processing a teaching message."""
    session_id: str
    ai_message: str = Field(description="The AI student's response text")
    ai_intent: str = Field(
        default="question",
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
    
    # ── NEW COGNITIVE SYSTEM FIELDS ──
    mode: Optional[str] = Field(
        default="student",
        description="Current AI mode: student, teacher, rescue, evaluator",
    )
    difficulty_level: Optional[int] = Field(
        default=1,
        description="Current difficulty level: 1 (beginner), 2 (intermediate), 3 (expert)",
    )
    confidence_score: Optional[float] = Field(
        default=0.0,
        description="System's confidence in user understanding (0-100)",
    )
    progress_state: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Session progress tracking data",
    )
    termination_offer: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional offer to end session when confidence is high",
    )
