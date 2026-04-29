"""
Curio AI — Report Generator Service

Generates comprehensive learning reports from session state and evaluation.

Report includes:
- Detailed gap analysis
- Mastery assessment
- Personalized recommendations
- Learning roadmap
- Progress tracking
"""

from typing import List, Dict, Any
from datetime import datetime

from app.models.evaluation_model import EvaluationResult
from app.models.report_model import GapItem, LearningReport
from app.models.session_model import SessionState
from app.utils.error_handler import CurioValidationError
from app.utils.logger import get_logger

logger = get_logger(__name__)


def generate_report(
    session_state: SessionState,
    evaluation: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a comprehensive learning report from session state and evaluation.

    Args:
        session_state: Session with conversation history and metadata
        evaluation: Comprehensive evaluation from SessionEvaluator

    Returns:
        Detailed report dictionary with all learning insights
    """
    
    topic = session_state.topic or "the discussed topic"
    user_turns = [t for t in session_state.conversation if t.role == "user"]
    
    report = {
        "report_id": f"report_{session_state.session_id}_{int(datetime.now().timestamp())}",
        "session_id": session_state.session_id,
        "topic": topic,
        "generated_at": datetime.now().isoformat(),
        
        # ── Core Metrics ──────────────────────────────────────
        "understanding_score": evaluation.get("overall_understanding_score", 0.0),
        "mastery_level": evaluation.get("mastery_level", "Beginner"),
        "confidence_level": evaluation.get("confidence_level", 0.0),
        "difficulty_reached": evaluation.get("final_difficulty_reached", 1),
        "question_count": evaluation.get("question_count", 0),
        "avg_response_quality": evaluation.get("avg_response_quality", 0.0),
        
        # ── Learning Profile ──────────────────────────────────
        "summary": _build_comprehensive_summary(topic, evaluation, len(user_turns)),
        "strengths": evaluation.get("strengths", []),
        "gaps": evaluation.get("gaps", []),
        "misconceptions": evaluation.get("misconceptions", []),
        
        # ── Structured Gaps Report ────────────────────────────
        "gap_analysis": _build_gap_analysis_report(evaluation, topic),
        
        # ── Recommendations ───────────────────────────────────
        "personalized_recommendations": evaluation.get("recommendations", []),
        "learning_roadmap": _build_learning_roadmap(
            evaluation,
            topic,
            session_state.difficulty_level
        ),
        
        # ── Session Statistics ─────────────────────────────────
        "session_statistics": {
            "total_turns": len(session_state.conversation),
            "user_turns": len(user_turns),
            "session_duration_minutes": 0,  # Can be calculated if timestamps available
            "mode_switches": len(session_state.mode_switch_history),
            "final_mode": session_state.current_mode,
        },
        
        # ── AI Analysis ───────────────────────────────────────
        "detailed_analysis": evaluation.get("ai_analysis", ""),
    }
    
    logger.info(
        "Report generated",
        extra={
            "session_id": session_state.session_id,
            "understanding_score": report["understanding_score"],
            "mastery_level": report["mastery_level"],
            "gaps_count": len(report["gaps"]),
        }
    )
    
    return report


def _build_comprehensive_summary(
    topic: str,
    evaluation: Dict[str, Any],
    turn_count: int,
) -> str:
    """Build comprehensive session summary."""
    
    score = evaluation.get("overall_understanding_score", 0.0)
    mastery = evaluation.get("mastery_level", "Beginner")
    
    if mastery == "Mastery":
        quality_desc = "excellent mastery"
        emoji = "✓"
    elif mastery == "Proficient":
        quality_desc = "solid proficiency"
        emoji = "○"
    elif mastery == "Developing":
        quality_desc = "developing understanding"
        emoji = "◐"
    else:
        quality_desc = "foundational understanding"
        emoji = "◑"
    
    gaps = evaluation.get("gaps", [])
    misconceptions = evaluation.get("misconceptions", [])
    
    summary = (
        f"{emoji} Teaching session on '{topic}' ({turn_count} teaching turns)\n"
        f"Overall understanding: {quality_desc} (Score: {score:.0f}%)\n"
        f"Mastery Level: {mastery}\n"
    )
    
    if gaps:
        summary += f"Areas for improvement: {len(gaps)} identified\n"
    
    if misconceptions:
        summary += f"⚠ Misconceptions detected: {len(misconceptions)} - Review recommended\n"
    
    summary += f"\n{evaluation.get('ai_analysis', 'Session completed.').split(chr(10))[0]}"
    
    return summary


def _build_gap_analysis_report(evaluation: Dict[str, Any], topic: str) -> Dict[str, Any]:
    """Build structured gap analysis report."""
    
    gaps = evaluation.get("gaps", [])
    
    gap_report = {
        "total_gaps_identified": len(gaps),
        "gaps_by_priority": {
            "high": [],
            "medium": [],
            "low": [],
        },
        "detailed_gaps": [],
    }
    
    for gap in gaps:
        priority = gap.get("priority", "medium")
        
        # Categorize by priority
        if priority in gap_report["gaps_by_priority"]:
            gap_report["gaps_by_priority"][priority].append(gap.get("area", "Unknown"))
        
        # Add detailed gap item
        gap_item = {
            "area": gap.get("area", "Unknown"),
            "issue": gap.get("issue", ""),
            "priority": priority,
            "why_it_matters": _explain_gap_importance(gap.get("area", "")),
            "suggested_focus": _suggest_gap_remediation(gap.get("area", ""), topic),
        }
        gap_report["detailed_gaps"].append(gap_item)
    
    return gap_report


def _explain_gap_importance(area: str) -> str:
    """Explain why a particular gap matters."""
    
    importance_map = {
        "Conceptual clarity": "Understanding the core concepts is fundamental to mastery and prevents cascading confusion",
        "Edge cases and special scenarios": "Missing edge case handling can lead to failures in real applications and incomplete understanding",
        "Practical examples": "Concrete examples demonstrate practical understanding and help retain knowledge",
        "Critical thinking": "The ability to question assumptions is essential for deep, lasting learning",
        "Conceptual depth": "Depth separates surface-level knowledge from true mastery",
    }
    
    # Return mapped explanation or generate generic one
    for key, explanation in importance_map.items():
        if key.lower() in area.lower():
            return explanation
    
    return f"Strengthening '{area}' is essential for complete understanding of this topic"


def _suggest_gap_remediation(area: str, topic: str) -> str:
    """Suggest how to address a specific gap."""
    
    remediation_map = {
        "Conceptual clarity": f"Create a written summary of {topic} in your own words, then compare with authoritative sources",
        "Edge cases": f"Identify 5 edge cases or boundary conditions in {topic} and explain how they're handled",
        "Practical examples": f"Write 3 real-world examples for {topic}, focusing on practical application",
        "Critical thinking": f"For each claim about {topic}, write 'Why is this true?' and 'What could make this false?'",
        "Conceptual depth": f"Use the Feynman Technique: explain {topic} as if teaching it to someone new",
    }
    
    for key, suggestion in remediation_map.items():
        if key.lower() in area.lower():
            return suggestion
    
    return f"Review and practice {area} through targeted exercises and re-teaching"


def _build_learning_roadmap(
    evaluation: Dict[str, Any],
    topic: str,
    current_difficulty: int,
) -> List[Dict[str, Any]]:
    """Build personalized learning roadmap."""
    
    mastery = evaluation.get("mastery_level", "Beginner")
    score = evaluation.get("overall_understanding_score", 0.0)
    gaps = evaluation.get("gaps", [])
    misconceptions = evaluation.get("misconceptions", [])
    
    roadmap = []
    
    # Step 1: Address critical issues
    if misconceptions:
        roadmap.append({
            "step": 1,
            "priority": "CRITICAL",
            "action": "Address Misconceptions",
            "description": f"Review and correct {len(misconceptions)} identified misconception(s)",
            "timeline": "Next session or immediately",
            "resources": [
                "Review authoritative sources on the topic",
                "Test your revised understanding",
                "Get feedback on corrected concepts"
            ],
        })
    
    # Step 2: Fill knowledge gaps
    if gaps:
        roadmap.append({
            "step": 1 if misconceptions else 1,
            "priority": "HIGH",
            "action": "Strengthen Knowledge Gaps",
            "description": f"Focus on {min(3, len(gaps))} high-priority gaps",
            "timeline": "This week",
            "resources": [
                f"Use targeted exercises for each gap",
                f"Create concrete examples for {topic}",
                "Teach someone else to reinforce understanding"
            ],
        })
    
    # Step 3: Deepen understanding
    if mastery in ["Developing", "Proficient"]:
        roadmap.append({
            "step": 2 if (misconceptions or gaps) else 1,
            "priority": "MEDIUM",
            "action": "Deepen Understanding",
            "description": "Move beyond basics to deeper conceptual understanding",
            "timeline": "Next 1-2 weeks",
            "resources": [
                f"Explore advanced aspects of {topic}",
                "Connect concepts to related topics",
                "Work through complex scenarios"
            ],
        })
    
    # Step 4: Achieve mastery
    if mastery != "Mastery":
        roadmap.append({
            "step": 3 if (misconceptions or gaps) else 2,
            "priority": "MEDIUM",
            "action": "Achieve Mastery",
            "description": "Teach the topic to others and handle adversarial questions",
            "timeline": "Ongoing practice",
            "resources": [
                f"Teach {topic} to peers or community",
                "Participate in challenging discussions",
                "Create teaching materials for others"
            ],
        })
    else:
        roadmap.append({
            "step": 2,
            "priority": "OPTIONAL",
            "action": "Share Knowledge",
            "description": "Teach others and explore related advanced topics",
            "timeline": "Ongoing",
            "resources": [
                "Create teaching materials",
                "Mentor others learning this topic",
                "Explore related advanced concepts"
            ],
        })
    
    return roadmap


def generate_quick_feedback(evaluation: Dict[str, Any]) -> str:
    """Generate quick feedback summary (for chat display)."""
    
    mastery = evaluation.get("mastery_level", "Beginner")
    score = evaluation.get("overall_understanding_score", 0.0)
    gaps = evaluation.get("gaps", [])
    
    feedback_parts = [
        f"Mastery Level: {mastery} ({score:.0f}%)"
    ]
    
    if gaps:
        gap_areas = [g.get("area", "Unknown") for g in gaps[:2]]
        feedback_parts.append(f"Focus areas: {', '.join(gap_areas)}")
    
    strengths = evaluation.get("strengths", [])
    if strengths:
        feedback_parts.append(f"Strengths: {strengths[0][:50]}...")
    
    return " | ".join(feedback_parts)
