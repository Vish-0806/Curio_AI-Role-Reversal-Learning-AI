from dotenv import load_dotenv
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any

ROOT_DIR = Path(__file__).resolve().parents[3]
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
            model=os.getenv("AI_MODEL", "llama-3.1-8b-instant"),
            messages=[{"role": "user", "content": prompt}],
        )
        return message.choices[0].message.content
    except Exception as exc:
        print(f"ERROR in call_llm: {str(exc)}")
        return "Error generating response"


def call_llm_structured(
    prompt: str,
    json_schema: Optional[Dict[str, Any]] = None,
    max_tokens: int = 1000,
) -> str:
    """
    Call Groq LLM with support for structured/JSON responses.
    
    Args:
        prompt: The input prompt for the LLM
        json_schema: Optional JSON schema for response validation
        max_tokens: Maximum tokens in response
        
    Returns:
        The response text from the LLM, parsed if JSON schema provided
    """
    try:
        client = _get_client()
        
        # Build the messages with JSON schema if provided
        messages = [{"role": "user", "content": prompt}]
        
        create_params = {
            "model": os.getenv("AI_MODEL", "llama-3.1-8b-instant"),
            "messages": messages,
            "max_tokens": max_tokens,
        }
        
        # Add JSON schema if provided (for structured outputs)
        if json_schema:
            create_params["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "schema": json_schema,
                    "strict": True
                }
            }
        
        message = client.chat.completions.create(**create_params)
        response_text = message.choices[0].message.content
        
        return response_text
        
    except Exception as exc:
        print(f"ERROR in call_llm: {str(exc)}")
        return "Error generating response"


def call_llm_with_system_prompt(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 1500,
) -> str:
    """
    Call Groq LLM with explicit system prompt for better control.
    
    Args:
        system_prompt: System-level instruction
        user_prompt: User message
        max_tokens: Maximum tokens in response
        
    Returns:
        The response text from the LLM
    """
    try:
        client = _get_client()
        message = client.chat.completions.create(
            model=os.getenv("AI_MODEL", "llama-3.1-8b-instant"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=max_tokens,
        )
        return message.choices[0].message.content
    except Exception as exc:
        print(f"ERROR in call_llm: {str(exc)}")
        return "Error generating response"


if __name__ == "__main__":
    print(call_llm("Explain binary search in one line"))

