"""
Curio AI — Dynamic Mistake Injection Service

Generates topic-agnostic, LLM-driven subtle conceptual mistakes
based on what the user taught. Mistakes are:
- Hard to detect (not obviously wrong)
- Topic-specific (derived from user explanations)
- Solvable (user can identify and correct)
- Mastery validation (tests deep understanding)
"""

from typing import Optional
from app.services.ai_engine.llm_client import call_llm_structured


def generate_mistake_injection_prompt(
    user_explanations: list[str],
    topic: str,
    difficulty_level: int = 1,
) -> str:
    """
    Build a prompt to generate a subtle mistake for user's topic.
    
    Args:
        user_explanations: List of user's explanations from conversation
        topic: The topic being taught
        difficulty_level: 1=beginner, 2=intermediate, 3=expert
        
    Returns:
        LLM prompt asking for mistake generation
    """
    
    # Condense user explanations to provide context
    explanation_summary = "\n".join(user_explanations[-3:]) if user_explanations else "No explanations yet"
    
    difficulty_context = {
        1: "simple and confidence-building but slightly misleading",
        2: "analytical and requires deeper thinking to spot",
        3: "deeply subtle, testing edge cases and hidden misconceptions"
    }
    
    prompt = f"""You are a cognitive learning system designed to challenge mastery through subtle mistakes.

TOPIC: {topic}
DIFFICULTY LEVEL: {difficulty_level}

USER'S EXPLANATIONS:
{explanation_summary}

YOUR TASK:
Generate ONE subtle, {difficulty_context.get(difficulty_level, 'challenging')} misconception or false statement about the topic based on what the user taught.

REQUIREMENTS FOR THE MISTAKE:
- Must seem plausible based on the user's explanation
- Should be {difficulty_context.get(difficulty_level, 'challenging')}
- Should be a single, concrete statement (1-2 sentences max)
- Must be something a user could legitimately need to defend against
- Avoid being obviously wrong
- Should challenge the user's actual understanding

FORMAT:
Generate ONLY the mistake statement as a question or challenge. No explanation, no meta-commentary.
Examples:
- "So in this system, the order doesn't matter at all, right?"
- "This approach always terminates in constant time?"
- "The edge case you mentioned only occurs with negative inputs?"

Now generate a mistake for the topic "{topic}" based on the user's explanation:"""
    
    return prompt


def inject_mistake_llm(
    user_explanations: list[str],
    topic: str,
    difficulty_level: int = 1,
) -> str:
    """
    Generate a topic-specific mistake using LLM.
    
    Args:
        user_explanations: List of user's explanations from conversation
        topic: The topic being taught
        difficulty_level: 1=beginner, 2=intermediate, 3=expert
        
    Returns:
        Generated mistake statement
    """
    try:
        prompt = generate_mistake_injection_prompt(
            user_explanations,
            topic,
            difficulty_level
        )
        
        mistake = call_llm_structured(prompt)
        
        # Ensure we got a valid response
        if mistake and len(mistake.strip()) > 5:
            return mistake.strip()
        
        # Fallback if LLM returns empty or very short response
        return generate_fallback_mistake(topic, difficulty_level)
        
    except Exception as exc:
        # If LLM fails, use intelligent fallback
        return generate_fallback_mistake(topic, difficulty_level)


def generate_fallback_mistake(topic: str, difficulty_level: int) -> str:
    """
    Generate a reasonable fallback mistake if LLM is unavailable.
    Still topic-aware and adaptive to difficulty.
    
    Args:
        topic: The topic being taught
        difficulty_level: 1=beginner, 2=intermediate, 3=expert
        
    Returns:
        Fallback mistake statement
    """
    fallback_mistakes_by_difficulty = {
        1: [
            f"So in {topic}, there are no exceptions to the basic rule you explained, right?",
            f"The approach you described works in all situations without modification?",
            f"There's no difference between edge cases in {topic}?",
            f"Scaling is not a concern for {topic}?",
            f"Order and sequence don't affect how {topic} works?",
        ],
        2: [
            f"Your explanation covers all scenarios in {topic}?",
            f"The assumptions you made about {topic} hold universally?",
            f"There are no hidden dependencies in the {topic} you described?",
            f"The time/space tradeoff isn't relevant to {topic}?",
            f"Different contexts apply the same {topic} principles identically?",
        ],
        3: [
            f"The corner cases you mentioned are the only edge cases in {topic}?",
            f"Your reasoning about {topic} wouldn't fail under adversarial conditions?",
            f"All variations of {topic} follow the same underlying pattern you described?",
            f"The optimization you chose is always better than alternatives in {topic}?",
            f"Your explanation of {topic} accounts for all known misconceptions?",
        ],
    }
    
    import random
    mistakes = fallback_mistakes_by_difficulty.get(difficulty_level, fallback_mistakes_by_difficulty[1])
    return random.choice(mistakes)
