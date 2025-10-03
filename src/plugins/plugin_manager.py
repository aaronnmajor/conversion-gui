"""Plugin manager for loading and managing plugins."""

import importlib.util
import sys
from pathlib import Path
from typing import Dict, List, Optional

from .plugin_interface import PluginInterface
from ..utils.logger import get_logger


logger = get_logger(__name__)


class PluginManager:
    """
    Plugin manager for discovering, loading, and managing plugins.
    """
    
    def __init__(self, plugin_dir: Optional[str] = None):
        """
        Initialize the plugin manager.
        
        Args:
            plugin_dir: Directory containing plugins (defaults to ~/.conversion-gui/plugins)
        """
        if plugin_dir is None:
            self.plugin_dir = Path.home() / ".conversion-gui" / "plugins"
        else:
            self.plugin_dir = Path(plugin_dir)
        
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
        
        self._plugins: Dict[str, PluginInterface] = {}
        self._enabled_plugins: set = set()
    
    def discover_plugins(self) -> List[str]:
        """
        Discover available plugins in the plugin directory.
        
        Returns:
            List of discovered plugin names
        """
        discovered = []
        
        if not self.plugin_dir.exists():
            return discovered
        
        for path in self.plugin_dir.glob("*.py"):
            if path.stem.startswith("_"):
                continue
            discovered.append(path.stem)
        
        logger.info(f"Discovered {len(discovered)} plugins")
        return discovered
    
    def load_plugin(self, plugin_name: str) -> bool:
        """
        Load a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to load
            
        Returns:
            True if plugin loaded successfully, False otherwise
        """
        plugin_path = self.plugin_dir / f"{plugin_name}.py"
        
        if not plugin_path.exists():
            logger.error(f"Plugin file not found: {plugin_path}")
            return False
        
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
            if spec is None or spec.loader is None:
                logger.error(f"Could not load spec for plugin: {plugin_name}")
                return False
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)
            
            # Find plugin class
            plugin_class = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (isinstance(item, type) and 
                    issubclass(item, PluginInterface) and 
                    item is not PluginInterface):
                    plugin_class = item
                    break
            
            if plugin_class is None:
                logger.error(f"No plugin class found in {plugin_name}")
                return False
            
            plugin_instance = plugin_class()
            self._plugins[plugin_name] = plugin_instance
            logger.info(f"Loaded plugin: {plugin_instance.name} v{plugin_instance.version}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading plugin {plugin_name}: {e}", exc_info=True)
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        Unload a plugin by name.
        
        Args:
            plugin_name: Name of the plugin to unload
            
        Returns:
            True if plugin unloaded successfully, False otherwise
        """
        if plugin_name not in self._plugins:
            return False
        
        try:
            plugin = self._plugins[plugin_name]
            plugin.cleanup()
            del self._plugins[plugin_name]
            self._enabled_plugins.discard(plugin_name)
            logger.info(f"Unloaded plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Error unloading plugin {plugin_name}: {e}")
            return False
    
    def enable_plugin(self, plugin_name: str, app_context) -> bool:
        """
        Enable a plugin.
        
        Args:
            plugin_name: Name of the plugin to enable
            app_context: Application context
            
        Returns:
            True if plugin enabled successfully, False otherwise
        """
        if plugin_name not in self._plugins:
            if not self.load_plugin(plugin_name):
                return False
        
        try:
            plugin = self._plugins[plugin_name]
            plugin.initialize(app_context)
            self._enabled_plugins.add(plugin_name)
            logger.info(f"Enabled plugin: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Error enabling plugin {plugin_name}: {e}")
            return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """
        Disable a plugin.
        
        Args:
            plugin_name: Name of the plugin to disable
            
        Returns:
            True if plugin disabled successfully, False otherwise
        """
        if plugin_name not in self._enabled_plugins:
            return False
        
        self._enabled_plugins.discard(plugin_name)
        logger.info(f"Disabled plugin: {plugin_name}")
        return True
    
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """
        Get a plugin instance by name.
        
        Args:
            plugin_name: Name of the plugin
            
        Returns:
            Plugin instance or None
        """
        return self._plugins.get(plugin_name)
    
    def get_enabled_plugins(self) -> List[PluginInterface]:
        """
        Get all enabled plugins.
        
        Returns:
            List of enabled plugin instances
        """
        return [self._plugins[name] for name in self._enabled_plugins if name in self._plugins]
    
    def get_all_plugins(self) -> List[PluginInterface]:
        """
        Get all loaded plugins.
        
        Returns:
            List of all plugin instances
        """
        return list(self._plugins.values())
