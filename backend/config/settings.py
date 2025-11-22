"""
Kalpana AGI - Configuration Settings
Purpose: Centralized configuration management.
Dependencies: python-dotenv, pydantic (optional but good practice, using stdlib for now to keep it simple as per spec requirements list)
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    PROJECT_ROOT = BASE_DIR  # Alias for compatibility
    BACKEND_DIR = BASE_DIR / "backend"
    FRONTEND_DIR = BASE_DIR / "frontend"
    PLUGINS_DIR = BACKEND_DIR / "plugins"
    MEMORY_DIR = BACKEND_DIR / "memory_store"
    ENCRYPTED_MEMORY_DIR = MEMORY_DIR / "encrypted" # New path for encrypted memory storage
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8001))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "kalpana-super-secret-key-change-in-prod")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "") # Should be set in .env
    
    # AI / LLM
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-r1:1.5b")
    LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:11434") # Ollama default
    
    # Voice
    WAKE_WORD = "kalpana"
    VOICE_ID = os.getenv("VOICE_ID", "com.apple.speech.synthesis.voice.Alex")
    
    # System
    PLATFORM = "darwin" # macOS
    
    @classmethod
    def ensure_dirs(cls):
        """Ensure critical directories exist"""
        cls.MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        cls.PLUGINS_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
settings.ensure_dirs()
