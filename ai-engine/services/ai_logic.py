import random

from prompt_builder import build_student_prompt
from llm_client import call_llm
from mistake_injection import inject_mistake


def generate_ai_response(user_input: str) -> str:
    """Return an AI response or injected mistake based on random chance."""
    if random.random() < 0.7:
        prompt = build_student_prompt(user_input)
        return call_llm(prompt)

    return inject_mistake(user_input)
