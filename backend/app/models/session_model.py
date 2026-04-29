"""
Curio AI — Session Models.

Defines the data structures for session lifecycle:
creation, state tracking, conversation turns, and expiry.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator

from app.utils.helpers import generate_id, utc_now


# ═══════════════════════════════════════════════════════════════════
#  Request / Response Models
# ═══════════════════════════════════════════════════════════════════

class SessionCreateRequest(BaseModel):
    """Payload to create a new teaching session."""
    user_id: Optional[Union[str, int]] = Field(default=None, description="Optional user identifier (accepts string or int)")
    topic: Optional[str] = Field(default=None, description="Topic the user will teach")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata (defaults to empty dict)")

    @field_validator("user_id", mode="before")
    @classmethod
    def convert_user_id_to_string(cls, v):
        """Convert int user_id to string, preserve string inputs."""
        if v is None:
            return None
        if isinstance(v, int):
            return str(v)
        if isinstance(v, str):
            return v
        return str(v)

    @field_validator("metadata", mode="before")
    @classmethod
    def ensure_metadata_dict(cls, v):
        """Ensure metadata is always a dict, default to empty dict."""
        if v is None:
            return {}
        if isinstance(v, dict):
            return v
        return {}


class SessionCreateResponse(BaseModel):
    """Response after successfully creating a session."""
    session_id: str
    created_at: datetime
    expires_at: datetime


# ═══════════════════════════════════════════════════════════════════
#  Internal State Models
# ═══════════════════════════════════════════════════════════════════

class ConversationTurn(BaseModel):
    """A single turn in the conversation (user or AI)."""
    turn_id: str = Field(default_factory=lambda: generate_id("turn"))
    role: Literal["user", "ai"] = Field(description="Who sent this message")
    text: str = Field(description="Message content")
    timestamp: datetime = Field(default_factory=utc_now)
    annotations: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata (e.g., ai_intent, flags)",
    )


class SessionState(BaseModel):
    """
    Full state of a teaching session with cognitive tracking.

    Designed for future persistence: version field for schema migrations,
    extras dict for ad-hoc data without schema changes.
    
    COGNITIVE SYSTEM FIELDS:
    - current_mode: AI behavioral mode (student, teacher, rescue, evaluator)
    - difficulty_level: Question difficulty (1=beginner, 2=intermediate, 3=expert)
    - user_understanding_score: Rolling understanding metric (0-100)
    - confidence_score: System confidence in user mastery (0-100)
    - question_count: Total questions asked in session
    - mode_switch_history: Timeline of mode transitions with reasons
    - user_response_quality_scores: Per-response quality ratings for progression
    - user_topic_understanding: System's summary of user's topic understanding
    """
    # ── Identity ─────────────────────────────────────────────────
    session_id: str = Field(default_factory=lambda: generate_id("sess"))
    version: int = Field(default=2, description="Schema version for migrations")

    # ── Timestamps ───────────────────────────────────────────────
    created_at: datetime = Field(default_factory=utc_now)
    expires_at: datetime  # Set by SessionManager based on TTL

    # ── User Info ────────────────────────────────────────────────
    user_id: Optional[str] = None
    topic: Optional[str] = None

    # ── Conversation ─────────────────────────────────────────────
    conversation: List[ConversationTurn] = Field(default_factory=list)

    # ── COGNITIVE STATE TRACKING ─────────────────────────────────
    # AI Mode & Difficulty Control
    current_mode: Literal["student", "teacher", "rescue", "evaluator"] = Field(
        default="student",
        description="Current AI behavioral mode"
    )
    difficulty_level: Literal[1, 2, 3] = Field(
        default=1,
        description="Question difficulty: 1=beginner, 2=intermediate, 3=expert"
    )
    
    # Understanding & Confidence Metrics
    user_understanding_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Rolling metric of user mastery (0-100)"
    )
    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="System confidence in user understanding (0-100)"
    )
    
    # Question & Response Tracking
    question_count: int = Field(default=0, description="Total questions asked")
    user_response_quality_scores: List[float] = Field(
        default_factory=list,
        description="Quality scores for each user response (0-1 scale)"
    )
    
    # Mode History
    mode_switch_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Timeline of mode transitions: {timestamp, old_mode, new_mode, reason}"
    )
    
    # Understanding Summary
    user_topic_understanding: Optional[str] = Field(
        default=None,
        description="AI's learned summary of what user understands about topic"
    )

    # ── Evaluation ───────────────────────────────────────────────
    last_evaluation: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Most recent evaluation result (stored as dict for flexibility)",
    )

    # ── Extensibility ────────────────────────────────────────────
    settings_overrides: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Per-session settings overrides",
    )
    extras: Dict[str, Any] = Field(
        default_factory=dict,
        description="Arbitrary extra data for future use",
    )

    model_config = {"from_attributes": True}
