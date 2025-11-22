# processor.py
"""Processor for handling user utterances.
It uses the simple keyword‑based intent detection from `intents.py`
and returns a canned response for each recognized intent.
Future work: replace with LLM‑based NLU and context handling.
"""

from .intents import get_intent

# Simple response mapping for demonstration purposes
INTENT_RESPONSES = {
    "greeting": "Hello! How can I assist you today?",
    "weather": "Sure, let me check the weather for you.",
    "time": "The current time is {time}.",
    "joke": "Why did the robot go to therapy? Because it had too many bytes!",
    "reminder": "I have set a reminder for you.",
    "unknown": "I'm sorry, I didn't understand that. Could you rephrase?",
}


def process_input(text: str) -> str:
    """Determine intent and return an appropriate response.

    Args:
        text: The raw user utterance.
    Returns:
        A string response suitable for TTS.
    """
    intent = get_intent(text)
    response_template = INTENT_RESPONSES.get(intent, INTENT_RESPONSES["unknown"])
    if intent == "time":
        from datetime import datetime
        current_time = datetime.now().strftime("%I:%M %p")
        return response_template.format(time=current_time)
    return response_template
