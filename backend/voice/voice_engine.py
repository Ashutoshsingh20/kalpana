"""
Kalpana AGI - Voice Engine
Purpose: Handle Speech-to-Text (STT) and Text-to-Speech (TTS).
Dependencies: speech_recognition, pyttsx3, pyaudio
"""

import logging
import speech_recognition as sr
import pyttsx3
import asyncio
from backend.config.settings import settings

logger = logging.getLogger("Kalpana.Voice")

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self._configure_voice()
        self.is_listening = False

    def _configure_voice(self):
        """Configure TTS voice settings."""
        try:
            voices = self.engine.getProperty('voices')
            # Try to find the configured voice or default to the first one
            selected_voice = next((v for v in voices if settings.VOICE_ID in v.id), voices[0])
            self.engine.setProperty('voice', selected_voice.id)
            self.engine.setProperty('rate', 180) # Slightly faster than default
        except Exception as e:
            logger.error(f"Error configuring voice: {e}")

    def speak(self, text: str):
        """
        Convert text to speech (Blocking for now, should be threaded in prod).
        """
        logger.info(f"Speaking: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS Error: {e}")

    async def listen(self) -> str:
        """
        Listen for audio input and transcribe it.
        """
        with sr.Microphone() as source:
            logger.info("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Heard: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                return ""
            except sr.UnknownValueError:
                return ""
            except Exception as e:
                logger.error(f"STT Error: {e}")
                return ""

voice_engine = VoiceEngine()
