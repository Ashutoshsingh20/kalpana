"""
Kalpana AGI - Calendar Integration Module (Local Storage)
Purpose: Manage calendar events using local JSON storage (personal use)
"""

import logging
import os
import json
from datetime import datetime
from typing import List, Dict, Any

logger = logging.getLogger("Kalpana.Calendar")

class CalendarManager:
    def __init__(self):
        self.events_file = os.path.join(os.path.dirname(__file__), "../data/calendar_events.json")
        self.events = []
        self._load_events()
    
    def _load_events(self):
        """Load events from JSON file."""
        try:
            os.makedirs(os.path.dirname(self.events_file), exist_ok=True)
            if os.path.exists(self.events_file):
                with open(self.events_file, 'r') as f:
                    self.events = json.load(f)
                logger.info(f"Loaded {len(self.events)} calendar events")
        except Exception as e:
            logger.error(f"Calendar load error: {e}")
            self.events = []
    
    def _save_events(self):
        """Save events to JSON file."""
        try:
            with open(self.events_file, 'w') as f:
                json.dump(self.events, f, indent=2)
            logger.info("Calendar events saved")
        except Exception as e:
            logger.error(f"Calendar save error: {e}")
    
    def create_event(self, summary: str, start_time: datetime, end_time: datetime, description: str = "") -> Dict[str, Any]:
        """Create a calendar event."""
        try:
            event_id = f"event_{len(self.events) + 1}"
            event = {
                'id': event_id,
                'summary': summary,
                'description': description,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'created_at': datetime.now().isoformat()
            }
            
            self.events.append(event)
            self._save_events()
            
            logger.info(f"Created event: {summary}")
            return {"status": "success", "event_id": event_id}
            
        except Exception as e:
            logger.error(f"Create event error: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_upcoming_events(self, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get upcoming events."""
        try:
            now = datetime.now()
            upcoming = [
                e for e in self.events
                if datetime.fromisoformat(e['start_time']) >= now
            ]
            upcoming.sort(key=lambda x: x['start_time'])
            
            logger.info(f"Retrieved {len(upcoming[:max_results])} upcoming events")
            return upcoming[:max_results]
            
        except Exception as e:
            logger.error(f"Get events error: {e}")
            return []
    
    def delete_event(self, event_id: str) -> Dict[str, Any]:
        """Delete a calendar event."""
        try:
            self.events = [e for e in self.events if e['id'] != event_id]
            self._save_events()
            logger.info(f"Deleted event: {event_id}")
            return {"status": "success"}
            
        except Exception as e:
            logger.error(f"Delete event error: {e}")
            return {"status": "error", "message": str(e)}

calendar_manager = CalendarManager()

