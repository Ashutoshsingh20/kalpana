"""
Kalpana AGI - Jokes Plugin
Purpose: Tell jokes.
"""

import logging
import random
from backend.plugins.loader import PluginInterface
from typing import Dict, Any

logger = logging.getLogger("Kalpana.JokesPlugin")

JOKES = [
    "Why did the robot go to therapy? Because it had too many bytes!",
    "What do you call a computer that sings? A-Dell!",
    "Why was the computer cold? It left its Windows open!",
    "How does a computer get drunk? It takes screenshots!",
    "Why did the PowerPoint presentation cross the road? To get to the other slide!",
]

class JokesPlugin(PluginInterface):
    def __init__(self):
        super().__init__()
        self.name = "jokes"
        self.version = "1.0.0"
        self.description = "Tell random jokes"
    
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute jokes command."""
        if command == "tell_joke":
            return self.tell_joke()
        else:
            return {"status": "error", "message": f"Unknown command: {command}"}
    
    def tell_joke(self) -> Dict[str, Any]:
        """Tell a random joke."""
        joke = random.choice(JOKES)
        return {"status": "success", "message": joke}
