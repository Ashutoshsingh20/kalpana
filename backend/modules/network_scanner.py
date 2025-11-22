"""
Kalpana AGI - Network Scanner Module
Purpose: Scan local network for devices and active connections.
Dependencies: psutil, socket
"""

import psutil
import socket
import logging
from typing import List, Dict

logger = logging.getLogger("Kalpana.NetworkScanner")

class NetworkScanner:
    def get_active_connections(self) -> List[Dict[str, str]]:
        """
        Get list of active network connections on the host.
        """
        connections = []
        try:
            # Get network connections (requires privileges for some details, but basic is fine)
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    connections.append({
                        "local": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "remote": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A",
                        "status": conn.status,
                        "pid": conn.pid
                    })
        except Exception as e:
            logger.error(f"Error scanning connections: {e}")
        return connections[:10] # Return top 10 for display

    def get_local_ip(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except:
            return "127.0.0.1"

network_scanner = NetworkScanner()
