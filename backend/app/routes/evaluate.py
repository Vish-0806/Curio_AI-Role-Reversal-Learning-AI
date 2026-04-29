"""
Curio AI — Evaluate Route.

POST /evaluate — Evaluate the user's teaching performance in a session.
"""

from fastapi import APIRouter, Request

from app.models.chat_model import ResponseEnvelope
from app.models.evaluation_model import EvaluationRequest, EvaluationResponse
from app.services.evaluation_router import evaluate_session
from app.services.session_manager import session_manager
from app.utils.helpers import generate_id

router = APIRouter(tags=["Evaluation"])


@router.post("/evaluate", response_model=ResponseEnvelope[EvaluationResponse])
async def evaluate(body: EvaluationRequest, request: Request):
    """
    Evaluate the user's teaching performance.

    Flow:
    1. Get session state
    2. Run evaluation engine
    3. Store evaluation result in session
    4. Return evaluation response
    """
    request_id = request.headers.get("X-Request-ID") or generate_id("req")

    # 1. Get session
    session = session_manager.get_session(body.session_id)

    # 2. Evaluate
    result = evaluate_session(session, rubric=body.rubric)

    # 3. Store in session
    session_manager.update_last_evaluation(
        session_id=body.session_id,
        evaluation_result=result.model_dump(),
    )

    # 4. Return response
    return ResponseEnvelope(
        success=True,
        data=EvaluationResponse(
            session_id=body.session_id,
            evaluation=result,
        ),
        request_id=request_id,
    )
