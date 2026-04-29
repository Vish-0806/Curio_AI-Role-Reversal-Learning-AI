"""
Curio AI — Session Models.

Defines the data structures for session lifecycle:
creation, state tracking, conversation turns, and expiry.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from app.utils.helpers import generate_id, utc_now


# ═══════════════════════════════════════════════════════════════════
#  Request / Response Models
# ═══════════════════════════════════════════════════════════════════

class SessionCreateRequest(BaseModel):
    """Payload to create a new teaching session."""
    user_id: Optional[str] = Field(default=None, description="Optional user identifier")
    topic: Optional[str] = Field(default=None, description="Topic the user will teach")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata")


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
    Full state of a teaching session.

    Designed for future persistence: version field for schema migrations,
    extras dict for ad-hoc data without schema changes.
    """
    # ── Identity ─────────────────────────────────────────────────
    session_id: str = Field(default_factory=lambda: generate_id("sess"))
    version: int = Field(default=1, description="Schema version for migrations")

    # ── Timestamps ───────────────────────────────────────────────
    created_at: datetime = Field(default_factory=utc_now)
    expires_at: datetime  # Set by SessionManager based on TTL

    # ── User Info ────────────────────────────────────────────────
    user_id: Optional[str] = None
    topic: Optional[str] = None

    # ── Conversation ─────────────────────────────────────────────
    conversation: List[ConversationTurn] = Field(default_factory=list)

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
