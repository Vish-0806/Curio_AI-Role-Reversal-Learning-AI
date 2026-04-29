"""
Curio AI — Adaptive Cognitive Mode Controller

Core engine managing:
- Mode switching (student → teacher → rescue → evaluator)
- Difficulty progression (beginner → intermediate → expert)
- Response analysis and quality scoring
- Confidence-based session termination recommendations
- Dynamic mistake injection
- Conversational continuity

This is the brain of the Curio cognitive learning system.
"""

from typing import Dict, List, Tuple, Optional, Any
import json

from app.services.ai_engine.prompt_builder import (
    build_student_mode_prompt,
    build_teacher_mode_prompt,
    build_rescue_mode_prompt,
    build_evaluator_mode_prompt,
)
from app.services.ai_engine.llm_client import call_llm_with_system_prompt, call_llm
from app.services.ai_engine.mistake_injection import inject_mistake_llm
from app.services.ai_engine.difficulty_engine import DifficultyProgressionEngine
from app.models.session_model import SessionState, ConversationTurn
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AdaptiveCognitiveController:
    """
    Main cognitive system controller for Curio AI.
    Manages mode switching, difficulty progression, and response generation.
    """
    
    def __init__(self):
        self.difficulty_engine = DifficultyProgressionEngine()
        self.mode_switch_history = []
        
        # Configuration
        self.HIGH_CONFIDENCE_THRESHOLD = 75.0  # Offer termination at this confidence
        self.MISTAKE_INJECTION_PROBABILITY = 0.15  # 15% chance of mistake injection per turn
        self.TEACHER_MODE_TRIGGER_THRESHOLD = 0.35  # If user score below this, offer teacher mode
        self.RESCUE_MODE_TRIGGER_THRESHOLD = 0.50   # If user score between this and 0.65, offer rescue
    
    def analyze_user_response(
        self,
        response_text: str,
        ai_difficulty_level: int,
    ) -> Dict[str, Any]:
        """
        Analyze user response quality and determine next system action.
        
        Args:
            response_text: The user's response to an AI question
            ai_difficulty_level: Current difficulty level (1, 2, or 3)
            
        Returns:
            Dictionary with analysis results including quality score and recommendations
        """
        
        # Calculate response quality
        quality_score = self.difficulty_engine.analyze_response_quality(
            response_text,
            ai_difficulty_level
        )
        
        analysis = {
            "response_quality_score": quality_score,
            "difficulty_level": ai_difficulty_level,
            "suggested_mode": "student",  # Default
            "confidence_assessment": self._assess_confidence(quality_score),
            "reasoning": ""
        }
        
        # Determine if mode switch is needed
        if quality_score < self.TEACHER_MODE_TRIGGER_THRESHOLD:
            analysis["suggested_mode"] = "teacher"
            analysis["reasoning"] = "User appears stuck - switching to teacher mode for clarification"
        elif quality_score < self.RESCUE_MODE_TRIGGER_THRESHOLD:
            analysis["suggested_mode"] = "rescue"
            analysis["reasoning"] = "User is partially stuck - switching to rescue mode for hints"
        
        return analysis
    
    def _assess_confidence(self, quality_score: float) -> float:
        """
        Convert response quality to confidence metric (0-100).
        
        Args:
            quality_score: Quality score (0-1 scale)
            
        Returns:
            Confidence (0-100 scale)
        """
        return quality_score * 100.0
    
    def generate_adaptive_response(
        self,
        session: SessionState,
        user_input: str,
        force_mode: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate an adaptive AI response based on session state and user input.
        
        This is the main entry point for generating all AI responses.
        It handles mode switching, difficulty progression, and all AI behaviors.
        
        Args:
            session: Current session state
            user_input: User's message
            force_mode: Optional mode override (for testing/control)
            
        Returns:
            Response dict with structured data for frontend
        """
        
        # Extract conversation history for context
        conversation_list = [
            {"role": turn.role, "text": turn.text}
            for turn in session.conversation[-5:]  # Last 5 turns
        ]
        
        # Analyze current user response
        analysis = self.analyze_user_response(user_input, session.difficulty_level)
        
        # Determine current mode
        current_mode = force_mode or session.current_mode
        suggested_mode = analysis.get("suggested_mode", "student")
        
        # Check if we should switch modes
        if suggested_mode != current_mode and suggested_mode != "student":
            current_mode = suggested_mode
            session.current_mode = current_mode
            session.mode_switch_history.append({
                "timestamp": str(session.created_at),
                "from_mode": session.current_mode,
                "to_mode": current_mode,
                "reason": analysis.get("reasoning", "")
            })
        
        # Update session tracking
        session.user_response_quality_scores.append(analysis["response_quality_score"])
        session.confidence_score = analysis["confidence_assessment"]
        session.question_count += 1
        
        # Generate AI response based on current mode
        if current_mode == "student":
            ai_response = self._generate_student_mode_response(
                session, user_input, conversation_list
            )
        elif current_mode == "teacher":
            ai_response = self._generate_teacher_mode_response(
                session, user_input, conversation_list
            )
        elif current_mode == "rescue":
            ai_response = self._generate_rescue_mode_response(
                session, user_input, conversation_list
            )
        else:
            ai_response = self._generate_student_mode_response(
                session, user_input, conversation_list
            )
        
        # Check for difficulty progression
        avg_performance = self.difficulty_engine.calculate_average_performance(
            session.user_response_quality_scores
        )
        new_difficulty, difficulty_reason = self.difficulty_engine.get_next_difficulty_level(
            session.difficulty_level,
            avg_performance,
            len(session.user_response_quality_scores)
        )
        
        if new_difficulty != session.difficulty_level:
            session.difficulty_level = new_difficulty
            logger.info(
                "Difficulty level changed",
                extra={
                    "session_id": session.session_id,
                    "old_level": session.difficulty_level,
                    "new_level": new_difficulty,
                    "reason": difficulty_reason,
                }
            )
        
        # Build response envelope
        response = {
            "mode": current_mode,
            "difficulty_level": session.difficulty_level,
            "ai_message": ai_response,
            "confidence_score": session.confidence_score,
            "progress_state": {
                "question_count": session.question_count,
                "avg_response_quality": avg_performance,
                "topic": session.topic,
            },
            "session_summary": None,
        }
        
        # Check if we should offer session termination based on confidence
        if session.confidence_score >= self.HIGH_CONFIDENCE_THRESHOLD:
            response["termination_offer"] = {
                "suggested": True,
                "message": f"Your understanding seems strong ({session.confidence_score:.0f}%)! "
                          "Would you like to continue with harder challenges or end the session?",
            }
        
        return response
    
    def _generate_student_mode_response(
        self,
        session: SessionState,
        user_input: str,
        conversation_history: List[dict],
    ) -> str:
        """Generate a student-mode question response."""
        
        # Decide if this should be a mistake injection instead of a question
        import random
        if random.random() < self.MISTAKE_INJECTION_PROBABILITY:
            # Inject a mistake for mastery validation
            user_explanations = [
                turn["text"] for turn in conversation_history
                if turn["role"] == "user"
            ]
            mistake = inject_mistake_llm(
                user_explanations,
                session.topic or "the topic",
                session.difficulty_level
            )
            logger.debug(
                "Mistake injected for mastery validation",
                extra={"session_id": session.session_id}
            )
            return mistake
        
        # Generate regular student-mode question
        prompt = build_student_mode_prompt(
            user_input,
            session.topic or "the topic",
            session.difficulty_level,
            conversation_history
        )
        
        response = call_llm_with_system_prompt(
            system_prompt="",
            user_prompt=prompt,
            max_tokens=500
        )
        
        return response
    
    def _generate_teacher_mode_response(
        self,
        session: SessionState,
        user_input: str,
        conversation_history: List[dict],
    ) -> str:
        """Generate a teacher-mode clarification response."""
        
        user_explanations = [
            turn["text"] for turn in conversation_history
            if turn["role"] == "user"
        ]
        
        prompt = build_teacher_mode_prompt(
            user_input,
            session.topic or "the topic",
            user_explanations
        )
        
        response = call_llm_with_system_prompt(
            system_prompt="",
            user_prompt=prompt,
            max_tokens=600
        )
        
        return response
    
    def _generate_rescue_mode_response(
        self,
        session: SessionState,
        user_input: str,
        conversation_history: List[dict],
    ) -> str:
        """Generate a rescue-mode hint response."""
        
        prompt = build_rescue_mode_prompt(
            user_input,
            session.topic or "the topic",
            session.difficulty_level
        )
        
        response = call_llm_with_system_prompt(
            system_prompt="",
            user_prompt=prompt,
            max_tokens=400
        )
        
        return response
    
    def generate_session_evaluation(
        self,
        session: SessionState,
    ) -> Dict[str, Any]:
        """
        Generate comprehensive session evaluation (EVALUATOR MODE).
        
        Args:
            session: Completed session state
            
        Returns:
            Evaluation report dictionary
        """
        
        # Build conversation history for analysis
        conversation_list = [
            {"role": turn.role, "text": turn.text}
            for turn in session.conversation
        ]
        
        prompt = build_evaluator_mode_prompt(
            conversation_list,
            session.topic or "the topic"
        )
        
        # Call LLM for comprehensive evaluation
        evaluation_response = call_llm(prompt)
        
        # Calculate session statistics
        avg_response_quality = (
            sum(session.user_response_quality_scores) / len(session.user_response_quality_scores)
            if session.user_response_quality_scores else 0.5
        )
        
        evaluation = {
            "session_id": session.session_id,
            "topic": session.topic,
            "overall_confidence": session.confidence_score,
            "average_response_quality": avg_response_quality,
            "total_turns": len(session.conversation),
            "final_difficulty_level": session.difficulty_level,
            "ai_evaluation": evaluation_response,
            "strengths": self._extract_strengths(evaluation_response),
            "gaps": self._extract_gaps(evaluation_response),
            "recommendations": self._extract_recommendations(evaluation_response),
        }
        
        return evaluation
    
    def _extract_strengths(self, evaluation_text: str) -> List[str]:
        """Extract strengths from evaluation text."""
        strengths = []
        # Simple heuristic: look for positive keywords
        if "strong" in evaluation_text.lower():
            strengths.append("Demonstrated strong conceptual understanding")
        if "clear" in evaluation_text.lower():
            strengths.append("Provided clear explanations")
        if "example" in evaluation_text.lower():
            strengths.append("Supported points with relevant examples")
        return strengths if strengths else ["Engaged actively in learning"]
    
    def _extract_gaps(self, evaluation_text: str) -> List[str]:
        """Extract learning gaps from evaluation text."""
        gaps = []
        # Simple heuristic: look for weakness keywords
        if "unclear" in evaluation_text.lower() or "confusion" in evaluation_text.lower():
            gaps.append("Some concepts need clarification")
        if "missing" in evaluation_text.lower():
            gaps.append("Some key concepts were not fully explored")
        if "edge case" in evaluation_text.lower():
            gaps.append("Edge cases and special scenarios need review")
        return gaps if gaps else ["Continue practicing and exploring"]
    
    def _extract_recommendations(self, evaluation_text: str) -> List[str]:
        """Extract recommendations from evaluation text."""
        recommendations = []
        if "practice" in evaluation_text.lower():
            recommendations.append("Practice with more complex scenarios")
        if "review" in evaluation_text.lower():
            recommendations.append("Review fundamental concepts")
        if "deeper" in evaluation_text.lower():
            recommendations.append("Explore the topic more deeply")
        return recommendations if recommendations else ["Build on current understanding with more topics"]


# Singleton instance
adaptive_controller = AdaptiveCognitiveController()
