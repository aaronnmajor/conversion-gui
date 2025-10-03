"""Database browser screen."""

from typing import List, Any

from PyQt6.QtWidgets import QVBoxLayout, QSplitter, QLabel
from PyQt6.QtCore import Qt

from ..core.base_screen import BaseScreen
from ..widgets.data_table import DataTable
from ..widgets.filter_widget import FilterWidget
from ..utils.logger import get_logger


logger = get_logger(__name__)


class DBBrowserScreen(BaseScreen):
    """
    Database browser screen with filtering capabilities.
    """
    
    @property
    def screen_name(self) -> str:
        """Get screen name."""
        return "Database Browser"
    
    @property
    def screen_icon(self) -> str:
        """Get screen icon name."""
        return "database"
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("<h2>Database Browser</h2>")
        layout.addWidget(title_label)
        
        # Create splitter for filter and table
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Filter widget
        self.filter_widget = FilterWidget()
        self.filter_widget.filterChanged.connect(self._on_filter_changed)
        splitter.addWidget(self.filter_widget)
        
        # Data table
        self.data_table = DataTable()
        splitter.addWidget(self.data_table)
        
        # Set splitter sizes (20% filter, 80% table)
        splitter.setSizes([200, 800])
        
        layout.addWidget(splitter)
        self.setLayout(layout)
        
        logger.info("DB Browser screen UI initialized")
    
    def load_data(self) -> None:
        """Load screen data."""
        # Sample data - in real implementation, this would load from database
        headers = ["ID", "Name", "Email", "Status", "Created"]
        data = [
            ["1", "John Doe", "john@example.com", "Active", "2024-01-01"],
            ["2", "Jane Smith", "jane@example.com", "Active", "2024-01-02"],
            ["3", "Bob Johnson", "bob@example.com", "Inactive", "2024-01-03"],
            ["4", "Alice Williams", "alice@example.com", "Active", "2024-01-04"],
            ["5", "Charlie Brown", "charlie@example.com", "Active", "2024-01-05"],
        ]
        
        self.data_table.setData(data, headers)
        self.filter_widget.setFields(headers)
        
        logger.info("DB Browser data loaded")
    
    def _on_filter_changed(self, field: str, operator: str, value: str) -> None:
        """
        Handle filter changes.
        
        Args:
            field: Field to filter on
            operator: Filter operator
            value: Filter value
        """
        logger.info(f"Filter changed: {field} {operator} {value}")
        # In real implementation, this would filter the data
        # For now, just log the filter change
    
    def refresh(self) -> None:
        """Refresh screen data."""
        super().refresh()
        logger.info("DB Browser screen refreshed")
