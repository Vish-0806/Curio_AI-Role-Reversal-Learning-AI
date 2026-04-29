"""
Curio AI — Chat Route.

POST /chat — Handle a teaching conversation turn.
Orchestrates: SessionManager → InputProcessor → PromptBuilder → AIRouter → ResponseFormatter
"""

from fastapi import APIRouter, Request

from app.models.chat_model import ChatRequest, ChatResponse, ResponseEnvelope
from app.services.ai_router import AIRouter
from app.services.input_processor import process_input
from app.services.prompt_payload_builder import build_prompt_payload
from app.services.response_formatter import format_response
from app.services.session_manager import session_manager
from app.utils.helpers import generate_id

router = APIRouter(tags=["Chat"])

# Module-level AI router instance
_ai_router = AIRouter()


@router.post("/chat", response_model=ResponseEnvelope[ChatResponse])
async def chat(body: ChatRequest, request: Request):
    """
    Process a teaching message from the user.

    Flow:
    1. Validate session exists and is active
    2. Clean and validate user input
    3. Build provider-agnostic prompt payload
    4. Send to AI provider via router
    5. Format AI response into ChatResponse
    6. Store both turns in session history
    7. Return wrapped response
    """
    request_id = request.headers.get("X-Request-ID") or generate_id("req")

    # 1. Get session
    session = session_manager.get_session(body.session_id)

    # 2. Process input
    processed = process_input(body.user_message)

    # 3. Append user turn to session
    session = session_manager.append_turn(
        session_id=body.session_id,
        role="user",
        text=processed.clean_text,
    )

    # 4. Build prompt payload
    payload = build_prompt_payload(
        session_state=session,
        user_message=processed.clean_text,
        mode=body.mode,
        context=body.context,
    )

    # 5. Get AI response
    raw_output = _ai_router.generate(payload)

    # 6. Format response
    chat_response = format_response(
        session_id=body.session_id,
        raw_output=raw_output,
    )

    # 7. Append AI turn to session
    session_manager.append_turn(
        session_id=body.session_id,
        role="ai",
        text=chat_response.ai_message,
        annotations={
            "ai_intent": chat_response.ai_intent,
            "flags": chat_response.flags.model_dump(),
        },
    )

    # 8. Add state summary if there were input warnings
    if processed.warnings:
        chat_response.updated_state_summary = "; ".join(processed.warnings)

    return ResponseEnvelope(
        success=True,
        data=chat_response,
        request_id=request_id,
    )
