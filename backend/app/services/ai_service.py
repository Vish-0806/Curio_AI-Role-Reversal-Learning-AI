"""
Curio AI — AI Service

Main interface for AI response generation.
Integrates the adaptive cognitive controller with session management.
"""

from typing import Dict, Any, Optional
from app.services.ai_engine.ai_logic import adaptive_controller
from app.services.ai_engine.evaluator import evaluator
from app.models.session_model import SessionState
from app.utils.logger import get_logger

logger = get_logger(__name__)


def get_ai_response(
    session: SessionState,
    user_input: str,
    force_mode: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate an adaptive AI response for the user.
    
    This is the main entry point for all AI responses during a session.
    
    Args:
        session: Current SessionState with full context
        user_input: User's latest message
        force_mode: Optional mode override for testing
        
    Returns:
        Structured response dictionary with:
        - mode: Current AI mode
        - difficulty_level: Current difficulty
        - ai_message: The AI's response
        - confidence_score: System's confidence
        - progress_state: Session progress
        - termination_offer: Optional offer to end session
    """
    
    try:
        # Generate adaptive response using cognitive controller
        response = adaptive_controller.generate_adaptive_response(
            session,
            user_input,
            force_mode
        )
        
        logger.debug(
            "AI response generated",
            extra={
                "session_id": session.session_id,
                "mode": response.get("mode"),
                "difficulty": response.get("difficulty_level"),
                "confidence": response.get("confidence_score"),
            }
        )
        
        return response
        
    except Exception as exc:
        logger.error(
            "Error generating AI response",
            extra={"error": str(exc), "session_id": session.session_id}
        )
        
        # Return safe fallback response
        return {
            "mode": "student",
            "difficulty_level": 1,
            "ai_message": "I encountered an issue. Could you rephrase your explanation?",
            "confidence_score": 0.0,
            "progress_state": {
                "question_count": session.question_count,
                "avg_response_quality": 0.0,
                "topic": session.topic,
            },
            "error": str(exc),
        }


def evaluate_user_response(
    user_input: str,
    difficulty_level: int = 1,
) -> Dict[str, Any]:
    """
    Evaluate a single user response (for detailed feedback).
    
    Args:
        user_input: User's response text
        difficulty_level: Current difficulty level (1, 2, or 3)
        
    Returns:
        Evaluation dict with score and feedback
    """
    
    return evaluator.evaluate_response(user_input, difficulty_level)


def generate_session_evaluation(session: SessionState) -> Dict[str, Any]:
    """
    Generate comprehensive evaluation for session completion.
    
    Args:
        session: Completed SessionState
        
    Returns:
        Full evaluation report
    """
    
    try:
        evaluation = evaluator.evaluate_session(session)
        
        logger.info(
            "Session evaluation completed",
            extra={
                "session_id": session.session_id,
                "understanding_score": evaluation.get("overall_understanding_score"),
            }
        )
        
        return evaluation
        
    except Exception as exc:
        logger.error(
            "Error evaluating session",
            extra={"error": str(exc), "session_id": session.session_id}
        )
        
        return {
            "session_id": session.session_id,
            "error": str(exc),
            "fallback": True,
        }
