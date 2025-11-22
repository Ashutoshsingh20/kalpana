"""
Kalpana AGI - Memory Module (Section S)
Purpose: Encrypted storage for conversations, preferences, and learned facts.
Dependencies: cryptography
"""

import json
import logging
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from backend.config.settings import settings

logger = logging.getLogger("Kalpana.Memory")

class Memory:
    def __init__(self):
        self.memory_file = settings.MEMORY_DIR / "memory.enc"
        self.key_file = settings.MEMORY_DIR / "memory.key"
        self.fernet: Optional[Fernet] = None
        self.data: Dict[str, Any] = {
            "conversations": [],
            "preferences": {},
            "facts": [],
            "automations": []
        }
        self._initialize()
    
    def _initialize(self):
        """Initialize encryption and load memory."""
        try:
            # Generate or load encryption key
            if not self.key_file.exists():
                logger.info("Generating new encryption key...")
                key = Fernet.generate_key()
                self.key_file.write_bytes(key)
                logger.info(f"Encryption key saved to: {self.key_file}")
            
            key = self.key_file.read_bytes()
            self.fernet = Fernet(key)
            
            # Load existing memory if available
            if self.memory_file.exists():
                self._load()
            else:
                logger.info("No existing memory found, starting fresh")
                self._save()
                
        except Exception as e:
            logger.error(f"Memory initialization error: {e}")
    
    def _load(self):
        """Load and decrypt memory from disk."""
        try:
            encrypted_data = self.memory_file.read_bytes()
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.data = json.loads(decrypted_data.decode('utf-8'))
            logger.info(f"Memory loaded: {len(self.data['conversations'])} conversations, "
                       f"{len(self.data['facts'])} facts")
        except Exception as e:
            logger.error(f"Memory load error: {e}")
            # Reset to default if corrupted
            self.data = {
                "conversations": [],
                "preferences": {},
                "facts": [],
                "automations": []
            }
    
    def _save(self):
        """Encrypt and save memory to disk."""
        try:
            json_data = json.dumps(self.data, indent=2)
            encrypted_data = self.fernet.encrypt(json_data.encode('utf-8'))
            self.memory_file.write_bytes(encrypted_data)
            logger.debug("Memory saved successfully")
        except Exception as e:
            logger.error(f"Memory save error: {e}")
    
    def save_conversation(self, user_input: str, kalpana_response: str, metadata: Dict = None):
        """Save a conversation exchange."""
        try:
            conversation = {
                "timestamp": datetime.now().isoformat(),
                "user": user_input,
                "kalpana": kalpana_response,
                "metadata": metadata or {}
            }
            self.data["conversations"].append(conversation)
            
            # Apply retention policy (keep last 100 conversations)
            if len(self.data["conversations"]) > 100:
                self.data["conversations"] = self.data["conversations"][-100:]
            
            self._save()
            logger.debug("Conversation saved")
        except Exception as e:
            logger.error(f"Save conversation error: {e}")
    
    def set_preference(self, key: str, value: Any):
        """Set a user preference."""
        try:
            self.data["preferences"][key] = value
            self._save()
            logger.info(f"Preference set: {key} = {value}")
        except Exception as e:
            logger.error(f"Set preference error: {e}")
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Get a user preference."""
        return self.data["preferences"].get(key, default)
    
    def add_fact(self, fact: str, confidence: float = 1.0):
        """Add a learned fact."""
        try:
            fact_entry = {
                "fact": fact,
                "confidence": confidence,
                "learned_at": datetime.now().isoformat()
            }
            self.data["facts"].append(fact_entry)
            self._save()
            logger.info(f"Fact learned: {fact}")
        except Exception as e:
            logger.error(f"Add fact error: {e}")
    
    def get_recent_conversations(self, count: int = 5) -> List[Dict]:
        """Get the N most recent conversations."""
        return self.data["conversations"][-count:]
    
    def search_conversations(self, query: str, limit: int = 3) -> List[Dict]:
        """Search conversations for relevant context."""
        try:
            query_lower = query.lower()
            matches = []
            
            for conv in reversed(self.data["conversations"]):
                if (query_lower in conv["user"].lower() or 
                    query_lower in conv["kalpana"].lower()):
                    matches.append(conv)
                    if len(matches) >= limit:
                        break
            
            return matches
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def clear_all(self):
        """Clear all memory (WARNING: irreversible)."""
        self.data = {
            "conversations": [],
            "preferences": {},
            "facts": [],
            "automations": []
        }
        self._save()
        logger.warning("All memory cleared")
    
    def get_stats(self) -> Dict[str, int]:
        """Get memory statistics."""
        return {
            "conversations": len(self.data["conversations"]),
            "preferences": len(self.data["preferences"]),
            "facts": len(self.data["facts"]),
            "automations": len(self.data["automations"])
        }

# Global instance
memory = Memory()
