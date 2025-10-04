"""Error handling utilities for the application."""

import sys
import traceback
from typing import Callable, Optional, Any
from functools import wraps

from PyQt6.QtWidgets import QMessageBox

from .logger import get_logger


logger = get_logger(__name__)


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """
    Global exception handler for uncaught exceptions.
    
    Args:
        exc_type: Exception type
        exc_value: Exception value
        exc_traceback: Exception traceback
    """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logger.critical(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )


def show_error_dialog(
    parent: Optional[Any],
    title: str,
    message: str,
    details: Optional[str] = None
) -> None:
    """
    Display an error dialog to the user.
    
    Args:
        parent: Parent widget
        title: Dialog title
        message: Error message
        details: Optional detailed error information
    """
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    
    if details:
        msg_box.setDetailedText(details)
    
    msg_box.exec()


def error_handler(
    show_dialog: bool = True,
    parent: Optional[Any] = None
) -> Callable:
    """
    Decorator for handling exceptions in functions.
    
    Args:
        show_dialog: Whether to show error dialog
        parent: Parent widget for dialog
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Error in {func.__name__}: {str(e)}",
                    exc_info=True
                )
                if show_dialog:
                    show_error_dialog(
                        parent,
                        "Error",
                        f"An error occurred: {str(e)}",
                        traceback.format_exc()
                    )
                raise
        return wrapper
    return decorator
