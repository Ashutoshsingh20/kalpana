"""
Kalpana AGI - Plugin System
Purpose: Dynamic plugin loading and management.
Dependencies: importlib
"""

import logging
import os
import importlib
import inspect
from typing import Dict, Any, List, Callable

logger = logging.getLogger("Kalpana.Plugins")

class PluginInterface:
    """Base interface for plugins."""
    
    def __init__(self):
        self.name = "base_plugin"
        self.version = "1.0.0"
        self.description = "Base plugin interface"
    
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute plugin command."""
        raise NotImplementedError("Plugin must implement execute method")
    
    def get_info(self) -> Dict[str, str]:
        """Get plugin information."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description
        }

class PluginLoader:
    """Dynamic plugin loader."""
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugins_dir = os.path.join(os.path.dirname(__file__), ".")
    
    def load_plugin(self, plugin_name: str) -> bool:
        """Load a plugin by name."""
        try:
            # Try to import the plugin module
            module = importlib.import_module(f"backend.plugins.{plugin_name}")
            
            # Find plugin class (should inherit from PluginInterface)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, PluginInterface) and obj != PluginInterface:
                    plugin_instance = obj()
                    self.plugins[plugin_instance.name] = plugin_instance
                    logger.info(f"Loaded plugin: {plugin_instance.name}")
                    return True
            
            logger.warning(f"No valid plugin class found in {plugin_name}")
            return False
            
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {e}")
            return False
    
    def load_all_plugins(self):
        """Load all available plugins."""
        try:
            plugin_files = [
                f[:-3] for f in os.listdir(self.plugins_dir)
                if f.endswith('.py') and f not in ['__init__.py', '__pycache__', 'loader.py']
            ]
            
            for plugin_file in plugin_files:
                self.load_plugin(plugin_file)
            
            logger.info(f"Loaded {len(self.plugins)} plugins")
            
        except Exception as e:
            logger.error(f"Failed to load plugins: {e}")
    
    def get_plugin(self, name: str) -> PluginInterface:
        """Get a loaded plugin by name."""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[Dict[str, str]]:
        """List all loaded plugins."""
        return [plugin.get_info() for plugin in self.plugins.values()]
    
    def execute_plugin(self, plugin_name: str, command: str, **kwargs) -> Dict[str, Any]:
        """Execute a command on a plugin."""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return {"status": "error", "message": f"Plugin '{plugin_name}' not found"}
        
        try:
            result = plugin.execute(command, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Plugin execution error: {e}")
            return {"status": "error", "message": str(e)}

plugin_loader = PluginLoader()
