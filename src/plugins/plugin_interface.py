"""Plugin interface definition."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class PluginInterface(ABC):
    """
    Base interface for all plugins.
    
    All plugins must inherit from this class and implement the required methods.
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get plugin name."""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Get plugin version."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get plugin description."""
        pass
    
    @abstractmethod
    def initialize(self, app_context: Any) -> None:
        """
        Initialize the plugin.
        
        Args:
            app_context: Application context object
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass
    
    def get_menu_items(self) -> list:
        """
        Get menu items to add to the application.
        
        Returns:
            List of menu item definitions
        """
        return []
    
    def get_toolbar_items(self) -> list:
        """
        Get toolbar items to add to the application.
        
        Returns:
            List of toolbar item definitions
        """
        return []
    
    def get_settings_widget(self) -> Optional[Any]:
        """
        Get settings widget for this plugin.
        
        Returns:
            Settings widget or None
        """
        return None
