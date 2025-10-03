"""Base screen class for all application screens."""

from abc import ABC, abstractmethod
from typing import Optional

from PyQt6.QtWidgets import QWidget


class BaseScreen(QWidget, ABC):
    """
    Base class for all application screens.
    
    Provides common interface and functionality for all screens.
    """
    
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the base screen.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self._initialized = False
    
    @property
    @abstractmethod
    def screen_name(self) -> str:
        """Get screen name."""
        pass
    
    @property
    @abstractmethod
    def screen_icon(self) -> str:
        """Get screen icon name."""
        pass
    
    @abstractmethod
    def setup_ui(self) -> None:
        """Set up the user interface."""
        pass
    
    @abstractmethod
    def load_data(self) -> None:
        """Load screen data."""
        pass
    
    def initialize(self) -> None:
        """
        Initialize the screen.
        
        Called when the screen is first shown.
        """
        if not self._initialized:
            self.setup_ui()
            self.load_data()
            self._initialized = True
    
    def refresh(self) -> None:
        """
        Refresh screen data.
        
        Called when the screen needs to reload its data.
        """
        if self._initialized:
            self.load_data()
    
    def cleanup(self) -> None:
        """
        Clean up screen resources.
        
        Called when the screen is being closed or destroyed.
        """
        pass
