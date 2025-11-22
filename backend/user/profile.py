"""
Kalpana AGI - User Profile Database
Purpose: Store and manage user preferences.
Dependencies: sqlite3
"""

import logging
import os
import sqlite3
from typing import Dict, Any, Optional

logger = logging.getLogger("Kalpana.UserProfile")

class UserProfileDB:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "../data/user_profile.db")
        self.conn = None
        self._initialize()
    
    def _initialize(self):
        """Initialize database."""
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            
            # Create tables
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS preferences (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conn.commit()
            logger.info("User profile database initialized")
            
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def set_preference(self, key: str, value: str) -> bool:
        """Set a user preference."""
        try:
            self.conn.execute(
                'INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)',
                (key, value)
            )
            self.conn.commit()
            logger.info(f"Set preference: {key} = {value}")
            return True
        except Exception as e:
            logger.error(f"Set preference error: {e}")
            return False
    
    def get_preference(self, key: str, default: str = "") -> str:
        """Get a user preference."""
        try:
            cursor = self.conn.execute('SELECT value FROM preferences WHERE key = ?', (key,))
            row = cursor.fetchone()
            return row['value'] if row else default
        except Exception as e:
            logger.error(f"Get preference error: {e}")
            return default
    
    def get_all_preferences(self) -> Dict[str, str]:
        """Get all preferences."""
        try:
            cursor = self.conn.execute('SELECT key, value FROM preferences')
            return {row['key']: row['value'] for row in cursor.fetchall()}
        except Exception as e:
            logger.error(f"Get all preferences error: {e}")
            return {}
    
    def delete_preference(self, key: str) -> bool:
        """Delete a preference."""
        try:
            self.conn.execute('DELETE FROM preferences WHERE key = ?', (key,))
            self.conn.commit()
            logger.info(f"Deleted preference: {key}")
            return True
        except Exception as e:
            logger.error(f"Delete preference error: {e}")
            return False
    
    def set_user_data(self, name: str, email: str) -> bool:
        """Set user data."""
        try:
            self.conn.execute(
                'INSERT OR REPLACE INTO user_data (id, name, email) VALUES (1, ?, ?)',
                (name, email)
            )
            self.conn.commit()
            logger.info(f"Set user data: {name}, {email}")
            return True
        except Exception as e:
            logger.error(f"Set user data error: {e}")
            return False
    
    def get_user_data(self) -> Optional[Dict[str, str]]:
        """Get user data."""
        try:
            cursor = self.conn.execute('SELECT name, email FROM user_data WHERE id = 1')
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Get user data error: {e}")
            return None

user_profile_db = UserProfileDB()
