from app.services.ai_engine.ai_logic import generate_ai_response


def get_ai_response(user_input: str, conversation: list) -> dict:
    """
    Wrapper for AI engine to match backend format
    """

    ai_text = generate_ai_response(user_input)

    return {
        "ai_message": ai_text,
        "ai_intent": "question",   # default
        "followups": [],
        "flags": {
            "needs_example": False,
            "detected_gap": False
        }
    }