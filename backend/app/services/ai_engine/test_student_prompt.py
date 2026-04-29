from app.services.ai_engine.prompt_builder import build_student_prompt
from app.services.ai_engine.llm_client import call_llm


def main() -> None:
    user_input = "Binary search works by dividing the array"
    prompt = build_student_prompt(user_input)
    response = call_llm(prompt)
    print(response)


if __name__ == "__main__":
    main()
