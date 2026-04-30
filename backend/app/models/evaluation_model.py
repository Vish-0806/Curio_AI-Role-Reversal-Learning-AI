"""
Curio AI — Evaluation Models.

Defines the data structures for evaluating a user's teaching performance
across multiple dimensions (clarity, examples, depth, etc.).
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.config.constants import SCHEMA_VERSION


class EvaluationRequest(BaseModel):
    """Payload for POST /evaluate."""
    session_id: str = Field(description="Session to evaluate")
    rubric: Optional[str] = Field(
        default=None,
        description="Optional rubric name to use (default uses standard rubric)",
    )


class DimensionScore(BaseModel):
    """Score for a single evaluation dimension."""
    dimension: str = Field(description="e.g. clarity, depth, examples")
    score: float = Field(ge=0.0, le=1.0, description="Score from 0.0 to 1.0")
    rationale: str = Field(description="Brief explanation for this score")


class MisconceptionItem(BaseModel):
    """A detected misconception or inaccuracy in the user's explanation."""
    description: str
    evidence: Optional[str] = Field(default=None, description="Quote from conversation")
    severity: str = Field(default="medium", description="low | medium | high")


class EvaluationResult(BaseModel):
    """Result of evaluating the user's teaching session."""
    schema_version: str = Field(default=SCHEMA_VERSION)
    overall_understanding_score: float = Field(default=0.0, description="Score from 0-100")
    confidence_level: float = Field(default=0.0, description="AI confidence in the assessment")
    mastery_level: str = Field(default="Beginner", description="Beginner | Developing | Proficient | Mastery")
    
    strengths: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    struggle_moments: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    
    ai_analysis: str = Field(default="", description="The full AI analysis text")
    
    # Statistics
    question_count: int = Field(default=0)
    avg_response_quality: float = Field(default=0.0)
    final_difficulty_reached: int = Field(default=1)
    
    # Legacy compatibility (optional)
    scores: List[DimensionScore] = Field(default_factory=list)
    overall_score: float = Field(default=0.0)
    misconceptions: List[MisconceptionItem] = Field(default_factory=list)
    
    extras: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extension point for future rubric versions",
    )


class EvaluationResponse(BaseModel):
    """Wrapped evaluation result for the API response."""
    session_id: str
    evaluation: EvaluationResult
