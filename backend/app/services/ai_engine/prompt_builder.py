"""
Curio AI — Adaptive Prompt Builder

Dynamically builds prompts for all AI modes:
- STUDENT MODE: Curious learner asking questions
- TEACHER MODE: Educational expert explaining
- RESCUE MODE: Helpful guide providing hints
- EVALUATOR MODE: Analysis and gap report generation

Supports difficulty progression (beginner → intermediate → expert)
and maintains conversational continuity with topic awareness.
"""

from typing import Optional, List


def build_student_mode_prompt(
    user_explanation: str,
    topic: str,
    difficulty_level: int = 1,
    conversation_history: Optional[List[dict]] = None,
) -> str:
    """
    Build a prompt for STUDENT MODE.
    AI acts as a curious student learning from the user.
    
    Args:
        user_explanation: What the user just explained
        topic: The topic being taught
        difficulty_level: 1=beginner, 2=intermediate, 3=expert
        conversation_history: Previous turns for context
        
    Returns:
        System prompt for student mode behavior
    """
    
    difficulty_instructions = {
        1: (
            "Ask SIMPLE, CONFIDENCE-BUILDING questions.\n"
            "- Focus on basic conceptual understanding\n"
            "- Ask 'what', 'why', 'how' but in approachable ways\n"
            "- Be slightly confused but eager to learn\n"
            "- Build toward deeper questions gradually"
        ),
        2: (
            "Ask ANALYTICAL questions that explore deeper understanding.\n"
            "- Challenge the explanation with 'why' questions\n"
            "- Explore real-world applications\n"
            "- Request examples and edge cases\n"
            "- Test logical consistency"
        ),
        3: (
            "Ask EXPERT-LEVEL questions with deep skepticism.\n"
            "- Attack hidden misconceptions and assumptions\n"
            "- Explore edge cases and boundary conditions\n"
            "- Challenge the reasoning with adversarial scenarios\n"
            "- Force conceptual defense and deeper justification"
        ),
    }
    
    system_instruction = (
        f"You are a curious, engaged STUDENT learning about: {topic}\n"
        f"The user is teaching you. Your job is to ask insightful questions.\n\n"
        f"DIFFICULTY LEVEL: {difficulty_level}\n"
        f"{difficulty_instructions.get(difficulty_level, difficulty_instructions[1])}\n\n"
        f"CORE RULES:\n"
        f"- Ask ONE focused question per response\n"
        f"- Never explain or correct the user\n"
        f"- Maintain a learning attitude\n"
        f"- Build on what the user said\n"
        f"- DO NOT EXPLAIN ANYTHING - ONLY ASK QUESTIONS\n"
    )
    
    # Add context if we have history
    history_context = ""
    if conversation_history and len(conversation_history) > 0:
        recent_turns = conversation_history[-2:]  # Last 2 exchanges for context
        history_context = "\nRECENT CONVERSATION:\n"
        for turn in recent_turns:
            role = "User" if turn.get("role") == "user" else "Student (You)"
            history_context += f"{role}: {turn.get('text', '')}\n"
    
    prompt = (
        f"{system_instruction}\n"
        f"{history_context}\n"
        f"User's latest explanation:\n{user_explanation}\n\n"
        f"Now ask ONE insightful follow-up question:"
    )
    
    return prompt


def build_teacher_mode_prompt(
    user_confusion: str,
    topic: str,
    previous_explanations: Optional[List[str]] = None,
) -> str:
    """
    Build a prompt for TEACHER MODE.
    AI switches to teacher role to clarify when user is stuck.
    
    Args:
        user_confusion: What the user is confused about
        topic: The topic being taught
        previous_explanations: Earlier user explanations for context
        
    Returns:
        System prompt for teacher mode behavior
    """
    
    system_instruction = (
        f"You are a patient TEACHER helping clarify: {topic}\n\n"
        f"The user is confused or stuck. Your job is to:\n"
        f"- Provide a MINIMAL, CLEAR explanation\n"
        f"- Use analogies or examples only if needed\n"
        f"- Help rebuild understanding without overwhelming\n"
        f"- Guide toward independent thinking\n"
        f"- Then return control to the user\n\n"
        f"IMPORTANT RULES:\n"
        f"- Keep explanation SHORT and FOCUSED\n"
        f"- Don't lecture or over-explain\n"
        f"- Use the user's own language where possible\n"
        f"- Clarify misconceptions gently\n"
        f"- End by encouraging the user to explain again\n"
    )
    
    context = ""
    if previous_explanations:
        context = f"\nUser's earlier explanation: {' '.join(previous_explanations[:2])}\n"
    
    prompt = (
        f"{system_instruction}"
        f"{context}"
        f"User's confusion point: {user_confusion}\n\n"
        f"Provide a brief, helpful clarification:"
    )
    
    return prompt


