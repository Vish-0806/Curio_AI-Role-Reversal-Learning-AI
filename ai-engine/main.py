import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVICES_DIR = ROOT / "services"
sys.path.insert(0, str(SERVICES_DIR))

from ai_logic import generate_ai_response
from evaluator import evaluate_response


def main() -> None:
    print("Welcome to the learning loop. Please explain your idea first.")
    first_input = input("Your explanation: ")

    user_responses = [first_input]
    current_input = first_input

    for turn in range(4):
        print(f"\nTurn {turn + 1}")
        ai_response = generate_ai_response(current_input)
        print("AI:")
        print(ai_response)

        current_input = input("Your reply: ")
        user_responses.append(current_input)

    combined_input = " ".join(user_responses)
    evaluation = evaluate_response(combined_input)

    print("\nFinal evaluation")
    print("Score (out of 10):", evaluation["score"])
    print("Understanding level:", evaluation["understanding"])
    print("Feedback:")
    for item in evaluation["feedback"]:
        print("-", item)


if __name__ == "__main__":
    main()