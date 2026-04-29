"""
Curio AI — Report Route.

POST /report — Generate a learning gap report for a session.
"""

from fastapi import APIRouter, Request

from app.models.chat_model import ResponseEnvelope
from app.models.evaluation_model import EvaluationResult
from app.models.report_model import ReportRequest, ReportResponse
from app.services.report_generator import generate_report
from app.services.session_manager import session_manager
from app.utils.error_handler import CurioValidationError
from app.utils.helpers import generate_id

router = APIRouter(tags=["Report"])


@router.post("/report", response_model=ResponseEnvelope[ReportResponse])
async def report(body: ReportRequest, request: Request):
    """
    Generate a learning report for the session.

    Requires that evaluation has been run first (POST /evaluate).

    Flow:
    1. Get session state
    2. Check evaluation exists
    3. Generate report from evaluation
    4. Return report response
    """
    request_id = request.headers.get("X-Request-ID") or generate_id("req")

    # 1. Get session
    session = session_manager.get_session(body.session_id)

    # 2. Check evaluation exists
    if not session.last_evaluation:
        raise CurioValidationError(
            message="No evaluation found. Run POST /api/evaluate first.",
            details={"session_id": body.session_id},
        )

    # 3. Reconstruct EvaluationResult from stored dict
    evaluation = EvaluationResult(**session.last_evaluation)

    # 4. Generate report
    learning_report = generate_report(session, evaluation)

    return ResponseEnvelope(
        success=True,
        data=ReportResponse(
            session_id=body.session_id,
            report=learning_report,
        ),
        request_id=request_id,
    )
