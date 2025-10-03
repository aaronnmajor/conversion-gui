"""Search screen for global content search."""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QGroupBox
)

from ..core.base_screen import BaseScreen
from ..widgets.data_table import DataTable
from ..utils.logger import get_logger


logger = get_logger(__name__)


class SearchScreen(BaseScreen):
    """
    Global search screen for searching across all content.
    """
    
    @property
    def screen_name(self) -> str:
        """Get screen name."""
        return "Search"
    
    @property
    def screen_icon(self) -> str:
        """Get screen icon name."""
        return "search"
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("<h2>Global Search</h2>")
        layout.addWidget(title_label)
        
        # Search group
        search_group = QGroupBox("Search Configuration")
        search_layout = QVBoxLayout()
        
        # Search input
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        self.search_input.returnPressed.connect(self._on_search_clicked)
        input_layout.addWidget(self.search_input)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._on_search_clicked)
        input_layout.addWidget(self.search_button)
        
        search_layout.addLayout(input_layout)
        
        # Search scope
        scope_layout = QHBoxLayout()
        scope_layout.addWidget(QLabel("Search in:"))
        self.scope_combo = QComboBox()
        self.scope_combo.addItems([
            "All",
            "Database Records",
            "Payments",
            "Conversion Jobs",
            "Log Files",
            "XML Files"
        ])
        scope_layout.addWidget(self.scope_combo)
        scope_layout.addStretch()
        
        search_layout.addLayout(scope_layout)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Results group
        results_group = QGroupBox("Search Results")
        results_layout = QVBoxLayout()
        
        self.results_label = QLabel("No searches performed yet")
        results_layout.addWidget(self.results_label)
        
        self.results_table = DataTable()
        results_layout.addWidget(self.results_table)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        self.setLayout(layout)
        
        logger.info("Search screen UI initialized")
    
    def load_data(self) -> None:
        """Load screen data."""
        # Initialize empty results
        headers = ["Type", "ID", "Title", "Content", "Location"]
        self.results_table.setData([], headers)
        
        logger.info("Search screen loaded")
    
    def _on_search_clicked(self) -> None:
        """Handle search button click."""
        search_term = self.search_input.text()
        search_scope = self.scope_combo.currentText()
        
        if not search_term:
            self.results_label.setText("Please enter a search term")
            return
        
        logger.info(f"Searching for '{search_term}' in {search_scope}")
        
        # Sample search results
        results = [
            ["Payment", "PAY001", "Payment Transaction", f"Contains '{search_term}'", "Payments"],
            ["Job", "JOB002", "Conversion Job", f"Description: {search_term}", "Jobs"],
            ["Log", "log_2024.txt", "Error Log", f"Line 42: {search_term}", "Logs"],
        ]
        
        headers = ["Type", "ID", "Title", "Content", "Location"]
        self.results_table.setData(results, headers)
        
        self.results_label.setText(f"Found {len(results)} results for '{search_term}' in {search_scope}")
        
        logger.info(f"Search complete: {len(results)} results found")
