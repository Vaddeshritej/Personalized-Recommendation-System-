"""
intent_module.py
Detects user intent from free-text input.
"""

from utils import print_heading

INTENTS = [
    "GENERATE_RECOMMENDATION",
    "REFINE_RECOMMENDATION",
    "SHOW_PROFILE",
    "EXPLAIN_RECOMMENDATION",
    "SAVE_RECOMMENDATION",
    "EXIT",
]

_KEYWORDS = {
    "EXIT": ["exit", "quit", "bye", "stop", "close"],
    "SHOW_PROFILE": ["profile", "my info", "my details", "who am i"],
    "EXPLAIN_RECOMMENDATION": ["explain", "why", "reason"],
    "REFINE_RECOMMENDATION": [
        "refine", "change", "not interested", "different",
        "feedback", "improve", "more like", "prefer"
    ],
    "SAVE_RECOMMENDATION": ["save", "store", "export", "write to file"],
    "GENERATE_RECOMMENDATION": [
        "recommend", "recommendation", "suggest", "generate",
        "new movie", "show me", "movies", "movie"
    ],
}


def detect_intent(user_text: str) -> str:
    """Return the most suitable intent for the user's text."""
    text = (user_text or "").strip().lower()

    if not text:
        return "GENERATE_RECOMMENDATION"

    # Exact command/menu numbers
    number_intents = {
        "1": "GENERATE_RECOMMENDATION",
        "2": "SHOW_PROFILE",
        "3": "EXPLAIN_RECOMMENDATION",
        "4": "REFINE_RECOMMENDATION",
        "5": "SAVE_RECOMMENDATION",
        "6": "EXIT",
    }

    if text in number_intents:
        return number_intents[text]

    # Check specific intents first
    for intent in [
        "EXIT",
        "SHOW_PROFILE",
        "EXPLAIN_RECOMMENDATION",
        "REFINE_RECOMMENDATION",
        "SAVE_RECOMMENDATION",
    ]:
        for keyword in _KEYWORDS[intent]:
            if keyword in text:
                return intent

    # Recommendation request
    for keyword in _KEYWORDS["GENERATE_RECOMMENDATION"]:
        if keyword in text:
            return "GENERATE_RECOMMENDATION"

    # Any other natural-language movie title/request is treated
    # as a new recommendation query.
    return "GENERATE_RECOMMENDATION"


def display_intent(user_text: str, intent: str):
    """Display detected intent."""
    print_heading("INTENT DETECTION")
    print(f"Input   : {user_text}")
    print(f"Intent  : {intent}")