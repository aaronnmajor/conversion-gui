"""Filter widget for data filtering."""

from typing import Callable, Optional

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QComboBox, QPushButton, QGroupBox
)


class FilterWidget(QWidget):
    """
    Filter widget for filtering table data.
    """
    
    filterChanged = pyqtSignal(str, str, str)  # field, operator, value
    
    def __init__(self, parent=None):
        """
        Initialize the filter widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Filter group
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()
        
        # Field selector
        filter_layout.addWidget(QLabel("Field:"))
        self.field_combo = QComboBox()
        filter_layout.addWidget(self.field_combo)
        
        # Operator selector
        filter_layout.addWidget(QLabel("Operator:"))
        self.operator_combo = QComboBox()
        self.operator_combo.addItems(["Contains", "Equals", "Starts with", "Ends with"])
        filter_layout.addWidget(self.operator_combo)
        
        # Value input
        filter_layout.addWidget(QLabel("Value:"))
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Enter filter value...")
        filter_layout.addWidget(self.value_input)
        
        # Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self._on_apply_clicked)
        filter_layout.addWidget(self.apply_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self._on_clear_clicked)
        filter_layout.addWidget(self.clear_button)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Quick search
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Quick Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search all fields...")
        self.search_input.textChanged.connect(self._on_search_changed)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        self.setLayout(layout)
    
    def setFields(self, fields: list) -> None:
        """
        Set available fields for filtering.
        
        Args:
            fields: List of field names
        """
        self.field_combo.clear()
        self.field_combo.addItems(fields)
    
    def _on_apply_clicked(self) -> None:
        """Handle apply button click."""
        field = self.field_combo.currentText()
        operator = self.operator_combo.currentText()
        value = self.value_input.text()
        
        self.filterChanged.emit(field, operator, value)
    
    def _on_clear_clicked(self) -> None:
        """Handle clear button click."""
        self.value_input.clear()
        self.search_input.clear()
        self.filterChanged.emit("", "", "")
    
    def _on_search_changed(self, text: str) -> None:
        """Handle search text change."""
        if not text:
            self.filterChanged.emit("", "", "")
        else:
            self.filterChanged.emit("*", "Contains", text)
