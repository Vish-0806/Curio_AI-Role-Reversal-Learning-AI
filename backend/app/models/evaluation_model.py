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
    scores: List[DimensionScore] = Field(
        description="Scores across evaluation dimensions",
    )
    overall_score: float = Field(ge=0.0, le=1.0, description="Weighted overall score")
    misconceptions: List[MisconceptionItem] = Field(default_factory=list)
    missing_examples: List[str] = Field(
        default_factory=list,
        description="Topics that lacked concrete examples",
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        default=0.5,
        description="Evaluator's confidence in this assessment",
    )
    rationale: str = Field(
        default="",
        description="Short overall rationale for the evaluation",
    )
    extras: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extension point for future rubric versions",
    )


class EvaluationResponse(BaseModel):
    """Wrapped evaluation result for the API response."""
    session_id: str
    evaluation: EvaluationResult
