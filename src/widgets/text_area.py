"""Text area widget with enhanced features."""

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class TextArea(QPlainTextEdit):
    """
    Enhanced text area widget with additional features.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the text area widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Set monospace font
        font = QFont("Courier New", 10)
        self.setFont(font)
        
        # Enable line wrap
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
    
    def setText(self, text: str) -> None:
        """
        Set text content.
        
        Args:
            text: Text to set
        """
        self.setPlainText(text)
    
    def getText(self) -> str:
        """
        Get text content.
        
        Returns:
            Current text content
        """
        return self.toPlainText()
    
    def appendText(self, text: str) -> None:
        """
        Append text to the content.
        
        Args:
            text: Text to append
        """
        self.appendPlainText(text)
    
    def clearText(self) -> None:
        """Clear all text content."""
        self.clear()
    
    def setReadOnly(self, read_only: bool) -> None:
        """
        Set read-only mode.
        
        Args:
            read_only: Whether to enable read-only mode
        """
        super().setReadOnly(read_only)
        if read_only:
            self.setStyleSheet("QPlainTextEdit { background-color: #f5f5f5; }")
        else:
            self.setStyleSheet("")
