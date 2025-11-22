"""
Kalpana AGI - Email Integration Module (Local Storage)
Purpose: Email management with local storage (personal use - demo mode)
"""

import logging
import os
import json
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger("Kalpana.Email")

class EmailManager:
    def __init__(self):
        self.emails_file = os.path.join(os.path.dirname(__file__), "../data/emails.json")
        self.emails = []
        self._load_emails()
    
    def _load_emails(self):
        """Load emails from JSON file."""
        try:
            os.makedirs(os.path.dirname(self.emails_file), exist_ok=True)
            if os.path.exists(self.emails_file):
                with open(self.emails_file, 'r') as f:
                    self.emails = json.load(f)
                logger.info(f"Loaded {len(self.emails)} emails")
        except Exception as e:
            logger.error(f"Email load error: {e}")
            self.emails = []
    
    def _save_emails(self):
        """Save emails to JSON file."""
        try:
            with open(self.emails_file, 'w') as f:
                json.dump(self.emails, f, indent=2)
            logger.info("Emails saved")
        except Exception as e:
            logger.error(f"Email save error: {e}")
    
    def send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Send an email (saves to local storage for demo)."""
        try:
            email = {
                'id': f"email_{len(self.emails) + 1}",
                'to': to,
                'from': 'kalpana@local',
                'subject': subject,
                'body': body,
                'date': datetime.now().isoformat(),
                'type': 'sent'
            }
            
            self.emails.append(email)
            self._save_emails()
            
            logger.info(f"Sent email to {to}")
            return {"status": "success", "message": "Email sent (local storage)"}
            
        except Exception as e:
            logger.error(f"Send email error: {e}")
            return {"status": "error", "message": str(e)}
    
    def read_emails(self, max_count: int = 10) -> List[Dict[str, Any]]:
        """Read recent emails."""
        try:
            # Return most recent emails
            recent = sorted(self.emails, key=lambda x: x['date'], reverse=True)
            logger.info(f"Read {len(recent[:max_count])} emails")
            return recent[:max_count]
            
        except Exception as e:
            logger.error(f"Read emails error: {e}")
            return []

email_manager = EmailManager()

