"""
Kalpana AGI - Smart Home Control (In-Memory Simulation)  
Purpose: Control IoT devices with simulated MQTT (personal use - no broker needed)
"""

import logging
from typing import Dict, Any
import json
from datetime import datetime

logger = logging.getLogger("Kalpana.SmartHome")

class SmartHomeBridge:
    def __init__(self):
        self.connected = True  # Always connected (simulation)
        self.devices = {}
        self.message_log = []
        logger.info("Smart Home Bridge initialized (simulation mode)")
    
    def publish(self, topic: str, payload: Any) -> Dict[str, Any]:
        """Publish message to topic (simulated)."""
        try:
            if isinstance(payload, dict):
                payload_str = json.dumps(payload)
            else:
                payload_str = str(payload)
            
            # Log the message
            message = {
                'topic': topic,
                'payload': payload_str,
                'timestamp': datetime.now().isoformat()
            }
            self.message_log.append(message)
            
            # Update device state
            if 'lights' in topic:
                device_id = topic.split('/')[-2] if '/' in topic else 'unknown'
                self.devices[device_id] = payload
            elif 'thermostat' in topic:
                self.devices['thermostat'] = payload
            
            logger.info(f"Published to {topic}: {payload_str}")
            return {"status": "success"}
                
        except Exception as e:
            logger.error(f"Publish error: {e}")
            return {"status": "error", "message": str(e)}
    
    def control_light(self, device_id: str, state: str) -> Dict[str, Any]:
        """Control a light (on/off/dim)."""
        topic = f"home/lights/{device_id}/command"
        return self.publish(topic, {"state": state})
    
    def control_thermostat(self, temperature: float) -> Dict[str, Any]:
        """Set thermostat temperature."""
        topic = "home/thermostat/set_temperature"
        return self.publish(topic, {"temperature": temperature})
    
    def get_device_status(self, device_id: str) -> Dict[str, Any]:
        """Get device status."""
        if device_id in self.devices:
            return {"status": "success", "state": self.devices[device_id]}
        return {"status": "unknown", "message": "Device not found"}
    
    def get_all_devices(self) -> Dict[str, Any]:
        """Get all device states."""
        return self.devices
    
    def get_message_log(self, max_count: int = 10) -> list:
        """Get recent message log."""
        return self.message_log[-max_count:]

mqtt_bridge = SmartHomeBridge()

