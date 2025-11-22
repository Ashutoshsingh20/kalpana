"""
Kalpana AGI - Core Brain
Purpose: Central intelligence, LLM integration, and decision making.
Dependencies: openai, requests
"""

import logging
import json
import asyncio
from typing import List, Dict, Any
from backend.config.settings import settings
from backend.kalpana_core.memory import memory
from backend.kalpana_core.context import context_retriever

logger = logging.getLogger("Kalpana.Brain")

class Brain:
    def __init__(self):
        self.model = settings.LLM_MODEL
        self.context = []
        self.system_prompt = """
        You are Kalpana, an elite AI systems engineer and personal assistant.
        You are running on a macOS system with full control permissions.
        Your goal is to assist the user efficiently, securely, and proactively.
        You have access to various tools for system control, web automation, and file management.
        Always prioritize security and user consent for sensitive actions.
        """
        logger.info(f"Brain initialized with model: {self.model}")

    async def process_input(self, user_input: str, context_data: Dict[str, Any] = None) -> str:
        """
        Process user input and generate a response or action plan.
        """
        logger.info(f"Processing input: {user_input}")
        
        # Retrieve relevant context from memory
        retrieved_context = context_retriever.get_context_for_input(user_input)
        conversation_history = context_retriever.get_conversation_history(count=2)
        
        # Construct messages with memory context
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # Add memory context if available
        if retrieved_context or conversation_history:
            context_message = ""
            if retrieved_context:
                context_message += f"{retrieved_context}\n\n"
            if conversation_history:
                context_message += f"{conversation_history}\n\n"
            messages.append({"role": "system", "content": f"Context from memory:\n{context_message}"})
        
        messages.append({"role": "user", "content": user_input})
        
        # Call LLM
        response = await self._call_llm(messages)
        
        # Save conversation to memory
        memory.save_conversation(user_input, response)
        
        return response

    async def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """
        Internal method to call the LLM provider (Ollama).
        """
        try:
            import requests
            
            # Format prompt for Ollama (DeepSeek might prefer raw text or specific chat format)
            # We'll use the standard /api/chat endpoint if available, or /api/generate
            
            url = f"{settings.LOCAL_LLM_URL}/api/chat"
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False
            }
            
            logger.info(f"Sending request to Ollama: {self.model}")
            
            # Run blocking request in thread
            response = await asyncio.to_thread(requests.post, url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("message", {}).get("content", "")
                logger.info(f"Ollama Response: {content[:50]}...")
                return content
            else:
                logger.error(f"Ollama Error {response.status_code}: {response.text}")
                return f"Error: I could not reach my neural net. (Status {response.status_code})"
                
        except Exception as e:
            logger.error(f"LLM Call Failed: {e}")
            return "Error: My connection to the local model is unstable."

    async def plan_task(self, goal: str):
        """
        Create a multi-step plan for a complex goal (Section L).
        """
        pass

brain = Brain()
