"""
Kalpana AGI - System Monitor Module
Purpose: Collect real-time system statistics (CPU, RAM, Disk, Network).
Dependencies: psutil
"""

import asyncio
import psutil
import logging
from typing import Dict, Any

logger = logging.getLogger("Kalpana.SystemMonitor")

class SystemMonitor:
    def __init__(self):
        self.running = False

    def get_stats(self) -> Dict[str, Any]:
        """
        Fetch current system statistics.
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            battery = psutil.sensors_battery()
            
            stats = {
                "cpu": cpu_percent,
                "ram": ram.percent,
                "disk": disk.percent,
                "battery": battery.percent if battery else 100,
                "power_plugged": battery.power_plugged if battery else True
            }
            return stats
        except Exception as e:
            logger.error(f"Error collecting stats: {e}")
            return {}

    async def start_monitoring(self, sio, interval: int = 2):
        """
        Start the monitoring loop and emit stats via Socket.IO.
        """
        self.running = True
        logger.info("System Monitor started.")
        while self.running:
            stats = self.get_stats()
            await sio.emit('system_stats', stats)
            await asyncio.sleep(interval)

    def stop(self):
        self.running = False

system_monitor = SystemMonitor()
