import random


def inject_mistake(user_input: str) -> str:
    """Return a short, incorrect or misleading challenge statement."""
    mistakes = [
        "So this works even if the data is not sorted, right?",
        "So the time complexity is O(n), correct?",
        "So this method always works in every case?",
        "So there is no need to check edge cases here, right?",
        "So the order of elements doesn't matter at all?",
    ]
    return random.choice(mistakes)
