"""
Curio AI — Evaluation Router Service.

Rule-based evaluator (heuristics) for MVP. Scores the user's teaching
across multiple dimensions: clarity, correctness_proxy, examples, depth, structure.

Extension points:
- Replace with AI-based evaluator (same interface)
- Add custom rubrics per topic
- Add peer-comparison scoring
"""

from typing import List

from app.config.constants import (
    EVALUATION_DIMENSIONS,
    EXAMPLE_INDICATORS,
    MIN_TURNS_FOR_EVALUATION,
    VAGUENESS_WORDS,
)
from app.models.evaluation_model import (
    DimensionScore,
    EvaluationResult,
    MisconceptionItem,
)
from app.models.session_model import SessionState
from app.utils.error_handler import CurioValidationError
from app.utils.logger import get_logger

logger = get_logger(__name__)


def evaluate_session(session_state: SessionState, rubric: str | None = None) -> EvaluationResult:
    """
    Evaluate the user's teaching performance using heuristics.

    Args:
        session_state: Session with conversation history
        rubric: Optional rubric name (reserved for future use)

    Returns:
        EvaluationResult with dimension scores and analysis
    """
    user_turns = [t for t in session_state.conversation if t.role == "user"]

    if len(user_turns) < MIN_TURNS_FOR_EVALUATION:
        raise CurioValidationError(
            message=f"Need at least {MIN_TURNS_FOR_EVALUATION} teaching turns to evaluate",
            details={"current_turns": len(user_turns), "required": MIN_TURNS_FOR_EVALUATION},
        )

    # Combine all user text for analysis
    full_text = " ".join(t.text for t in user_turns)
    full_lower = full_text.lower()

    # ── Score each dimension ─────────────────────────────────────
    scores: List[DimensionScore] = []

    # 1. Clarity
    clarity = _score_clarity(full_text, full_lower, user_turns)
    scores.append(clarity)

    # 2. Correctness proxy
    correctness = _score_correctness_proxy(full_text, full_lower)
    scores.append(correctness)

    # 3. Examples
    examples = _score_examples(full_text, full_lower)
    scores.append(examples)

    # 4. Depth
    depth = _score_depth(full_text, full_lower, user_turns)
    scores.append(depth)

    # 5. Structure
    structure = _score_structure(full_text, user_turns)
    scores.append(structure)

    # ── Overall score (weighted average) ─────────────────────────
    weights = {"clarity": 0.25, "correctness_proxy": 0.2, "examples": 0.2, "depth": 0.2, "structure": 0.15}
    overall = sum(s.score * weights.get(s.dimension, 0.2) for s in scores)
    overall = round(min(1.0, max(0.0, overall)), 2)

    # ── Misconceptions (heuristic) ───────────────────────────────
    misconceptions = _detect_misconceptions(full_text, full_lower)

    # ── Missing examples ─────────────────────────────────────────
    missing_examples = []
    if examples.score < 0.5:
        missing_examples.append("The explanation lacks concrete examples")
    if "analogy" not in full_lower and "like" not in full_lower:
        missing_examples.append("No analogies were used to aid understanding")

    # ── Confidence ───────────────────────────────────────────────
    confidence = min(0.9, 0.3 + (len(user_turns) * 0.1))

    rationale = (
        f"Based on {len(user_turns)} teaching turns. "
        f"Strongest area: {max(scores, key=lambda s: s.score).dimension}. "
        f"Weakest area: {min(scores, key=lambda s: s.score).dimension}."
    )

    logger.info("Evaluation complete", extra={
        "session_id": session_state.session_id,
        "overall_score": overall,
        "turn_count": len(user_turns),
    })

    return EvaluationResult(
        scores=scores,
        overall_score=overall,
        misconceptions=misconceptions,
        missing_examples=missing_examples,
        confidence=round(confidence, 2),
        rationale=rationale,
    )


# ═══════════════════════════════════════════════════════════════════
#  Dimension Scorers (private)
# ═══════════════════════════════════════════════════════════════════

