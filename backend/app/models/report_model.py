"""
Curio AI — Report Models.

Defines the data structures for generating learning gap reports
after a teaching session has been evaluated.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.config.constants import SCHEMA_VERSION


class ReportRequest(BaseModel):
    """Payload for POST /report."""
    session_id: str = Field(description="Session to generate report for")


class GapItem(BaseModel):
    """A single knowledge gap identified in the user's teaching."""
    concept: str = Field(description="The concept with a gap")
    symptom: str = Field(description="How the gap manifested in the explanation")
    why_it_matters: str = Field(description="Why this gap is important to address")
    suggested_exercise: str = Field(description="A drill or exercise to close the gap")


class LearningReport(BaseModel):
    """Full learning report generated from evaluation results."""
    schema_version: str = Field(default=SCHEMA_VERSION)
    summary: str = Field(description="Executive summary of the teaching session")
    strengths: List[str] = Field(
        default_factory=list,
        description="Things the user explained well",
    )
    gaps: List[GapItem] = Field(
        default_factory=list,
        description="Knowledge gaps with actionable remediation",
    )
    suggested_drills: List[str] = Field(
        default_factory=list,
        description="Recommended practice exercises",
    )
    next_steps: List[str] = Field(
        default_factory=list,
        description="What to focus on next",
    )
    extras: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extension point for future report types",
    )


class ReportResponse(BaseModel):
    """Wrapped learning report for the API response."""
    session_id: str
    report: LearningReport
