"""
Kalpana AGI - Firewall Manager (Section T)
Purpose: macOS packet filter (pfctl) wrapper for network security
Dependencies: None (uses subprocess for pfctl)
Permissions: Requires sudo/admin access
"""

import logging
import subprocess
from typing import List, Dict, Any

logger = logging.getLogger("Kalpana.FirewallManager")

class FirewallManager:
    def __init__(self):
        self.pf_conf = "/etc/pf.conf"
        logger.info("Firewall Manager initialized")
    
    def get_status(self) -> Dict[str, Any]:
        """Get current firewall status."""
        try:
            result = subprocess.run(
                ['sudo', 'pfctl', '-s', 'info'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            enabled = "Status: Enabled" in result.stdout
            
            return {
                "enabled": enabled,
                "status": "Active" if enabled else "Inactive",
                "message": "Firewall is protecting your system" if enabled else "Firewall is disabled"
            }
        except subprocess.TimeoutExpired:
            logger.error("Firewall status check timed out")
            return {"enabled": False, "status": "Unknown", "message": "Timeout checking firewall"}
        except Exception as e:
            logger.error(f"Failed to get firewall status: {e}")
            return {"enabled": False, "status": "Error", "message": str(e)}
    
    def enable(self) -> bool:
        """Enable the packet filter firewall (requires sudo)."""
        try:
            result = subprocess.run(
                ['sudo', 'pfctl', '-e'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 or "already enabled" in result.stderr.lower():
                logger.info("✅ Firewall enabled")
                return True
            else:
                logger.error(f"Failed to enable firewall: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Enable firewall error: {e}")
            return False
    
    def disable(self) -> bool:
        """Disable the packet filter firewall (requires sudo)."""
        try:
            result = subprocess.run(
                ['sudo', 'pfctl', '-d'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.warning("⚠️ Firewall disabled")
                return True
            else:
                logger.error(f"Failed to disable firewall: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Disable firewall error: {e}")
            return False
    
    def block_port(self, port: int, protocol: str = "tcp") -> bool:
        """
        Block a specific port (requires sudo).
        NOTE: This is a simplified example. Production use would require
        proper pf.conf rule management.
        """
        try:
            logger.info(f"Blocking port {port}/{protocol}")
            # In production, this would add a rule to pf.conf
            # For now, just log the action
            logger.warning(f"Port blocking requires pf.conf modification: {port}/{protocol}")
            return True
        except Exception as e:
            logger.error(f"Block port error: {e}")
            return False
    
    def allow_ip(self, ip_address: str) -> bool:
        """Allow traffic from specific IP (requires sudo)."""
        try:
            logger.info(f"Whitelisting IP: {ip_address}")
            # Production: add to pf.conf
            logger.warning(f"IP whitelisting requires pf.conf modification: {ip_address}")
            return True
        except Exception as e:
            logger.error(f"Allow IP error: {e}")
            return False
    
    def block_ip(self, ip_address: str) -> bool:
        """Block traffic from specific IP (requires sudo)."""
        try:
            logger.info(f"Blocking IP: {ip_address}")
            # Production: add to pf.conf
            logger.warning(f"IP blocking requires pf.conf modification: {ip_address}")
            return True
        except Exception as e:
            logger.error(f"Block IP error: {e}")
            return False
    
    def flush_rules(self) -> bool:
        """Flush all firewall rules (requires sudo)."""
        try:
            result = subprocess.run(
                ['sudo', 'pfctl', '-F', 'all'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("Firewall rules flushed")
                return True
            else:
                logger.error(f"Failed to flush rules: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Flush rules error: {e}")
            return False

firewall_manager = FirewallManager()
