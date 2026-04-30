"""
Curio AI — Chat Route.

POST /chat — Handle a teaching conversation turn.
Integrated with adaptive cognitive controller for role-reversal learning.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Request

from app.models.chat_model import ChatRequest, ChatResponse, ResponseEnvelope, ErrorDetail, AIFlags
from app.services.input_processor import process_input
from app.services.session_manager import session_manager
from app.services.ai_service import get_ai_response   # Adaptive cognitive controller
from app.utils.error_handler import NotFoundError, SessionExpiredError
from app.utils.helpers import generate_id
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["Chat"])


def normalize_context(context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Normalize context data for safe processing.
    
    Rules:
    - If context is None, return empty dict
    - If context is a dict, return as-is
    - If context is a string (legacy), convert to {"value": string}
    
    Args:
        context: Raw context from request (may be string, dict, or None)
    
    Returns:
        Normalized dict context
    """
    if context is None:
        return {}
    if isinstance(context, dict):
        return context
    if isinstance(context, str):
        return {"value": context}
    return {}


@router.post("/chat", response_model=ResponseEnvelope[ChatResponse])
async def chat(body: ChatRequest, request: Request):
    request_id = request.headers.get("X-Request-ID") or generate_id("req")

    try:
        # Log incoming request
        logger.debug(
            "Chat request received",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "mode": body.mode,
                "user_message_length": len(body.user_message),
                "context_type": type(body.context).__name__ if body.context else "None",
            },
        )

        # 1. Normalize context input
        normalized_context = normalize_context(body.context)
        logger.debug(
            "Context normalized",
            extra={
                "request_id": request_id,
                "normalized_context": normalized_context,
            },
        )

        # 2. Get session
        session = session_manager.get_session(body.session_id)
        logger.debug(
            "Session retrieved",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "conversation_length": len(session.conversation),
            },
        )

        # 3. Process input
        processed = process_input(body.user_message)
        logger.debug(
            "Input processed",
            extra={
                "request_id": request_id,
                "original_length": len(body.user_message),
                "cleaned_length": len(processed.clean_text),
                "warnings_count": len(processed.warnings) if processed.warnings else 0,
                "warnings": processed.warnings if processed.warnings else [],
            },
        )

        # 4. Store user message
        session = session_manager.append_turn(
            session_id=body.session_id,
            role="user",
            text=processed.clean_text,
        )
        logger.debug(
            "User message stored",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "turn_count": len(session.conversation),
            },
        )

        # 5. Generate adaptive AI response using the cognitive controller
        ai_output = get_ai_response(
            session,
            processed.clean_text
        )
        logger.debug(
            "AI response generated",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "mode": ai_output.get("mode"),
                "difficulty": ai_output.get("difficulty_level"),
                "ai_message_length": len(ai_output.get("ai_message", "")),
            },
        )

        # 6. Convert AI output → ChatResponse
        chat_response = ChatResponse(
            session_id=body.session_id,
            ai_message=ai_output.get("ai_message", ""),
            ai_intent=ai_output.get("mode", "student"),  # Map mode to intent
            followups=[],
            flags=AIFlags(),
            updated_state_summary=None,
            # NEW COGNITIVE FIELDS
            mode=ai_output.get("mode", "student"),
            difficulty_level=ai_output.get("difficulty_level", 1),
            confidence_score=ai_output.get("confidence_score", 0.0),
            progress_state=ai_output.get("progress_state"),
            termination_offer=ai_output.get("termination_offer"),
        )

        # 7. Store AI response with cognitive annotations
        session = session_manager.append_turn(
            session_id=body.session_id,
            role="ai",
            text=chat_response.ai_message,
            annotations={
                "ai_intent": ai_output.get("mode"),
                "mode": ai_output.get("mode"),
                "difficulty_level": ai_output.get("difficulty_level"),
                "confidence_score": ai_output.get("confidence_score"),
                "context": normalized_context,
            },
        )
        logger.debug(
            "AI response stored",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "turn_count": len(session.conversation) + 1,
            },
        )

        # 8. Add warnings if any
        if processed.warnings:
            chat_response.updated_state_summary = "; ".join(processed.warnings)

        logger.info(
            "Chat turn completed successfully",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
            },
        )

        return ResponseEnvelope(
            success=True,
            data=chat_response,
            request_id=request_id,
        )

    except (NotFoundError, SessionExpiredError) as e:
        # Handle missing or expired sessions
        error_code = "SESSION_NOT_FOUND" if isinstance(e, NotFoundError) else "SESSION_EXPIRED"
        logger.warning(
            f"Session error: {str(e)}",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "error_code": error_code,
            },
        )
        return ResponseEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(
                code=error_code,
                message=str(e),
                details={"session_id": body.session_id},
            ),
            request_id=request_id,
        )

    except ValueError as e:
        # Handle validation errors (e.g., invalid session_id format)
        error_msg = f"Validation error: {str(e)}"
        logger.warning(
            error_msg,
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "error_type": "ValueError",
            },
        )
        return ResponseEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message=error_msg,
                details={"type": "ValueError"},
            ),
            request_id=request_id,
        )

    except KeyError as e:
        # Handle missing keys in responses or data structures
        error_msg = f"Missing required field: {str(e)}"
        logger.error(
            error_msg,
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "error_type": "KeyError",
            },
        )
        return ResponseEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(
                code="MISSING_FIELD",
                message=error_msg,
                details={"type": "KeyError"},
            ),
            request_id=request_id,
        )

    except ConnectionError as e:
        # Handle database/service connection failures
        error_msg = f"Connection failed: {str(e)}"
        logger.error(
            error_msg,
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "error_type": "ConnectionError",
            },
        )
        return ResponseEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(
                code="CONNECTION_ERROR",
                message=error_msg,
                details={"type": "ConnectionError"},
            ),
            request_id=request_id,
        )

    except Exception as e:
        # Catch-all for unexpected errors
        error_msg = f"Unexpected error: {str(e)}"
        logger.exception(
            error_msg,
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "error_type": type(e).__name__,
            },
        )
        return ResponseEnvelope(
            success=False,
            data=None,
            error=ErrorDetail(
                code="INTERNAL_ERROR",
                message=error_msg,
                details={"type": type(e).__name__},
            ),
            request_id=request_id,
        )