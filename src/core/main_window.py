"""Main application window."""

from typing import Dict, Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QListWidget, QListWidgetItem,
    QMenuBar, QMenu, QToolBar, QStatusBar, QMessageBox,
    QDialog, QLabel, QTextEdit, QPushButton
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon

from ..screens.dashboard_screen import DashboardScreen
from ..screens.db_browser_screen import DBBrowserScreen
from ..screens.payments_screen import PaymentsScreen
from ..screens.conversion_jobs_screen import ConversionJobsScreen
from ..screens.log_analytics_screen import LogAnalyticsScreen
from ..screens.xml_helper_screen import XMLHelperScreen
from ..screens.search_screen import SearchScreen
from ..utils.settings import Settings
from ..utils.logger import get_logger, setup_logger
from ..plugins.plugin_manager import PluginManager


logger = get_logger(__name__)


class SettingsDialog(QDialog):
    """
    Settings dialog for application configuration.
    """
    
    def __init__(self, settings: Settings, parent=None):
        """
        Initialize the settings dialog.
        
        Args:
            settings: Settings manager
            parent: Parent widget
        """
        super().__init__(parent)
        self.settings = settings
        
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("<h2>Application Settings</h2>"))
        
        # Settings display (simplified for now)
        settings_text = QTextEdit()
        settings_text.setReadOnly(True)
        settings_text.setPlainText(
            f"Window Size: {settings.get('window.width')}x{settings.get('window.height')}\n"
            f"Theme: {settings.get('theme')}\n"
            f"Log Level: {settings.get('log_level')}\n"
            f"Plugins Enabled: {settings.get('plugins_enabled')}\n"
        )
        layout.addWidget(settings_text)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)


