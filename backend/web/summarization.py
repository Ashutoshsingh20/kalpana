"""
Kalpana AGI - Summarization Module
Purpose: Summarize text content using LLM.
Dependencies: openai or similar LLM API
"""

import logging
import os
from typing import List

logger = logging.getLogger("Kalpana.Summarization")

class Summarizer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.use_llm = bool(self.api_key)
    
    def summarize_with_llm(self, text: str, max_length: int = 200) -> str:
        """
        Summarize text using OpenAI API.
        """
        try:
            import openai
            openai.api_key = self.api_key
            
            prompt = f"Summarize the following text in {max_length} words or less:\n\n{text[:4000]}"
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length * 2,
                temperature=0.5
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Summarized {len(text)} chars to {len(summary)} chars using LLM")
            return summary
            
        except Exception as e:
            logger.error(f"LLM summarization error: {e}")
            return self.summarize_extractive(text, max_length)
    
    def summarize_extractive(self, text: str, max_length: int = 200) -> str:
        """
        Simple extractive summarization (first N sentences).
        """
        try:
            sentences = text.split('. ')
            summary = []
            total_words = 0
            
            for sentence in sentences:
                words = sentence.split()
                if total_words + len(words) > max_length:
                    break
                summary.append(sentence)
                total_words += len(words)
            
            result = '. '.join(summary) + '.'
            logger.info(f"Extractive summary: {total_words} words")
            return result
            
        except Exception as e:
            logger.error(f"Extractive summarization error: {e}")
            return text[:max_length * 6]  # Rough char estimate
    
    def summarize(self, text: str, max_length: int = 200) -> str:
        """
        Summarize text using the best available method.
        """
        if self.use_llm:
            return self.summarize_with_llm(text, max_length)
        else:
            return self.summarize_extractive(text, max_length)
    
    def summarize_with_citations(self, search_results: List[dict]) -> str:
        """
        Summarize search results and add citations.
        """
        try:
            combined_text = ""
            citations = []
            
            for idx, result in enumerate(search_results[:3], 1):
                snippet = result.get('snippet', '')
                title = result.get('title', '')
                url = result.get('url', '')
                
                combined_text += f"{snippet} "
                citations.append(f"[{idx}] {title} - {url}")
            
            summary = self.summarize(combined_text, max_length=150)
            
            # Add citations
            result = f"{summary}\n\nSources:\n" + "\n".join(citations)
            return result
            
        except Exception as e:
            logger.error(f"Citation summarization error: {e}")
            return "Failed to summarize search results."

summarizer = Summarizer()
