"""
Curio AI — Evaluate Route.

POST /evaluate — Evaluate the user's teaching performance in a session.
Uses the comprehensive LLM-driven evaluator for detailed gap analysis.
"""

from fastapi import APIRouter, Request

from app.models.chat_model import ResponseEnvelope
from app.models.evaluation_model import EvaluationRequest
from app.services.ai_service import generate_session_evaluation
from app.services.session_manager import session_manager
from app.services.report_generator import generate_report
from app.utils.helpers import generate_id, utc_now
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(tags=["Evaluation"])


@router.post("/evaluate", response_model=ResponseEnvelope)
async def evaluate(body: EvaluationRequest, request: Request):
    """
    Evaluate the user's teaching performance.

    Flow:
    1. Get session state
    2. Run comprehensive LLM-driven evaluation
    3. Generate detailed gap report
    4. Store evaluation result in session
    5. Return evaluation response with recommendations
    """
    request_id = request.headers.get("X-Request-ID") or generate_id("req")

    try:
        logger.debug(
            "Evaluation requested",
            extra={"request_id": request_id, "session_id": body.session_id}
        )
        
        # 1. Get session
        session = session_manager.get_session(body.session_id)
        
        # 2. Run comprehensive evaluation
        evaluation = generate_session_evaluation(session)
        
        # 3. Generate detailed report
        report = generate_report(session, evaluation)
        
        # 4. Persistence: Store the report in the reports collection
        # Add necessary metadata for the dashboard to find it
        report_storage_data = {
            **report,
            "user_id": session.user_id,
            "topic": session.topic,
            "generated_at": utc_now().isoformat(),
            "understanding_score": evaluation.get("overall_understanding_score", 0),
            "mastery_level": evaluation.get("mastery_level", "Unknown")
        }
        session_manager.store_report(report_storage_data)
        
        # 5. Store evaluation result in session
        session_manager.update_last_evaluation(
            session_id=body.session_id,
            evaluation_result=evaluation,
        )
        
        logger.info(
            "Session evaluated successfully",
            extra={
                "request_id": request_id,
                "session_id": body.session_id,
                "understanding_score": evaluation.get("overall_understanding_score"),
                "mastery_level": evaluation.get("mastery_level"),
            }
        )
        
        # 5. Return comprehensive evaluation response
        return ResponseEnvelope(
            success=True,
            data={
                "session_id": body.session_id,
                "evaluation": evaluation,
                "report": report,
            },
            request_id=request_id,
        )
        
    except Exception as exc:
        logger.error(
            "Evaluation failed",
            extra={"request_id": request_id, "error": str(exc)}
        )
        return ResponseEnvelope(
            success=False,
            data=None,
            error={
                "code": "EVALUATION_ERROR",
                "message": f"Failed to evaluate session: {str(exc)}",
            },
            request_id=request_id,
        )
