def evaluate_response(user_input: str) -> dict:
    """Evaluate the user response and return score, understanding, and feedback."""
    score = 0
    feedback = []
    text = user_input.lower()

    if len(user_input) > 20:
        score += 3
    else:
        feedback.append("Add more detail to make your response longer.")

    if "because" in text:
        score += 3
    else:
        feedback.append("Include reasoning like 'because' to explain your thinking.")

    if "example" in text:
        score += 4
    else:
        feedback.append("Add an example to illustrate your point.")

    if score <= 3:
        understanding = "Weak"
    elif score <= 7:
        understanding = "Moderate"
    else:
        understanding = "Strong"

    return {
        "score": score,
        "understanding": understanding,
        "feedback": feedback,
    }
