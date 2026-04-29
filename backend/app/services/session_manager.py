"""
Curio AI — Session Manager Service (MongoDB Version)
"""

from datetime import timedelta, timezone
from typing import Optional, Dict

from bson import ObjectId

from app.database.mongodb import mongo_connected, mongo_error, sessions
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
    MongoDB-backed session manager
    """

    def create_session(self, request: SessionCreateRequest) -> SessionState:
        """Create a new teaching session"""
        settings = get_settings()
        now = utc_now()

        session = SessionState(
            session_id="",  # temporary
            created_at=now,
            expires_at=now + timedelta(minutes=settings.SESSION_TTL_MINUTES),
            user_id=request.user_id,
            topic=request.topic,
            extras=request.metadata,
            conversation=[],
            last_evaluation=None,
        )

        session_dict = session.model_dump()

        # 🔥 STEP 1: INSERT INTO DB
        result = sessions.insert_one(session_dict)

        # 🔥 STEP 2: GET GENERATED ID
        mongo_id = str(result.inserted_id)

        # 🔥 STEP 3: UPDATE session_id FIELD IN DB
        sessions.update_one(
            {"_id": result.inserted_id},
            {"$set": {"session_id": mongo_id}}
        )

        # 🔥 STEP 4: UPDATE OBJECT
        session.session_id = mongo_id

        logger.info(
            "Session created",
            extra={"session_id": mongo_id, "topic": request.topic},
        )

        return session

    @property
    def active_session_count(self) -> int:
        """Return active session count for health endpoint."""
        try:
            return int(sessions.count_documents({}))
        except Exception:
            return 0

    def get_session(self, session_id: str) -> SessionState:
        """Retrieve session from MongoDB with safe ObjectId validation."""
        if not session_id or not isinstance(session_id, str):
            logger.warning(
                "Invalid session_id format",
                extra={"session_id": session_id, "type": type(session_id).__name__},
            )
            raise NotFoundError(f"Invalid session ID format: '{session_id}'")

        lookup_ids = []
        
        # Try ObjectId conversion safely
        try:
            if len(session_id) == 24:  # Valid hex string length for ObjectId
                lookup_ids.append(ObjectId(session_id))
                logger.debug(f"ObjectId conversion successful for: {session_id}")
        except (ValueError, Exception) as e:
            # ObjectId conversion failed, log and continue with string lookup
            logger.debug(
                "ObjectId conversion failed, will try string lookup",
                extra={"session_id": session_id, "error": str(e)},
            )
        
        # Always try string lookup as fallback
        lookup_ids.append(session_id)

        session_data = None
        for lookup_id in lookup_ids:
            try:
                session_data = sessions.find_one({"_id": lookup_id})
                if session_data is not None:
                    logger.debug(f"Session found using lookup_id: {lookup_id}")
                    break
            except Exception as e:
                logger.debug(f"Failed to query with lookup_id {lookup_id}: {str(e)}")
                continue

        if session_data is None:
            logger.warning(f"Session not found: {session_id}")
            raise NotFoundError(f"Session '{session_id}' not found")

        session_data.pop("_id", None)

        session = SessionState(**session_data)

        expiry = session.expires_at
        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
            session.expires_at = expiry

        if utc_now() > expiry:
            if "_id" in session_data:
                sessions.delete_one({"_id": session_data["_id"]})
            raise SessionExpiredError(session_id)

        return session

    def append_turn(
        self,
        session_id: str,
        role: str,
        text: str,
        annotations: Optional[Dict] = None,
    ) -> SessionState:
        """Append a conversation turn"""

        turn = ConversationTurn(
            turn_id=generate_id("turn"),
            role=role,
            text=text,
            timestamp=utc_now(),
            annotations=annotations,
        )

        sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$push": {"conversation": turn.model_dump()}}
        )

        logger.info(
            "Turn appended",
            extra={
                "session_id": session_id,
                "role": role,
                "turn_id": turn.turn_id,
            },
        )

        return self.get_session(session_id)

    def update_last_evaluation(self, session_id: str, evaluation_result: dict) -> SessionState:
        """Store evaluation in MongoDB"""

        sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"last_evaluation": evaluation_result}}
        )

        logger.info("Evaluation stored", extra={"session_id": session_id})

        return self.get_session(session_id)


# Singleton instance
session_manager = SessionManager()

if not mongo_connected:
    logger.warning(
        "MongoDB unavailable. Using in-memory session store.",
        extra={"mongo_error": mongo_error},
    )