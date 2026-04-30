"""
Curio AI — Comprehensive Session Evaluator

LLM-driven evaluation system that analyzes full sessions and generates:
- Detailed gap reports
- Strength identification
- Misconception detection
- Learning recommendations
- Mastery assessment

Uses cognitive analysis to understand what was learned vs what needs review.
"""

from typing import List, Dict, Any, Optional
from app.services.ai_engine.llm_client import call_llm_with_system_prompt
from app.models.session_model import SessionState
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SessionEvaluator:
    """
    Comprehensive evaluator for teaching sessions using LLM analysis.
    """
    
    def __init__(self):
        self.min_understanding_score = 0.0
        self.max_understanding_score = 100.0
    
    def evaluate_session(
        self,
        session: SessionState,
    ) -> Dict[str, Any]:
        """
        Perform comprehensive LLM-driven evaluation of a session.
        """
        from app.services.ai_engine.prompt_builder import build_evaluator_mode_prompt
        from app.services.ai_engine.llm_client import call_llm
        import json
        
        # Build conversation summary for analysis
        conversation_list = [
            {"role": turn.role, "text": turn.text}
            for turn in session.conversation
        ]
        
        prompt = build_evaluator_mode_prompt(
            conversation_list,
            session.topic or "the topic"
        )
        
        # Get LLM analysis
        llm_analysis_raw = call_llm(prompt)
        
        # Try to parse JSON from the response
        try:
            # Clean response if LLM added markdown backticks
            if "```json" in llm_analysis_raw:
                llm_analysis_raw = llm_analysis_raw.split("```json")[1].split("```")[0].strip()
            elif "```" in llm_analysis_raw:
                llm_analysis_raw = llm_analysis_raw.split("```")[1].split("```")[0].strip()
            
            evaluation_json = json.loads(llm_analysis_raw)
            if not isinstance(evaluation_json, dict):
                raise ValueError("LLM response is not a JSON object")
        except Exception as e:
            logger.error(f"Failed to parse evaluation JSON: {str(e)}")
            # Fallback
            evaluation_json = {
                "strengths": ["Demonstrated interest in the topic"],
                "gaps": ["Detailed evaluation processing failed"],
                "assumptions": [],
                "struggle_moments": [],
                "recommendations": ["Continue exploring the topic systematically"],
                "mastery_score": int(session.confidence_score),
                "overall_summary": llm_analysis_raw[:500]
            }
        
        # Calculate overall understanding score
        understanding_score = float(evaluation_json.get("mastery_score", session.confidence_score))
        
        evaluation = {
            "session_id": session.session_id,
            "topic": session.topic,
            "overall_understanding_score": understanding_score,
            "confidence_level": session.confidence_score,
            "mastery_level": self._assess_mastery(understanding_score),
            "question_count": session.question_count,
            "avg_response_quality": (
                sum(session.user_response_quality_scores) / len(session.user_response_quality_scores)
                if session.user_response_quality_scores else 0.0
            ),
            "final_difficulty_reached": session.difficulty_level,
            "strengths": evaluation_json.get("strengths", []),
            "gaps": evaluation_json.get("gaps", []),
            "assumptions": evaluation_json.get("assumptions", []),
            "struggle_moments": evaluation_json.get("struggle_moments", []),
            "recommendations": evaluation_json.get("recommendations", []),
            "ai_analysis": evaluation_json.get("overall_summary", llm_analysis_raw),
        }
        
        logger.info(
            "Session evaluated",
            extra={
                "session_id": session.session_id,
                "understanding_score": understanding_score,
            }
        )
        
        return evaluation
    
    def evaluate_response(
        self,
        user_input: str,
        difficulty_level: int = 1,
    ) -> Dict[str, Any]:
        """
        Evaluate a single user response during a session.
        
        Args:
            user_input: User's response text
            difficulty_level: Current difficulty level (1, 2, or 3)
            
        Returns:
            Response evaluation with score and feedback
        """
        
        score = self._calculate_response_score(user_input, difficulty_level)
        understanding = self._classify_understanding(score)
        feedback = self._generate_response_feedback(user_input, score, difficulty_level)
        
        return {
            "score": score,
            "understanding": understanding,
            "feedback": feedback,
            "difficulty_level": difficulty_level,
        }
    
    def _build_conversation_text(self, conversation: List) -> str:
        """Build formatted conversation text for LLM analysis."""
        
        text_parts = []
        for turn in conversation:
            role = "User" if turn.role == "user" else "AI"
            text_parts.append(f"{role}: {turn.text}\n")
        
        return "".join(text_parts)
    
    def _get_llm_analysis(self, conversation: str, topic: str) -> str:
        """Get LLM analysis of the full conversation."""
        
        prompt = f"""Analyze this teaching session on {topic}:

{conversation}

Provide a detailed analysis covering:
1. What the user understands well
2. Conceptual gaps or areas of confusion
3. Misconceptions or incorrect assumptions
4. Reasoning quality and logical depth
5. Use of examples and practical understanding
6. Areas that need further review

Be specific and actionable."""
        
        try:
            analysis = call_llm_with_system_prompt(
                system_prompt="You are an expert educator analyzing student understanding.",
                user_prompt=prompt,
                max_tokens=2000
            )
            return analysis
        except Exception as exc:
            logger.error(
                "LLM analysis failed",
                extra={"error": str(exc)}
            )
            return "Unable to generate detailed analysis. Focus on foundational review."
    
    def _parse_strengths(self, analysis: str) -> List[str]:
        """Extract strength indicators from LLM analysis."""
        
        strengths = []
        analysis_lower = analysis.lower()
        
        # Parse for positive indicators
        if "clearly understands" in analysis_lower or "demonstrated strong" in analysis_lower:
            strengths.append("Clear conceptual understanding demonstrated")
        
        if "good explanation" in analysis_lower or "articulate" in analysis_lower:
            strengths.append("Can articulate concepts effectively")
        
        if "relevant examples" in analysis_lower or "practical understanding" in analysis_lower:
            strengths.append("Can apply concepts practically")
        
        if "logical reasoning" in analysis_lower or "sound logic" in analysis_lower:
            strengths.append("Demonstrates solid logical reasoning")
        
        if "comprehensive" in analysis_lower:
            strengths.append("Comprehensive topic coverage")
        
        if not strengths:
            strengths.append("Engaged meaningfully with the topic")
        
        return strengths[:5]  # Limit to top 5
    
    def _parse_gaps(self, analysis: str) -> List[Dict[str, str]]:
        """Extract learning gaps from LLM analysis."""
        
        gaps = []
        analysis_lower = analysis.lower()
        
        # Parse for gap indicators
        if "confusion" in analysis_lower or "unclear" in analysis_lower:
            gaps.append({
                "area": "Conceptual clarity",
                "issue": "Some concepts need further clarification",
                "priority": "medium"
            })
        
        if "edge case" in analysis_lower or "boundary" in analysis_lower:
            gaps.append({
                "area": "Edge cases and special scenarios",
                "issue": "Limited exploration of boundary conditions",
                "priority": "high"
            })
        
        if "example" in analysis_lower and "missing" in analysis_lower:
            gaps.append({
                "area": "Practical examples",
                "issue": "Few concrete examples provided",
                "priority": "medium"
            })
        
        if "assumption" in analysis_lower or "not questioned" in analysis_lower:
            gaps.append({
                "area": "Critical thinking",
                "issue": "Assumptions not thoroughly questioned",
                "priority": "medium"
            })
        
        if "depth" in analysis_lower and ("lack" in analysis_lower or "limited" in analysis_lower):
            gaps.append({
                "area": "Conceptual depth",
                "issue": "Deeper understanding needed",
                "priority": "medium"
            })
        
        return gaps[:5]  # Limit to top 5
    
    def _parse_misconceptions(self, analysis: str) -> List[Dict[str, str]]:
        """Extract misconceptions from LLM analysis."""
        
        misconceptions = []
        analysis_lower = analysis.lower()
        
        if "misconception" in analysis_lower or "incorrect" in analysis_lower or "wrong" in analysis_lower:
            misconceptions.append({
                "issue": "One or more conceptual misconceptions detected",
                "severity": "high",
                "action": "Review core concepts carefully"
            })
        
        if "oversimplif" in analysis_lower:
            misconceptions.append({
                "issue": "Topic oversimplified, missing nuances",
                "severity": "medium",
                "action": "Explore more complex scenarios"
            })
        
        if "assumption" in analysis_lower and ("flawed" in analysis_lower or "false" in analysis_lower):
            misconceptions.append({
                "issue": "Flawed assumptions about the topic",
                "severity": "high",
                "action": "Challenge and revise core assumptions"
            })
        
        return misconceptions[:3]  # Limit to top 3
    
    def _calculate_understanding_score(
        self,
        response_scores: List[float],
        gap_count: int,
        strength_count: int,
    ) -> float:
        """
        Calculate overall understanding score (0-100).
        
        Args:
            response_scores: List of individual response quality scores
            gap_count: Number of identified gaps
            strength_count: Number of identified strengths
            
        Returns:
            Overall score (0-100)
        """
        
        if not response_scores:
            return 0.0
        
        # Base score from response quality
        base_score = (sum(response_scores) / len(response_scores)) * 100.0
        
        # Adjust for gaps (each gap reduces score)
        gap_penalty = min(20, gap_count * 3)
        
        # Boost for strengths (each strength adds to score)
        strength_bonus = min(15, strength_count * 2)
        
        final_score = base_score - gap_penalty + strength_bonus
        
        # Clamp to 0-100
        return max(0.0, min(100.0, final_score))
    
    def _assess_mastery(self, understanding_score: float) -> str:
        """
        Assess mastery level based on understanding score.
        
        Args:
            understanding_score: Score 0-100
            
        Returns:
            Mastery level: Beginner, Developing, Proficient, or Mastery
        """
        
        if understanding_score >= 85:
            return "Mastery"
        elif understanding_score >= 70:
            return "Proficient"
        elif understanding_score >= 50:
            return "Developing"
        else:
            return "Beginner"
    
    def _calculate_response_score(self, response: str, difficulty_level: int) -> float:
        """
        Calculate quality score for a single response (0-1 scale).
        
        Args:
            response: User's response text
            difficulty_level: Current difficulty level
            
        Returns:
            Score 0-1
        """
        
        score = 0.5  # Baseline
        words = response.split()
        
        # Length scoring
        word_count = len(words)
        if word_count < 5:
            score -= 0.2
        elif word_count < 15:
            score -= 0.05
        elif word_count > 50:
            score += 0.15
        
        # Reasoning indicators
        reasoning_words = ["because", "since", "therefore", "thus", "so that"]
        if any(word in response.lower() for word in reasoning_words):
            score += 0.15
        
        # Examples
        if any(word in response.lower() for word in ["example", "like", "such as"]):
            score += 0.15
        
        # Difficulty-specific scoring
        if difficulty_level >= 2:
            # Check for nuanced thinking
            nuance_words = ["however", "although", "while", "but", "depends"]
            if any(word in response.lower() for word in nuance_words):
                score += 0.1
        
        if difficulty_level >= 3:
            # Check for edge case awareness
            if any(word in response.lower() for word in ["edge case", "boundary", "exception", "special"]):
                score += 0.1
        
        return max(0.0, min(1.0, score))
    
    def _classify_understanding(self, score: float) -> str:
        """Classify understanding level based on score."""
        
        if score >= 0.75:
            return "Strong"
        elif score >= 0.50:
            return "Moderate"
        else:
            return "Weak"
    
    def _generate_response_feedback(
        self,
        response: str,
        score: float,
        difficulty_level: int,
    ) -> List[str]:
        """Generate specific feedback for a response."""
        
        feedback = []
        response_lower = response.lower()
        
        # Length feedback
        word_count = len(response.split())
        if word_count < 10 and difficulty_level >= 2:
            feedback.append("Expand your response with more detail")
        
        # Reasoning feedback
        reasoning_words = ["because", "since", "therefore"]
        if not any(word in response_lower for word in reasoning_words):
            if score < 0.6:
                feedback.append("Include reasoning: explain the 'why' behind your answer")
        
        # Example feedback
        if "example" not in response_lower and difficulty_level >= 2 and score < 0.7:
            feedback.append("Add an example or concrete case to support your point")
        
        # Nuance feedback (for higher difficulties)
        if difficulty_level >= 2:
            nuance_words = ["however", "depends", "but", "although"]
            if not any(word in response_lower for word in nuance_words) and score < 0.65:
                feedback.append("Consider nuances or conditions where your answer might vary")
        
        # Edge case feedback (for expert level)
        if difficulty_level >= 3 and score < 0.7:
            if "edge" not in response_lower and "boundary" not in response_lower:
                feedback.append("Think about edge cases and boundary conditions")
        
        if not feedback:
            if score >= 0.75:
                feedback.append("Good response! Keep building on this.")
            elif score >= 0.50:
                feedback.append("Solid start. Add more depth or specificity.")
        
        return feedback
    
    def _generate_recommendations(
        self,
        gaps: List[Dict],
        misconceptions: List[Dict],
        understanding_score: float,
        difficulty_level: int,
    ) -> List[str]:
        """Generate learning recommendations."""
        
        recommendations = []
        
        # Handle misconceptions first
        if misconceptions:
            recommendations.append("Priority: Review and correct identified misconceptions")
        
        # Gap-based recommendations
        if gaps:
            gap_areas = [gap.get("area", "") for gap in gaps[:3]]
            if gap_areas:
                recommendations.append(f"Review these areas: {', '.join(gap_areas)}")
        
        # Performance-based recommendations
        if understanding_score < 50:
            recommendations.append("Build foundational understanding before advancing complexity")
        elif understanding_score < 70:
            recommendations.append("Consolidate understanding through targeted practice")
        elif understanding_score >= 85:
            if difficulty_level < 3:
                recommendations.append("You're ready for more advanced challenges")
            else:
                recommendations.append("Excellent mastery! Consider teaching others to deepen understanding")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Continue practicing with diverse examples")
        
        return recommendations


# Singleton instance
evaluator = SessionEvaluator()
