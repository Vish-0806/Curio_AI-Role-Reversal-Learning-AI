"""
Curio AI — Session Manager Service.

In-memory session store for MVP, designed with a clean interface
so persistence (Redis, PostgreSQL, etc.) can be swapped in later
by implementing the same method signatures.

Thread-safe via threading.Lock.
"""

import threading
from datetime import timedelta
from typing import Dict, Optional

from app.config.settings import get_settings
from app.models.session_model import (
    ConversationTurn,
    SessionCreateRequest,
    SessionState,
)
from app.utils.error_handler import NotFoundError, SessionExpiredError
from app.utils.helpers import generate_id, utc_now
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SessionManager:
    """
    Manages teaching session lifecycle (in-memory).

    Extension point: Replace this class with a DB-backed implementation
    that has the same public interface (create_session, get_session, etc.).
    """

    def __init__(self):
        self._store: Dict[str, SessionState] = {}
        self._lock = threading.Lock()

    def create_session(self, request: SessionCreateRequest) -> SessionState:
        """Create a new teaching session."""
        settings = get_settings()
        now = utc_now()
        session = SessionState(
            session_id=generate_id("sess"),
            created_at=now,
            expires_at=now + timedelta(minutes=settings.SESSION_TTL_MINUTES),
            user_id=request.user_id,
            topic=request.topic,
            extras=request.metadata,
        )
        with self._lock:
            self._store[session.session_id] = session

        logger.info(
            "Session created",
            extra={"session_id": session.session_id, "topic": request.topic},
        )
        return session

    def get_session(self, session_id: str) -> SessionState:
        """
        Retrieve a session by ID.

        Raises:
            NotFoundError: If session does not exist.
            SessionExpiredError: If session has expired.
        """
        with self._lock:
            session = self._store.get(session_id)

        if session is None:
            raise NotFoundError(f"Session '{session_id}' not found")

        if utc_now() > session.expires_at:
            # Clean up expired session
            with self._lock:
                self._store.pop(session_id, None)
            raise SessionExpiredError(session_id)

        return session

    def append_turn(
        self,
        session_id: str,
        role: str,
        text: str,
        annotations: Optional[Dict] = None,
    ) -> SessionState:
        """
        Append a conversation turn to a session.

        Args:
            session_id: Target session
            role: "user" or "ai"
            text: Message content
            annotations: Optional metadata (ai_intent, flags, etc.)

        Returns:
            Updated SessionState
        """
        session = self.get_session(session_id)
        turn = ConversationTurn(
            turn_id=generate_id("turn"),
            role=role,
            text=text,
            timestamp=utc_now(),
            annotations=annotations,
        )

        with self._lock:
            session.conversation.append(turn)
            # Enforce max conversation history
            from app.config.constants import MAX_CONVERSATION_HISTORY
            if len(session.conversation) > MAX_CONVERSATION_HISTORY:
                session.conversation = session.conversation[-MAX_CONVERSATION_HISTORY:]

        logger.info(
            "Turn appended",
            extra={
                "session_id": session_id,
                "role": role,
                "turn_id": turn.turn_id,
                "total_turns": len(session.conversation),
            },
        )
        return session

    def update_last_evaluation(self, session_id: str, evaluation_result: dict) -> SessionState:
        """Store the latest evaluation result in the session."""
        session = self.get_session(session_id)
        with self._lock:
            session.last_evaluation = evaluation_result
        logger.info("Evaluation stored", extra={"session_id": session_id})
        return session

    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions from the store.

        Returns:
            Number of sessions removed.
        """
        now = utc_now()
        removed = 0
        with self._lock:
            expired_ids = [
                sid for sid, s in self._store.items()
                if now > s.expires_at
            ]
            for sid in expired_ids:
                del self._store[sid]
                removed += 1

        if removed:
            logger.info(f"Cleaned up {removed} expired session(s)")
        return removed

    @property
    def active_session_count(self) -> int:
        """Return the number of active (non-expired) sessions."""
        with self._lock:
            return len(self._store)


# ── Module-level singleton ───────────────────────────────────────
# Services import this instance rather than creating their own.
session_manager = SessionManager()
