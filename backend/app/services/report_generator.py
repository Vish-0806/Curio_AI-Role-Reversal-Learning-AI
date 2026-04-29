"""
Curio AI — Report Generator Service.

Generates a LearningReport from session state + evaluation results.
Currently deterministic; designed for future AI-generated reports.

Extension points:
- AI-generated personalized recommendations
- Spaced repetition scheduling
- Cross-session trend analysis
"""

from typing import List

from app.models.evaluation_model import EvaluationResult
from app.models.report_model import GapItem, LearningReport
from app.models.session_model import SessionState
from app.utils.error_handler import CurioValidationError
from app.utils.logger import get_logger

logger = get_logger(__name__)


def generate_report(session_state: SessionState, evaluation: EvaluationResult) -> LearningReport:
    """
    Generate a learning report from session state and evaluation.

    Args:
        session_state: Session with conversation history
        evaluation: Completed evaluation result

    Returns:
        LearningReport with strengths, gaps, drills, and next steps
    """
    topic = session_state.topic or "the discussed topic"
    user_turns = [t for t in session_state.conversation if t.role == "user"]

    # ── Summary ──────────────────────────────────────────────────
    summary = _build_summary(topic, evaluation, len(user_turns))

    # ── Strengths ────────────────────────────────────────────────
    strengths = _identify_strengths(evaluation)

    # ── Gaps ─────────────────────────────────────────────────────
    gaps = _identify_gaps(topic, evaluation)

    # ── Suggested Drills ─────────────────────────────────────────
    drills = _suggest_drills(topic, evaluation)

    # ── Next Steps ───────────────────────────────────────────────
    next_steps = _suggest_next_steps(topic, evaluation, gaps)

    logger.info("Report generated", extra={
        "session_id": session_state.session_id,
        "strengths": len(strengths),
        "gaps": len(gaps),
    })

    return LearningReport(
        summary=summary,
        strengths=strengths,
        gaps=gaps,
        suggested_drills=drills,
        next_steps=next_steps,
    )


def _build_summary(topic: str, evaluation: EvaluationResult, turn_count: int) -> str:
    score = evaluation.overall_score
    if score >= 0.8:
        quality = "excellent"
    elif score >= 0.6:
        quality = "good"
    elif score >= 0.4:
        quality = "developing"
    else:
        quality = "needs improvement"

    return (
        f"Teaching session on '{topic}' ({turn_count} turns): {quality} overall "
        f"(score: {score:.0%}). "
        f"{evaluation.rationale}"
    )


def _identify_strengths(evaluation: EvaluationResult) -> List[str]:
    strengths = []
    for dim in evaluation.scores:
        if dim.score >= 0.7:
            label = dim.dimension.replace("_", " ").title()
            strengths.append(f"{label}: {dim.rationale}")
    if not strengths:
        strengths.append("Keep practicing! Strengths will emerge with more teaching.")
    return strengths


def _identify_gaps(topic: str, evaluation: EvaluationResult) -> List[GapItem]:
    gaps = []
    for dim in evaluation.scores:
        if dim.score < 0.5:
            gap = _dimension_to_gap(topic, dim.dimension, dim.score, dim.rationale)
            gaps.append(gap)

    for misc in evaluation.misconceptions:
        gaps.append(GapItem(
            concept=f"Potential misconception in {topic}",
            symptom=misc.description,
            why_it_matters="Misconceptions can compound and lead to deeper misunderstandings",
            suggested_exercise=f"Review authoritative sources on {topic} and verify your claims",
        ))

    return gaps


def _dimension_to_gap(topic: str, dimension: str, score: float, rationale: str) -> GapItem:
    gap_map = {
        "clarity": GapItem(
            concept=f"Clarity of explanation for {topic}",
            symptom=f"Low clarity score ({score:.0%}): {rationale}",
            why_it_matters="Unclear explanations indicate the teacher may not fully grasp the concept",
            suggested_exercise="Rewrite your explanation in 3 sentences for a 10-year-old",
        ),
        "correctness_proxy": GapItem(
            concept=f"Confidence and consistency in {topic}",
            symptom=f"Low consistency score ({score:.0%}): {rationale}",
            why_it_matters="Contradictions and hedging suggest uncertain understanding",
            suggested_exercise="List 3 facts you're certain about and verify them against a textbook",
        ),
        "examples": GapItem(
            concept=f"Use of examples for {topic}",
            symptom=f"Low examples score ({score:.0%}): {rationale}",
            why_it_matters="Examples are crucial for demonstrating practical understanding",
            suggested_exercise="Come up with 3 real-world examples that illustrate the concept",
        ),
        "depth": GapItem(
            concept=f"Depth of knowledge in {topic}",
            symptom=f"Low depth score ({score:.0%}): {rationale}",
            why_it_matters="Shallow explanations suggest surface-level understanding",
            suggested_exercise="Explain WHY the concept works, not just WHAT it is",
        ),
        "structure": GapItem(
            concept=f"Organization of {topic} explanation",
            symptom=f"Low structure score ({score:.0%}): {rationale}",
            why_it_matters="Well-structured explanations reflect organized thinking",
            suggested_exercise="Create an outline before explaining: intro, key points, examples, summary",
        ),
    }
    return gap_map.get(dimension, GapItem(
        concept=topic,
        symptom=f"Low score in {dimension}",
        why_it_matters="This area needs improvement",
        suggested_exercise="Review and practice this area",
    ))


def _suggest_drills(topic: str, evaluation: EvaluationResult) -> List[str]:
    drills = []
    if evaluation.overall_score < 0.6:
        drills.append(f"Feynman Technique: Explain {topic} from scratch without notes")
    for dim in evaluation.scores:
        if dim.score < 0.5 and dim.dimension == "examples":
            drills.append(f"Example Bank: Write 5 examples for each sub-concept of {topic}")
        if dim.score < 0.5 and dim.dimension == "depth":
            drills.append(f"Why Chain: Ask 'why?' 5 times to dig deeper into {topic}")
    if not drills:
        drills.append(f"Challenge Mode: Try teaching {topic} to someone unfamiliar with it")
    return drills


def _suggest_next_steps(topic: str, evaluation: EvaluationResult, gaps: List[GapItem]) -> List[str]:
    steps = []
    if gaps:
        steps.append(f"Address the {len(gaps)} identified gap(s) using the suggested exercises")
    if evaluation.overall_score >= 0.7:
        steps.append(f"Try teaching a more advanced aspect of {topic}")
        steps.append("Move to quiz mode to test your knowledge under pressure")
    else:
        steps.append(f"Review foundational material on {topic}")
        steps.append("Re-teach the topic focusing on areas with low scores")
    steps.append("Schedule a follow-up session in 2-3 days (spaced repetition)")
    return steps