def build_rescue_mode_prompt(
    user_struggle: str,
    topic: str,
    difficulty_level: int = 1,
) -> str:
    """
    Build a prompt for RESCUE MODE.
    AI provides subtle hints when user is partially stuck.
    
    Args:
        user_struggle: Where the user is stuck
        topic: The topic being taught
        difficulty_level: Current difficulty level
        
    Returns:
        System prompt for rescue mode behavior
    """
    
    hint_level = {
        1: "Provide VERY GENTLE hints and leading questions.",
        2: "Provide INDIRECT hints that guide reasoning.",
        3: "Provide STRATEGIC hints pointing to logical next steps.",
    }
    
    system_instruction = (
        f"You are a RESCUE GUIDE helping with: {topic}\n"
        f"The user is stuck but can solve this independently.\n\n"
        f"{hint_level.get(difficulty_level, hint_level[1])}\n\n"
        f"RULES:\n"
        f"- NEVER give the full answer\n"
        f"- Ask leading questions, not explanations\n"
        f"- Help the user think through it themselves\n"
        f"- Preserve their confidence and independence\n"
        f"- Point to what they should consider, not the answer\n"
    )
    
    prompt = (
        f"{system_instruction}\n"
        f"User's struggle point: {user_struggle}\n\n"
        f"Provide a hint or guiding question (without solving it):"
    )
    
    return prompt


def build_evaluator_mode_prompt(
    conversation_history: List[dict],
    topic: str,
) -> str:
    """
    Build a prompt for EVALUATOR MODE.
    AI analyzes the full session and generates gap report.
    
    Args:
        conversation_history: Full conversation history
        topic: The topic being taught
        
    Returns:
        System prompt for evaluation
    """
    
    # Compile conversation for analysis
    conv_text = ""
    for turn in conversation_history:
        role = "User" if turn.get("role") == "user" else "AI"
        conv_text += f"{role}: {turn.get('text', '')}\n"
    
    system_instruction = (
        f"You are a COGNITIVE LEARNING EVALUATOR analyzing a teaching session on: {topic}\n\n"
        f"ANALYSIS TASK:\n"
        f"1. Identify STRENGTHS in the user's understanding\n"
        f"2. Identify GAPS and misconceptions\n"
        f"3. Note STRUGGLE POINTS and weak reasoning\n"
        f"4. Assess MASTERY LEVEL (0-100)\n"
        f"5. Recommend KEY AREAS for revisiting\n\n"
        f"Be specific, constructive, and actionable.\n"
    )
    
    prompt = (
        f"{system_instruction}\n"
        f"FULL CONVERSATION:\n{conv_text}\n\n"
        f"Provide a detailed evaluation of the user's understanding."
    )
    
    return prompt


def build_difficulty_progression_prompt(
    current_difficulty: int,
    user_performance: float,
) -> int:
    """
    Determine if difficulty should progress based on performance.
    
    Args:
        current_difficulty: Current level (1, 2, or 3)
        user_performance: User's score (0-1 scale)
        
    Returns:
        New difficulty level (1-3)
    """
    
    # Difficulty progression thresholds
    if current_difficulty == 1:
        if user_performance >= 0.75:
            return 2  # Progress to intermediate
        return 1
    
    elif current_difficulty == 2:
        if user_performance >= 0.80:
            return 3  # Progress to expert
        elif user_performance < 0.50:
            return 1  # Regress to beginner
        return 2
    
    else:  # current_difficulty == 3
        if user_performance < 0.45:
            return 2  # Regress to intermediate
        return 3


def build_mode_transition_prompt(
    from_mode: str,
    to_mode: str,
    reason: str,
) -> str:
    """
    Generate contextual transition message when switching modes.
    
    Args:
        from_mode: Current mode
        to_mode: New mode
        reason: Why we're switching (e.g., "user_stuck", "strong_performance")
        
    Returns:
        Transition context prompt
    """
    
    transition_messages = {
        ("student", "teacher"): (
            "Switching to TEACHER MODE because the user needs clarification. "
            "I'll provide a brief explanation to help rebuild understanding, "
            "then return to asking questions."
        ),
        ("student", "rescue"): (
            "Switching to RESCUE MODE because the user is partially stuck. "
            "I'll provide hints to guide independent problem-solving."
        ),
        ("teacher", "student"): (
            "Switching back to STUDENT MODE. Now asking follow-up questions "
            "to test the clarified understanding."
        ),
        ("rescue", "student"): (
            "Returning to STUDENT MODE to continue with deeper questions."
        ),
    }
    
    key = (from_mode, to_mode)
    return transition_messages.get(key, f"Switching from {from_mode} to {to_mode}.")
