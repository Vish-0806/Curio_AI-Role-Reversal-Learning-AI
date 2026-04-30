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
        stuck_phrases = ["don't know", "dont know", "not sure", "no idea", "stuck", "explain", "describe", "what is", "how does", "help me"]
        ready_phrases = ["i'll explain", "i will explain", "i understand", "i got it", "let me explain", "i'll try", "ill try"]
        
        is_user_stuck = any(phrase in response_text.lower() for phrase in stuck_phrases)
        is_user_ready = any(phrase in response_text.lower() for phrase in ready_phrases)

        # STRICT KEYWORD-BASED SWITCHING
        if is_user_stuck:
            analysis["suggested_mode"] = "teacher"
            analysis["reasoning"] = "User used a 'stuck' keyword - switching to teacher mode"
        elif is_user_ready:
            analysis["suggested_mode"] = "student"
            analysis["reasoning"] = "User used a 'ready' keyword - switching back to student mode"
        else:
            # If no keywords, STAY in the current mode (don't suggest a switch)
            analysis["suggested_mode"] = None 
            analysis["reasoning"] = "No mode switch keywords detected"
        
        return analysis
    
    def _assess_confidence(self, quality_score: float) -> float:
        """Convert response quality to confidence metric (0-100)."""
        return quality_score * 100.0
    
    def generate_adaptive_response(
        self,
        session: SessionState,
        user_input: str,
        force_mode: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate an adaptive AI response based on session state and user input.
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
        suggested_mode = analysis.get("suggested_mode")
        
        # Check if we should switch modes
        if suggested_mode and suggested_mode != current_mode:
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
        }
        
        # Check if we should offer session termination
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
        import random
        if random.random() < self.MISTAKE_INJECTION_PROBABILITY:
            user_explanations = [
                turn["text"] for turn in conversation_history
                if turn["role"] == "user"
            ]
            mistake = inject_mistake_llm(
                user_explanations,
                session.topic or "the topic",
                session.difficulty_level
            )
            return mistake
        
        prompt = build_student_mode_prompt(
            user_input,
            session.topic or "the topic",
            session.difficulty_level,
            conversation_history
        )
        return call_llm(prompt)
    
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
        
        # Find the last question asked by the AI to provide context
        last_ai_question = None
        for turn in reversed(conversation_history):
            if turn["role"] == "ai":
                last_ai_question = turn["text"]
                break
        
        prompt = build_teacher_mode_prompt(
            user_input,
            session.topic or "the topic",
            user_explanations,
            last_ai_question=last_ai_question
        )
        return call_llm(prompt)
    
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
        return call_llm(prompt)
    
    def generate_session_evaluation(
        self,
        session: SessionState,
    ) -> Dict[str, Any]:
        """Generate comprehensive session evaluation (EVALUATOR MODE)."""
        conversation_list = [
            {"role": turn.role, "text": turn.text}
            for turn in session.conversation
        ]
        prompt = build_evaluator_mode_prompt(
            conversation_list,
            session.topic or "the topic"
        )
        
        evaluation_raw = call_llm(prompt)
        
        try:
            if "```json" in evaluation_raw:
                evaluation_raw = evaluation_raw.split("```json")[1].split("```")[0].strip()
            elif "```" in evaluation_raw:
                evaluation_raw = evaluation_raw.split("```")[1].split("```")[0].strip()
            
            evaluation_json = json.loads(evaluation_raw)
            if not isinstance(evaluation_json, dict):
                raise ValueError("LLM response is not a JSON object")
        except Exception as e:
            logger.error(f"Failed to parse evaluation JSON: {str(e)}")
            evaluation_json = {
                "strengths": ["Completed the session"],
                "gaps": ["Evaluation processing failed"],
                "assumptions": [],
                "struggle_moments": [],
                "recommendations": ["Review the topic once more"],
                "mastery_score": int(session.confidence_score),
                "overall_summary": evaluation_raw[:500]
            }
        
        avg_performance = (
            sum(session.user_response_quality_scores) / len(session.user_response_quality_scores)
            if session.user_response_quality_scores else 0.5
        )
        
        return {
            "session_id": session.session_id,
            "topic": session.topic,
            "overall_confidence": evaluation_json.get("mastery_score", session.confidence_score),
            "average_response_quality": avg_performance,
            "total_turns": len(session.conversation),
            "final_difficulty_level": session.difficulty_level,
            "ai_evaluation": evaluation_json.get("overall_summary"),
            "strengths": evaluation_json.get("strengths", []),
            "gaps": evaluation_json.get("gaps", []),
            "assumptions": evaluation_json.get("assumptions", []),
            "struggle_moments": evaluation_json.get("struggle_moments", []),
            "recommendations": evaluation_json.get("recommendations", []),
        }


adaptive_controller = AdaptiveCognitiveController()
