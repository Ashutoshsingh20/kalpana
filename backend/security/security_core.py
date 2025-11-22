"""
Kalpana AGI - Enhanced Security Core (Section T)
Purpose: Advanced threat detection, ransomware monitoring, file integrity
Dependencies: watchdog, cryptography
Permissions: File System Read/Write
"""

import logging
import time
import math
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from backend.config.settings import settings

logger = logging.getLogger("Kalpana.SecurityCore")

class SecurityMetrics:
    def __init__(self):
        self.files_modified_last_minute = []
        self.suspicious_extensions = ['.encrypted', '.locked', '.crypto', '.cerber', '.locky']
        self.high_entropy_files = []
        self.threat_score = 0.0
        self.alerts = []
    
    def calculate_entropy(self, data: bytes) -> float:
        """Calculate Shannon entropy of data (measure of randomness)."""
        if not data:
            return 0.0
        
        entropy = 0
        for x in range(256):
            p_x = float(data.count(bytes([x]))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log2(p_x)
        return entropy
    
    def is_high_entropy(self, file_path: Path) -> bool:
        """Check if file has high entropy (likely encrypted)."""
        try:
            data = file_path.read_bytes()[:4096]  # Sample first 4KB
            entropy = self.calculate_entropy(data)
            return entropy > 7.5  # Threshold for encrypted data
        except Exception:
            return False
    
    def update_threat_score(self):
        """Calculate overall threat score (0-100)."""
        score = 0
        
        # Recent rapid file changes
        recent_changes = len([t for t in self.files_modified_last_minute 
                             if datetime.now() - t < timedelta(seconds=5)])
        if recent_changes > 10:
            score += 40
        elif recent_changes > 5:
            score += 20
        
        # Suspicious extensions
        if self.suspicious_extensions:
            score += 30
        
        # High entropy files
        if len(self.high_entropy_files) > 0:
            score += 30
        
        self.threat_score = min(score, 100)
        return self.threat_score

class SecurityEventHandler(FileSystemEventHandler):
    def __init__(self, metrics: SecurityMetrics):
        self.metrics = metrics
        logger.info("Security Event Handler initialized")
    
    def on_modified(self, event):
        if event.is_directory:
            return
        
        try:
            file_path = Path(event.src_path)
            self.metrics.files_modified_last_minute.append(datetime.now())
            
            # Clean up old timestamps (keep last minute only)
            cutoff = datetime.now() - timedelta(minutes=1)
            self.metrics.files_modified_last_minute = [
                t for t in self.metrics.files_modified_last_minute if t > cutoff
            ]
            
            # Check for suspicious extension
            if any(file_path.suffix == ext for ext in self.metrics.suspicious_extensions):
                alert = f"⚠️ Suspicious file extension detected: {file_path.name}"
                self.metrics.alerts.append(alert)
                logger.warning(alert)
            
            # Check for high entropy (encrypted content)
            if file_path.suffix in ['.txt', '.doc', '.pdf'] and file_path.exists():
                if self.metrics.is_high_entropy(file_path):
                    self.metrics.high_entropy_files.append(str(file_path))
                    alert = f"⚠️ High entropy file detected (possible encryption): {file_path.name}"
                    self.metrics.alerts.append(alert)
                    logger.warning(alert)
            
            # Update threat score
            score = self.metrics.update_threat_score()
            if score > 50:
                logger.error(f"🚨 THREAT LEVEL HIGH: {score}/100")
            
        except Exception as e:
            logger.error(f"Security event error: {e}")

class SecurityCore:
    def __init__(self):
        self.monitor_path = settings.PROJECT_ROOT
        self.metrics = SecurityMetrics()
        self.event_handler = SecurityEventHandler(self.metrics)
        self.observer = Observer()
        logger.info(f"Security Core initialized, monitoring: {self.monitor_path}")
    
    def start_protection(self):
        """Start file system monitoring."""
        try:
            self.observer.schedule(self.event_handler, str(self.monitor_path), recursive=True)
            self.observer.start()
            logger.info("🛡️ Security monitoring ACTIVE")
        except Exception as e:
            logger.error(f"Failed to start security monitoring: {e}")
    
    def stop_protection(self):
        """Stop file system monitoring."""
        self.observer.stop()
        self.observer.join()
        logger.info("Security monitoring STOPPED")
    
    def get_status(self):
        """Get current security status."""
        threat_level = "LOW"
        if self.metrics.threat_score > 70:
            threat_level = "CRITICAL"
        elif self.metrics.threat_score > 40:
            threat_level = "HIGH"
        elif self.metrics.threat_score > 20:
            threat_level = "MEDIUM"
        
        return {
            "active": self.observer.is_alive(),
            "threat_level": threat_level,
            "threat_score": self.metrics.threat_score,
            "monitored_path": str(self.monitor_path),
            "recent_alerts": self.metrics.alerts[-5:],  # Last 5 alerts
            "files_modified_last_minute": len(self.metrics.files_modified_last_minute)
        }

security_core = SecurityCore()
