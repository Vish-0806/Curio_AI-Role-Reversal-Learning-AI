"""
Curio AI — Session Routes.

POST /session/create  — Create a new teaching session
GET  /session/{id}    — Retrieve session state
"""

from fastapi import APIRouter, Request

from app.models.chat_model import ResponseEnvelope
from app.models.session_model import SessionCreateRequest, SessionCreateResponse
from app.services.session_manager import session_manager
from app.utils.helpers import generate_id

router = APIRouter(prefix="/session", tags=["Session"])


@router.post("/create", response_model=ResponseEnvelope[SessionCreateResponse])
async def create_session(body: SessionCreateRequest, request: Request):
    """Create a new teaching session."""
    request_id = request.headers.get("X-Request-ID") or generate_id("req")

    session = session_manager.create_session(body)

    return ResponseEnvelope(
        success=True,
        data=SessionCreateResponse(
            session_id=session.session_id,
            created_at=session.created_at,
            expires_at=session.expires_at,
        ),
        request_id=request_id,
    )


@router.get("/{session_id}", response_model=ResponseEnvelope)
async def get_session(session_id: str, request: Request):
    """Retrieve current session state."""
    request_id = request.headers.get("X-Request-ID") or generate_id("req")

    session = session_manager.get_session(session_id)

    return ResponseEnvelope(
        success=True,
        data=session.model_dump(),
        request_id=request_id,
    )
