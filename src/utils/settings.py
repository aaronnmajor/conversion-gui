"""Settings management for the application."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .logger import get_logger


logger = get_logger(__name__)


class Settings:
    """
    Application settings manager.
    
    Handles loading, saving, and accessing application settings.
    """
    
    def __init__(self, settings_file: Optional[str] = None):
        """
        Initialize the settings manager.
        
        Args:
            settings_file: Path to settings file (defaults to ~/.conversion-gui/settings.json)
        """
        if settings_file is None:
            self.settings_file = Path.home() / ".conversion-gui" / "settings.json"
        else:
            self.settings_file = Path(settings_file)
        
        self._settings: Dict[str, Any] = {}
        self._defaults: Dict[str, Any] = {
            "window": {
                "width": 1280,
                "height": 720,
                "maximized": False
            },
            "theme": "light",
            "log_level": "INFO",
            "plugins_enabled": True,
            "recent_files": [],
            "database": {
                "type": "sqlite",
                "path": ""
            }
        }
        self.load()
    
    def load(self) -> None:
        """Load settings from file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    self._settings = json.load(f)
                logger.info(f"Settings loaded from {self.settings_file}")
            else:
                self._settings = self._defaults.copy()
                logger.info("Using default settings")
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            self._settings = self._defaults.copy()
    
    def save(self) -> None:
        """Save settings to file."""
        try:
            self.settings_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
            logger.info(f"Settings saved to {self.settings_file}")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value.
        
        Args:
            key: Setting key (supports dot notation, e.g., 'window.width')
            default: Default value if key not found
            
        Returns:
            Setting value or default
        """
        keys = key.split('.')
        value = self._settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a setting value.
        
        Args:
            key: Setting key (supports dot notation, e.g., 'window.width')
            value: Value to set
        """
        keys = key.split('.')
        settings = self._settings
        
        for k in keys[:-1]:
            if k not in settings:
                settings[k] = {}
            settings = settings[k]
        
        settings[keys[-1]] = value
    
    def reset(self) -> None:
        """Reset settings to defaults."""
        self._settings = self._defaults.copy()
        logger.info("Settings reset to defaults")