def _score_clarity(text: str, lower: str, turns) -> DimensionScore:
    """Score clarity based on sentence length, vagueness, and structure."""
    words = text.split()
    avg_word_count = len(words) / max(len(turns), 1)

    vague_count = sum(1 for w in VAGUENESS_WORDS if w in lower)
    vague_penalty = min(0.4, vague_count * 0.08)

    score = 0.7
    if avg_word_count > 30:
        score += 0.15
    elif avg_word_count < 10:
        score -= 0.2

    score -= vague_penalty
    score = round(min(1.0, max(0.0, score)), 2)

    rationale = f"Avg {avg_word_count:.0f} words/turn, {vague_count} vague terms detected"
    return DimensionScore(dimension="clarity", score=score, rationale=rationale)


def _score_correctness_proxy(text: str, lower: str) -> DimensionScore:
    """Proxy for correctness: check for contradictions and hedging."""
    contradiction_markers = ["but also", "however", "on the other hand", "actually no"]
    hedge_markers = ["I think", "maybe", "probably", "not sure", "I guess"]

    contradictions = sum(1 for m in contradiction_markers if m in lower)
    hedges = sum(1 for m in hedge_markers if m in lower)

    score = 0.7
    score -= contradictions * 0.1
    score -= hedges * 0.05
    score = round(min(1.0, max(0.0, score)), 2)

    rationale = f"{contradictions} contradiction markers, {hedges} hedging phrases"
    return DimensionScore(dimension="correctness_proxy", score=score, rationale=rationale)


def _score_examples(text: str, lower: str) -> DimensionScore:
    """Score based on presence and quantity of examples."""
    example_count = sum(1 for ind in EXAMPLE_INDICATORS if ind in lower)

    if example_count >= 3:
        score = 0.9
    elif example_count >= 1:
        score = 0.6
    else:
        score = 0.2

    rationale = f"{example_count} example indicator(s) found"
    return DimensionScore(dimension="examples", score=score, rationale=rationale)


def _score_depth(text: str, lower: str, turns) -> DimensionScore:
    """Score depth based on word count, detail level, and progression."""
    total_words = len(text.split())
    detail_markers = ["because", "therefore", "the reason", "this means", "as a result", "specifically"]
    detail_count = sum(1 for m in detail_markers if m in lower)

    score = 0.5
    if total_words > 200:
        score += 0.2
    if total_words > 500:
        score += 0.1
    score += min(0.3, detail_count * 0.06)
    score = round(min(1.0, max(0.0, score)), 2)

    rationale = f"{total_words} total words, {detail_count} detail markers"
    return DimensionScore(dimension="depth", score=score, rationale=rationale)


def _score_structure(text: str, turns) -> DimensionScore:
    """Score structure based on turn count, consistency, and organization."""
    turn_count = len(turns)
    turn_lengths = [len(t.text.split()) for t in turns]
    length_variance = max(turn_lengths) - min(turn_lengths) if turn_lengths else 0

    score = 0.6
    if turn_count >= 5:
        score += 0.15
    if length_variance < 50:
        score += 0.1
    score = round(min(1.0, max(0.0, score)), 2)

    rationale = f"{turn_count} turns, length variance: {length_variance} words"
    return DimensionScore(dimension="structure", score=score, rationale=rationale)


def _detect_misconceptions(text: str, lower: str) -> List[MisconceptionItem]:
    """Heuristic misconception detection."""
    misconceptions = []

    absolute_terms = ["always", "never", "impossible", "guaranteed", "100%"]
    for term in absolute_terms:
        if term in lower:
            idx = lower.index(term)
            context = text[max(0, idx - 30):idx + 30]
            misconceptions.append(MisconceptionItem(
                description=f"Absolute claim detected ('{term}') — most concepts have exceptions",
                evidence=context.strip(),
                severity="low",
            ))

    if len(misconceptions) > 3:
        misconceptions = misconceptions[:3]

    return misconceptions
