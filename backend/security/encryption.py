"""
Kalpana AGI - Encryption Module
Purpose: AES-256 encryption for conversation logs and sensitive data.
Dependencies: cryptography
"""

import logging
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
import base64

logger = logging.getLogger("Kalpana.Encryption")

class EncryptionManager:
    def __init__(self):
        self.key_file = os.path.join(os.path.dirname(__file__), "../data/encryption.key")
        self.key = None
        self.fernet = None
        self._initialize()
    
    def _initialize(self):
        """Initialize encryption key."""
        try:
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            
            if os.path.exists(self.key_file):
                # Load existing key
                with open(self.key_file, 'rb') as f:
                    self.key = f.read()
            else:
                # Generate new key
                self.key = Fernet.generate_key()
                with open(self.key_file, 'wb') as f:
                    f.write(self.key)
                logger.info("Generated new encryption key")
            
            self.fernet = Fernet(self.key)
            logger.info("Encryption initialized")
            
        except Exception as e:
            logger.error(f"Encryption initialization error: {e}")
    
    def encrypt(self, data: str) -> str:
        """Encrypt a string."""
        try:
            encrypted = self.fernet.encrypt(data.encode('utf-8'))
            return base64.b64encode(encrypted).decode('utf-8')
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return ""
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a string."""
        try:
            encrypted = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.fernet.decrypt(encrypted)
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return ""
    
    def encrypt_file(self, file_path: str) -> bool:
        """Encrypt a file in place."""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = self.fernet.encrypt(data)
            
            with open(file_path + '.encrypted', 'wb') as f:
                f.write(encrypted)
            
            logger.info(f"Encrypted file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"File encryption error: {e}")
            return False
    
    def decrypt_file(self, file_path: str, output_path: str) -> bool:
        """Decrypt a file."""
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted = self.fernet.decrypt(encrypted_data)
            
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            logger.info(f"Decrypted file: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"File decryption error: {e}")
            return False

encryption_manager = EncryptionManager()
