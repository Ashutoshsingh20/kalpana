"""
Kalpana AGI - Reminders Module
Purpose: Schedule and manage reminders and alarms.
Dependencies: schedule, asyncio
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
import os

logger = logging.getLogger("Kalpana.Reminders")

class ReminderManager:
    def __init__(self):
        self.reminders_file = os.path.join(os.path.dirname(__file__), "../data/reminders.json")
        self.reminders = []
        self.load_reminders()
    
    def load_reminders(self):
        """Load reminders from file."""
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r') as f:
                    self.reminders = json.load(f)
                logger.info(f"Loaded {len(self.reminders)} reminders")
        except Exception as e:
            logger.error(f"Load reminders error: {e}")
            self.reminders = []
    
    def save_reminders(self):
        """Save reminders to file."""
        try:
            os.makedirs(os.path.dirname(self.reminders_file), exist_ok=True)
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f, indent=2)
            logger.info("Reminders saved")
        except Exception as e:
            logger.error(f"Save reminders error: {e}")
    
    def add_reminder(self, message: str, trigger_time: datetime, recurring: bool = False) -> Dict[str, Any]:
        """Add a new reminder."""
        try:
            reminder = {
                'id': len(self.reminders) + 1,
                'message': message,
                'trigger_time': trigger_time.isoformat(),
                'recurring': recurring,
                'active': True,
                'created_at': datetime.now().isoformat()
            }
            
            self.reminders.append(reminder)
            self.save_reminders()
            
            logger.info(f"Added reminder: {message} at {trigger_time}")
            return {"status": "success", "reminder": reminder}
            
        except Exception as e:
            logger.error(f"Add reminder error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_active_reminders(self) -> List[Dict[str, Any]]:
        """Get all active reminders."""
        return [r for r in self.reminders if r.get('active', False)]
    
    def check_due_reminders(self) -> List[Dict[str, Any]]:
        """Check for reminders that are due."""
        now = datetime.now()
        due_reminders = []
        
        for reminder in self.get_active_reminders():
            trigger_time = datetime.fromisoformat(reminder['trigger_time'])
            if trigger_time <= now:
                due_reminders.append(reminder)
                if not reminder.get('recurring', False):
                    reminder['active'] = False
        
        if due_reminders:
            self.save_reminders()
        
        return due_reminders
    
    def delete_reminder(self, reminder_id: int) -> Dict[str, Any]:
        """Delete a reminder."""
        try:
            self.reminders = [r for r in self.reminders if r['id'] != reminder_id]
            self.save_reminders()
            logger.info(f"Deleted reminder {reminder_id}")
            return {"status": "success"}
        except Exception as e:
            logger.error(f"Delete reminder error: {e}")
            return {"status": "error", "message": str(e)}
    
    async def start_monitoring(self, sio):
        """Monitor reminders and emit notifications."""
        logger.info("Started reminder monitoring")
        while True:
            try:
                due = self.check_due_reminders()
                for reminder in due:
                    await sio.emit('reminder_notification', {
                        'message': reminder['message'],
                        'time': reminder['trigger_time']
                    })
                    logger.info(f"Triggered reminder: {reminder['message']}")
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Reminder monitoring error: {e}")
                await asyncio.sleep(60)

reminder_manager = ReminderManager()
