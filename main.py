"""Main application entry point."""

import sys

from PyQt6.QtWidgets import QApplication

from src.core.main_window import MainWindow
from src.utils.error_handler import handle_exception
from src.utils.logger import get_logger


# Set up global exception handler
sys.excepthook = handle_exception

logger = get_logger(__name__)


def main():
    """Main application function."""
    logger.info("Starting Conversion GUI application")
    
    app = QApplication(sys.argv)
    app.setApplicationName("Conversion GUI")
    app.setOrganizationName("ConversionGUI")
    
    window = MainWindow()
    window.show()
    
    logger.info("Application window shown")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
