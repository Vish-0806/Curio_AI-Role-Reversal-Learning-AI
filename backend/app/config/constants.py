"""
Curio AI — Non-environment constants.

These are hardcoded values that don't change between environments.
Modify these to tune system behavior without touching business logic.
"""

# ── Version ──────────────────────────────────────────────────────
APP_NAME = "Curio AI"
APP_VERSION = "0.1.0"
API_PREFIX = "/api"

# ── Message Limits ───────────────────────────────────────────────
MAX_USER_MESSAGE_LENGTH = 5000  # characters
MAX_AI_RESPONSE_LENGTH = 3000  # characters
MAX_CONVERSATION_HISTORY = 50  # max turns kept in session
HISTORY_WINDOW_FOR_PROMPT = 10  # last N turns sent to AI

# ── System Prompt Keys ───────────────────────────────────────────
# These keys map to the system prompts used by the prompt builder.
SYSTEM_PROMPT_KEY_TEACH = "teach"
SYSTEM_PROMPT_KEY_QUIZ = "quiz"
SYSTEM_PROMPT_KEY_REVIEW = "review"

DEFAULT_MODE = SYSTEM_PROMPT_KEY_TEACH

# ── System Prompts ───────────────────────────────────────────────
SYSTEM_PROMPTS = {
    SYSTEM_PROMPT_KEY_TEACH: (
        "You are Curio, a curious and enthusiastic AI student. "
        "The user is your teacher and will explain concepts to you. "
        "Your job is to:\n"
        "1. Ask clarifying questions when explanations are unclear.\n"
        "2. Challenge the teacher's logic respectfully to test depth.\n"
        "3. Request concrete examples when concepts are abstract.\n"
        "4. Occasionally make intentional mistakes to see if the teacher catches them.\n"
        "5. Show genuine curiosity and excitement about learning.\n"
        "You must respond in JSON format with keys: "
        "ai_message, ai_intent, followups, flags."
    ),
    SYSTEM_PROMPT_KEY_QUIZ: (
        "You are Curio in quiz mode. Ask the teacher targeted questions "
        "about the topic to assess their understanding depth. "
        "Start simple, then increase complexity. "
        "You must respond in JSON format with keys: "
        "ai_message, ai_intent, followups, flags."
    ),
    SYSTEM_PROMPT_KEY_REVIEW: (
        "You are Curio in review mode. Summarize what you've learned "
        "from the teacher so far, highlighting areas where the explanation "
        "was strong and where gaps remain. "
        "You must respond in JSON format with keys: "
        "ai_message, ai_intent, followups, flags."
    ),
}

# ── AI Intent Types ──────────────────────────────────────────────
AI_INTENTS = [
    "question",      # AI asks a clarifying question
    "challenge",     # AI challenges the teacher's logic
    "hint",          # AI gives a hint or nudge
    "mistake",       # AI intentionally makes a mistake
    "acknowledgment",# AI acknowledges understanding
    "summary",       # AI summarizes what it learned
    "follow_up",     # AI asks a follow-up question
]

# ── Evaluation Rubric ────────────────────────────────────────────
EVALUATION_DIMENSIONS = [
    "clarity",             # How clear is the explanation?
    "correctness_proxy",   # Proxy for factual accuracy (heuristic)
    "examples",            # Did the teacher use examples?
    "depth",               # How deep is the explanation?
    "structure",           # Is the explanation well-structured?
]

EVALUATION_SCORE_MIN = 0.0
EVALUATION_SCORE_MAX = 1.0

# ── Vagueness Markers ────────────────────────────────────────────
VAGUENESS_WORDS = [
    "stuff", "thing", "things", "something", "somehow",
    "kind of", "sort of", "like", "basically", "whatever",
    "etc", "and so on", "you know",
]

# ── Example Indicators ───────────────────────────────────────────
EXAMPLE_INDICATORS = [
    "for example", "e.g.", "for instance", "such as",
    "like when", "consider", "imagine", "suppose",
    "let's say", "to illustrate",
]

# ── Report Constants ─────────────────────────────────────────────
SCHEMA_VERSION = "1.0"
MIN_TURNS_FOR_EVALUATION = 3
