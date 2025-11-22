"""
Kalpana AGI - System Control Tools
Purpose: Control macOS system functions (Apps, Volume, Brightness).
Dependencies: os, subprocess, osascript (via subprocess)
"""

import os
import subprocess
import logging

logger = logging.getLogger("Kalpana.SystemControl")

class SystemControl:
    
    @staticmethod
    def open_app(app_name: str):
        """Open a macOS application."""
        logger.info(f"Opening app: {app_name}")
        try:
            subprocess.run(["open", "-a", app_name], check=True)
            return True
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return False

    @staticmethod
    def set_volume(level: int):
        """Set system volume (0-100)."""
        # macOS volume is 0-7 usually, or 0-100 via AppleScript
        logger.info(f"Setting volume to: {level}")
        script = f"set volume output volume {level}"
        try:
            subprocess.run(["osascript", "-e", script])
            return True
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return False

    @staticmethod
    def say_system(text: str):
        """Use macOS built-in 'say' command as a fallback TTS."""
        subprocess.run(["say", text])

system_control = SystemControl()
