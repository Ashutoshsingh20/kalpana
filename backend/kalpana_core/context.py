"""
Kalpana AGI - Context Retrieval System
Purpose: Fetch relevant memories to inject into LLM context.
Dependencies: memory module
"""

import logging
from typing import List, Dict, Any
from backend.kalpana_core.memory import memory

logger = logging.getLogger("Kalpana.Context")

class ContextRetriever:
    def get_context_for_input(self, user_input: str, max_items: int = 3) -> str:
        """
        Retrieve relevant context for the current user input.
        Returns a formatted string to inject into LLM prompt.
        """
        try:
            context_parts = []
            
            # 1. Get user preferences
            preferences = memory.data.get("preferences", {})
            if preferences:
                prefs_str = ", ".join([f"{k}: {v}" for k, v in preferences.items()])
                context_parts.append(f"User Preferences: {prefs_str}")
            
            # 2. Get relevant past conversations
            relevant_convs = memory.search_conversations(user_input, limit=max_items)
            if relevant_convs:
                conv_strs = []
                for conv in relevant_convs:
                    conv_strs.append(f"User: {conv['user']}\nKalpana: {conv['kalpana']}")
                context_parts.append("Relevant Past Conversations:\n" + "\n---\n".join(conv_strs))
            
            # 3. Get learned facts
            facts = memory.data.get("facts", [])
            if facts:
                recent_facts = facts[-5:]  # Last 5 facts
                facts_str = "\n".join([f"- {f['fact']}" for f in recent_facts])
                context_parts.append(f"Known Facts:\n{facts_str}")
            
            # Combine all context
            if context_parts:
                return "\n\n".join(context_parts)
            else:
                return ""
                
        except Exception as e:
            logger.error(f"Context retrieval error: {e}")
            return ""
    
    def get_conversation_history(self, count: int = 3) -> str:
        """Get recent conversation history for continuity."""
        try:
            recent = memory.get_recent_conversations(count)
            if not recent:
                return ""
            
            history = []
            for conv in recent:
                history.append(f"User: {conv['user']}\nKalpana: {conv['kalpana']}")
            
            return "Recent Conversation:\n" + "\n---\n".join(history)
        except Exception as e:
            logger.error(f"History retrieval error: {e}")
            return ""

context_retriever = ContextRetriever()
