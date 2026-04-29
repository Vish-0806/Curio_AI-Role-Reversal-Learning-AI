from dotenv import load_dotenv
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")


def _get_client():
    try:
        from groq import Groq
    except ImportError as exc:
        raise ValueError("groq package is not installed. Run 'pip install groq'.") from exc

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in the environment")
    return Groq(api_key=api_key)


def call_llm(prompt: str) -> str:
    """
    Call Groq LLM with the provided prompt.

    Args:
        prompt: The input prompt for the LLM

    Returns:
        The response text from the LLM, or an error message if the API call fails
    """
    try:
        client = _get_client()
        message = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
        )
        return message.choices[0].message.content
    except Exception as exc:
        if __name__ == "__main__":
            print("DEBUG:", repr(exc))
        return "Error generating response"


if __name__ == "__main__":
    print(call_llm("Explain binary search in one line"))

