# intents.py
"""Intent definitions for Kalpana.
This is a lightweight placeholder implementation using keyword matching.
In the future this can be replaced with a transformer model.
"""

# Simple intent mapping: intent name -> list of trigger keywords
INTENT_KEYWORDS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "weather": ["weather", "temperature", "forecast"],
    "time": ["time", "clock", "what time"],
    "joke": ["joke", "funny", "make me laugh"],
    "reminder": ["remind", "reminder", "alert"],
}

def get_intent(text: str) -> str:
    """Return the best‑matching intent for the given text.
    Simple case‑insensitive keyword search; returns "unknown" if no match.
    """
    lowered = text.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for kw in keywords:
            if kw in lowered:
                return intent
    return "unknown"
