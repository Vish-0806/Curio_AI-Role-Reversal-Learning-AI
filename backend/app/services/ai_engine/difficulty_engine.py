"""
Curio AI — Adaptive Difficulty Progression Engine

Analyzes user response quality and automatically manages difficulty progression:
- LEVEL 1 (Beginner): Simple, confidence-building questions
- LEVEL 2 (Intermediate): More analytical, "why" questions, real-world application
- LEVEL 3 (Expert): Skepticism, edge cases, deep logical attacks

Progression is automatic based on:
- User response quality scores
- Confidence metrics
- Number of successful responses at each level
- Pattern of understanding vs confusion
"""

from typing import Tuple, List


class DifficultyProgressionEngine:
    """
    Manages adaptive difficulty progression based on user performance.
    """
    
    # Configuration for progression thresholds
    PROGRESS_TO_INTERMEDIATE_THRESHOLD = 0.75  # User score needed to progress
    PROGRESS_TO_EXPERT_THRESHOLD = 0.80
    REGRESS_THRESHOLD = 0.45  # Score below this triggers regression
    BEGINNER_FLOOR = 0.50  # Minimum score at level 1 before regression
    
    # Number of successful responses needed at each level before progressing
    MIN_RESPONSES_AT_LEVEL = 2
    
    def __init__(self):
        self.responses_at_current_level = 0
        self.consecutive_weak_responses = 0
        self.max_consecutive_weak = 2
    
    def analyze_response_quality(
        self,
        response_text: str,
        ai_difficulty_level: int,
    ) -> float:
        """
        Score user's response quality (0-1 scale).
        
        Args:
            response_text: User's response to AI question
            ai_difficulty_level: Current difficulty level (1, 2, or 3)
            
        Returns:
            Quality score (0-1 scale)
        """
        
        score = 0.5  # Baseline
        
        # Check length (longer, more detailed responses typically score higher)
        word_count = len(response_text.split())
        if word_count < 10:
            score -= 0.15  # Too brief
        elif word_count > 20:
            score += 0.1   # Good detail
        elif word_count > 50:
            score += 0.15  # Excellent detail
        
        # Check for reasoning indicators (higher weight for higher difficulties)
        reasoning_words = ["because", "therefore", "since", "thus", "so that", "as a result"]
        if any(word in response_text.lower() for word in reasoning_words):
            score += 0.15
        
        # Check for examples
        example_indicators = ["example", "like", "such as", "for instance", "e.g.", "instance"]
        if any(word in response_text.lower() for word in example_indicators):
            score += 0.15
        
        # Check for defense/justification (especially important for higher difficulties)
        if ai_difficulty_level >= 2:
            defense_words = ["because", "however", "but", "although", "while", "yet"]
            if any(word in response_text.lower() for word in defense_words):
                score += 0.1
        
        # Penalty for uncertainty or "I don't know" at higher difficulties
        if ai_difficulty_level >= 2:
            doubt_words = ["i don't know", "not sure", "unsure", "confused"]
            if any(word in response_text.lower() for word in doubt_words):
                score -= 0.2
        
        # Clamp score to 0-1
        return max(0.0, min(1.0, score))
    
    def calculate_average_performance(
        self,
        recent_scores: List[float],
        window_size: int = 5,
    ) -> float:
        """
        Calculate average user performance over recent responses.
        
        Args:
            recent_scores: List of recent response quality scores
            window_size: Number of recent responses to consider
            
        Returns:
            Average performance (0-1 scale)
        """
        if not recent_scores:
            return 0.5
        
        # Use only the most recent responses
        relevant_scores = recent_scores[-window_size:] if len(recent_scores) >= window_size else recent_scores
        
        if not relevant_scores:
            return 0.5
        
        return sum(relevant_scores) / len(relevant_scores)
    
    def should_progress_difficulty(
        self,
        current_difficulty: int,
        average_performance: float,
        responses_at_level: int,
    ) -> bool:
        """
        Determine if user should progress to next difficulty level.
        
        Args:
            current_difficulty: Current level (1, 2, or 3)
            average_performance: Average user performance (0-1)
            responses_at_level: Number of responses at current level
            
        Returns:
            True if should progress
        """
        
        # Can't progress beyond expert
        if current_difficulty >= 3:
            return False
        
        # Need minimum responses at current level
        if responses_at_level < self.MIN_RESPONSES_AT_LEVEL:
            return False
        
        # Check performance threshold based on current level
        if current_difficulty == 1:
            return average_performance >= self.PROGRESS_TO_INTERMEDIATE_THRESHOLD
        elif current_difficulty == 2:
            return average_performance >= self.PROGRESS_TO_EXPERT_THRESHOLD
        
        return False
    
    def should_regress_difficulty(
        self,
        current_difficulty: int,
        average_performance: float,
    ) -> bool:
        """
        Determine if user should regress to easier difficulty.
        
        Args:
            current_difficulty: Current level (1, 2, or 3)
            average_performance: Average user performance (0-1)
            
        Returns:
            True if should regress
        """
        
        # Can't go below beginner
        if current_difficulty <= 1:
            return False
        
        # Don't regress from beginner immediately
        if current_difficulty == 1 and average_performance > self.BEGINNER_FLOOR:
            return False
        
        # Regress if performance drops below threshold
        return average_performance < self.REGRESS_THRESHOLD
    
    def get_next_difficulty_level(
        self,
        current_difficulty: int,
        average_performance: float,
        responses_at_level: int,
    ) -> Tuple[int, str]:
        """
        Determine the next difficulty level and reason.
        
        Args:
            current_difficulty: Current level (1, 2, or 3)
            average_performance: Average user performance (0-1)
            responses_at_level: Number of responses at current level
            
        Returns:
            Tuple of (new_difficulty_level, reason_for_change)
        """
        
        reason = ""
        new_level = current_difficulty
        
        # Check for progression first
        if self.should_progress_difficulty(current_difficulty, average_performance, responses_at_level):
            new_level = current_difficulty + 1
            reason = f"Strong performance ({average_performance:.0%}) - progressing to level {new_level}"
        
        # Check for regression
        elif self.should_regress_difficulty(current_difficulty, average_performance):
            new_level = current_difficulty - 1
            reason = f"Performance needs improvement ({average_performance:.0%}) - regressing to level {new_level}"
        
        else:
            reason = f"Maintaining level {current_difficulty} - performance stable ({average_performance:.0%})"
        
        return new_level, reason
    
    def get_difficulty_context(self, difficulty_level: int) -> dict:
        """
        Get descriptive context for current difficulty level.
        
        Args:
            difficulty_level: Current level (1, 2, or 3)
            
        Returns:
            Dictionary with difficulty context
        """
        
        contexts = {
            1: {
                "name": "Beginner",
                "description": "Simple, confidence-building questions",
                "characteristics": ["Basic concepts", "Approachable", "Building foundation"],
                "question_style": "Simple 'what', 'why', 'how' questions",
            },
            2: {
                "name": "Intermediate",
                "description": "Analytical questions exploring deeper understanding",
                "characteristics": ["Real-world application", "Logical consistency", "Edge cases"],
                "question_style": "Deeper 'why' questions and application scenarios",
            },
            3: {
                "name": "Expert",
                "description": "Deep skepticism and conceptual defense challenges",
                "characteristics": ["Edge cases", "Misconceptions", "Adversarial scenarios"],
                "question_style": "Skeptical, adversarial questions testing mastery",
            },
        }
        
        return contexts.get(difficulty_level, contexts[1])
