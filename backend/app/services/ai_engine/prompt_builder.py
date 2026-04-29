def build_student_prompt(user_input: str) -> str:
    """Build a student-style system prompt from user input."""
    system_instruction = (
        "You are a curious student. Do not explain concepts. Only ask questions."
    )
    rules = (
        "Ask 'why', 'how', 'what if'.\n"
        "Challenge the explanation.\n"
        "Stay on topic.\n"
        "Be slightly confused.\n"
        "DO NOT EXPLAIN ANYTHING.\n"
        "ONLY ASK A QUESTION."
    )

    return (
        f"{system_instruction}\n\n"
        "Instructions:\n"
        f"{rules}\n\n"
        "User input:\n"
        f"{user_input}"
    )
