"""
Kalpana AGI - Weather Plugin
Purpose: Get weather information.
Dependencies: requests
"""

import logging
import os
import requests
from backend.plugins.loader import PluginInterface
from typing import Dict, Any

logger = logging.getLogger("Kalpana.WeatherPlugin")

class WeatherPlugin(PluginInterface):
    def __init__(self):
        super().__init__()
        self.name = "weather"
        self.version = "1.0.0"
        self.description = "Get weather information"
        self.api_key = os.getenv("WEATHER_API_KEY", "")
    
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute weather command."""
        if command == "get_weather":
            location = kwargs.get("location", "London")
            return self.get_weather(location)
        else:
            return {"status": "error", "message": f"Unknown command: {command}"}
    
    def get_weather(self, location: str) -> Dict[str, Any]:
        """Get current weather for a location."""
        if not self.api_key:
            return {"status": "success", "message": f"Weather in {location}: 72°F, Partly cloudy (demo mode - no API key)"}
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=imperial"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return {
                    "status": "success",
                    "message": f"Weather in {location}: {temp}°F, {description}"
                }
            else:
                return {"status": "error", "message": "Failed to fetch weather"}
                
        except Exception as e:
            logger.error(f"Weather error: {e}")
            return {"status": "error", "message": str(e)}