class MainWindow(QMainWindow):
    """
    Main application window with navigation and content areas.
    """
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Initialize managers
        self.settings = Settings()
        self.plugin_manager = PluginManager()
        
        # Set up logger
        log_file = str(self.settings.settings_file.parent / "app.log")
        setup_logger("conversion_gui", log_file)
        
        # Screens dictionary
        self.screens: Dict[str, QWidget] = {}
        
        # Set up UI
        self._setup_ui()
        
        # Restore window state
        self._restore_window_state()
        
        logger.info("Main window initialized")
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle("Conversion GUI - Dashboard")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Left navigation
        self.nav_list = QListWidget()
        self.nav_list.setMaximumWidth(200)
        self.nav_list.setMinimumWidth(150)
        self.nav_list.currentRowChanged.connect(self._on_nav_changed)
        main_layout.addWidget(self.nav_list)
        
        # Content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create toolbar
        self._create_toolbar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Add screens
        self._add_screen("Dashboard", DashboardScreen())
        self._add_screen("Database Browser", DBBrowserScreen())
        self._add_screen("Payments", PaymentsScreen())
        self._add_screen("Conversion Jobs", ConversionJobsScreen())
        self._add_screen("Log Analytics", LogAnalyticsScreen())
        self._add_screen("XML Helper", XMLHelperScreen())
        self._add_screen("Search", SearchScreen())
        
        # Select first screen
        if self.nav_list.count() > 0:
            self.nav_list.setCurrentRow(0)
    
    def _create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        new_action = QAction("&New...", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._on_new_clicked)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._on_open_clicked)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        settings_action = QAction("&Settings...", self)
        settings_action.triggered.connect(self._on_settings_clicked)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        refresh_action = QAction("&Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self._on_refresh_clicked)
        edit_menu.addAction(refresh_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        dashboard_action = QAction("&Dashboard", self)
        dashboard_action.triggered.connect(lambda: self._navigate_to("Dashboard"))
        view_menu.addAction(dashboard_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        plugins_action = QAction("&Plugins...", self)
        plugins_action.triggered.connect(self._on_plugins_clicked)
        tools_menu.addAction(plugins_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About...", self)
        about_action.triggered.connect(self._on_about_clicked)
        help_menu.addAction(about_action)
    
    def _create_toolbar(self) -> None:
        """Create the toolbar."""
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # Home action
        home_action = QAction("Home", self)
        home_action.setStatusTip("Go to Dashboard")
        home_action.triggered.connect(lambda: self._navigate_to("Dashboard"))
        toolbar.addAction(home_action)
        
        toolbar.addSeparator()
        
        # Refresh action
        refresh_action = QAction("Refresh", self)
        refresh_action.setStatusTip("Refresh current screen")
        refresh_action.triggered.connect(self._on_refresh_clicked)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # Search action
        search_action = QAction("Search", self)
        search_action.setStatusTip("Open search")
        search_action.triggered.connect(lambda: self._navigate_to("Search"))
        toolbar.addAction(search_action)
    
    def _add_screen(self, name: str, screen: QWidget) -> None:
        """
        Add a screen to the application.
        
        Args:
            name: Screen name
            screen: Screen widget
        """
        # Add to navigation
        self.nav_list.addItem(name)
        
        # Add to content stack
        self.content_stack.addWidget(screen)
        
        # Store reference
        self.screens[name] = screen
        
        logger.debug(f"Added screen: {name}")
    
    def _on_nav_changed(self, index: int) -> None:
        """
        Handle navigation change.
        
        Args:
            index: Selected navigation index
        """
        self.content_stack.setCurrentIndex(index)
        
        # Get screen name
        item = self.nav_list.item(index)
        if item:
            screen_name = item.text()
            self.setWindowTitle(f"Conversion GUI - {screen_name}")
            self.status_bar.showMessage(f"Viewing: {screen_name}")
            
            # Initialize screen if needed
            screen = self.screens.get(screen_name)
            if screen and hasattr(screen, 'initialize'):
                screen.initialize()
            
            logger.debug(f"Navigated to: {screen_name}")
    
    def _navigate_to(self, screen_name: str) -> None:
        """
        Navigate to a specific screen.
        
        Args:
            screen_name: Name of screen to navigate to
        """
        for i in range(self.nav_list.count()):
            item = self.nav_list.item(i)
            if item and item.text() == screen_name:
                self.nav_list.setCurrentRow(i)
                break
    
    def _on_new_clicked(self) -> None:
        """Handle new action."""
        logger.info("New action triggered")
        self.status_bar.showMessage("New action - not implemented yet", 3000)
    
    def _on_open_clicked(self) -> None:
        """Handle open action."""
        logger.info("Open action triggered")
        self.status_bar.showMessage("Open action - not implemented yet", 3000)
    
    def _on_refresh_clicked(self) -> None:
        """Handle refresh action."""
        current_index = self.content_stack.currentIndex()
        screen = self.content_stack.widget(current_index)
        
        if screen and hasattr(screen, 'refresh'):
            screen.refresh()
            self.status_bar.showMessage("Refreshed", 2000)
            logger.info("Screen refreshed")
    
    def _on_settings_clicked(self) -> None:
        """Handle settings action."""
        dialog = SettingsDialog(self.settings, self)
        dialog.exec()
        logger.info("Settings dialog opened")
    
    def _on_plugins_clicked(self) -> None:
        """Handle plugins action."""
        plugins = self.plugin_manager.get_all_plugins()
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Plugins")
        msg.setText(f"Total plugins loaded: {len(plugins)}")
        
        if plugins:
            details = "\n".join([f"{p.name} v{p.version}" for p in plugins])
            msg.setDetailedText(details)
        else:
            msg.setInformativeText("No plugins currently loaded.")
        
        msg.exec()
        logger.info("Plugins dialog opened")
    
    def _on_about_clicked(self) -> None:
        """Handle about action."""
        QMessageBox.about(
            self,
            "About Conversion GUI",
            "<h2>Conversion GUI v1.0.0</h2>"
            "<p>A modular PyQt6 application for data conversion, "
            "analytics, and management.</p>"
            "<p>Features:</p>"
            "<ul>"
            "<li>Database browser with filtering</li>"
            "<li>Payment management and analytics</li>"
            "<li>Conversion job tracking with detailed views</li>"
            "<li>Log analytics with regex support</li>"
            "<li>XML validation and formatting</li>"
            "<li>Global search capabilities</li>"
            "<li>Extensible plugin system</li>"
            "</ul>"
        )
        logger.info("About dialog opened")
    
    def _restore_window_state(self) -> None:
        """Restore window state from settings."""
        width = self.settings.get("window.width", 1280)
        height = self.settings.get("window.height", 720)
        maximized = self.settings.get("window.maximized", False)
        
        self.resize(width, height)
        
        if maximized:
            self.showMaximized()
    
    def closeEvent(self, event) -> None:
        """
        Handle window close event.
        
        Args:
            event: Close event
        """
        # Save window state
        self.settings.set("window.width", self.width())
        self.settings.set("window.height", self.height())
        self.settings.set("window.maximized", self.isMaximized())
        self.settings.save()
        
        # Cleanup screens
        for screen in self.screens.values():
            if hasattr(screen, 'cleanup'):
                screen.cleanup()
        
        logger.info("Application closing")
        event.accept()
