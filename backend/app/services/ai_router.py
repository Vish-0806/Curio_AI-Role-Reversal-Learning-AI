"""
Curio AI — AI Router (Provider Abstraction).

Architecture:
    AIClient (Protocol) <- MockAIClient / GroqAIClient / ...
    get_ai_client(settings) -> AIClient (factory)
    AIRouter.generate(payload) -> normalized dict
"""

import json
import random
from typing import Any, Dict, List, Protocol, runtime_checkable

import httpx

from app.config.settings import Settings, get_settings
from app.utils.error_handler import AIProviderError
from app.utils.logger import get_logger

logger = get_logger(__name__)

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


@runtime_checkable
class AIClient(Protocol):
    """Interface for AI provider clients."""
    def generate(self, payload: Dict[str, Any]) -> Dict[str, Any]: ...


# ═══════════════════════════════════════════════════════════════════
#  Groq AI Client (real provider)
# ═══════════════════════════════════════════════════════════════════

class GroqAIClient:
    """Groq API client using their OpenAI-compatible endpoint."""

    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile"):
        self._api_key = api_key
        self._model = model

    def generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Call Groq API and parse the JSON response."""
        # Build messages array for the chat completions API
        messages: List[Dict[str, str]] = [
            {"role": "system", "content": payload["system_prompt"]},
        ]

        # Add conversation history
        for turn in payload.get("conversation_history", []):
            role = turn["role"]
            if role == "user":
                messages.append({"role": "user", "content": turn["content"]})
            elif role == "ai":
                messages.append({"role": "assistant", "content": turn["content"]})
            elif role == "system":
                messages.append({"role": "system", "content": turn["content"]})

        # Add the current user message
        messages.append({"role": "user", "content": payload["user_message"]})

        # Call Groq API
        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    GROQ_API_URL,
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self._model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 1024,
                        "response_format": {"type": "json_object"},
                    },
                )
                response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error("Groq API HTTP error", extra={
                "status": e.response.status_code,
                "body": e.response.text[:500],
            })
            raise AIProviderError(
                message=f"Groq API error: {e.response.status_code}",
                details={"status": e.response.status_code},
            )
        except httpx.RequestError as e:
            logger.error("Groq API request error", extra={"error": str(e)})
            raise AIProviderError(message=f"Groq API connection error: {e}")

        # Parse response
        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # Parse the JSON content from the LLM
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            logger.warning("Groq returned non-JSON, using raw text", extra={"content": content[:200]})
            parsed = {
                "ai_message": content,
                "ai_intent": "acknowledgment",
                "followups": [],
                "flags": {"needs_example": False, "detected_gap": False},
            }

        logger.info("Groq response received", extra={
            "model": self._model,
            "intent": parsed.get("ai_intent", "unknown"),
        })
        return parsed


# ═══════════════════════════════════════════════════════════════════
#  Mock AI Client (for testing without API keys)
# ═══════════════════════════════════════════════════════════════════

class MockAIClient:
    """Deterministic mock AI client for development/testing."""

    _RESPONSES = {
        "question": [
            "Can you explain what happens when {topic} encounters an edge case?",
            "How does this relate to the bigger picture of {topic}?",
            "Could you break that down more? I want to understand the fundamentals.",
        ],
        "challenge": [
            "Are you sure? I thought the opposite might be true for {topic}.",
            "Doesn't that contradict what you said earlier?",
        ],
        "mistake": [
            "So {topic} basically means everything is the same, right?",
            "So {topic} has no exceptions at all? That seems too simple.",
        ],
        "acknowledgment": [
            "Clear explanation! I think I'm starting to get {topic}.",
            "That clicks! The example really helped.",
        ],
        "follow_up": [
            "Can you give me a real-world example?",
            "How would a beginner apply this in practice?",
        ],
    }

    _FOLLOWUPS = [
        "Can you give me an example?",
        "How does this compare to similar concepts?",
        "What's the most common mistake people make?",
        "Why is this important?",
    ]

    def generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        meta = payload.get("metadata", {})
        mode = meta.get("mode", "teach")
        topic = meta.get("topic", "this concept")
        turn_count = meta.get("turn_count", 0)
        user_msg = payload.get("user_message", "")

        intents = ["question", "acknowledgment", "challenge", "follow_up", "mistake"]
        intent = intents[turn_count % len(intents)]
        if mode == "quiz":
            intent = "question"
        elif mode == "review":
            intent = "acknowledgment"

        templates = self._RESPONSES.get(intent, self._RESPONSES["acknowledgment"])
        ai_message = templates[turn_count % len(templates)].format(topic=topic)

        needs_example = "example" not in user_msg.lower() and turn_count > 1
        detected_gap = len(user_msg) < 50 and turn_count > 2

        n = min(2, max(0, 3 - turn_count))
        followups = random.sample(self._FOLLOWUPS, min(n, len(self._FOLLOWUPS)))

        return {
            "ai_message": ai_message,
            "ai_intent": intent,
            "followups": followups,
            "flags": {"needs_example": needs_example, "detected_gap": detected_gap},
        }


# ═══════════════════════════════════════════════════════════════════
#  Factory + Router
# ═══════════════════════════════════════════════════════════════════

def get_ai_client(settings: Settings | None = None) -> AIClient:
    """Factory: return AI client based on settings.AI_PROVIDER."""
    if settings is None:
        settings = get_settings()
    provider = settings.AI_PROVIDER.lower()

    if provider == "mock":
        logger.info("Using MockAIClient")
        return MockAIClient()
    elif provider == "groq":
        if not settings.GROQ_API_KEY:
            raise AIProviderError(
                message="GROQ_API_KEY is required when AI_PROVIDER=groq",
            )
        logger.info("Using GroqAIClient", extra={"model": settings.AI_MODEL})
        return GroqAIClient(api_key=settings.GROQ_API_KEY, model=settings.AI_MODEL)
    else:
        raise AIProviderError(
            message=f"Unsupported AI provider: '{provider}'",
            details={"supported_providers": ["mock", "groq"]},
        )


class AIRouter:
    """Routes requests to configured provider, normalizes output."""

    def __init__(self, client: AIClient | None = None):
        self._client = client or get_ai_client()

    def generate(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            raw = self._client.generate(payload)
        except AIProviderError:
            raise
        except Exception as e:
            logger.error("AI provider failed", extra={"error": str(e)}, exc_info=True)
            raise AIProviderError(message=f"AI provider error: {e}")

        normalized = {
            "ai_message": raw.get("ai_message", "I'm having trouble responding."),
            "ai_intent": raw.get("ai_intent", "acknowledgment"),
            "followups": raw.get("followups", []),
            "flags": raw.get("flags", {"needs_example": False, "detected_gap": False}),
        }
        logger.info("AI response generated", extra={"intent": normalized["ai_intent"]})
        return normalized
