"""Main dashboard screen."""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,
    QGroupBox, QFrame
)
from PyQt6.QtCore import Qt

from ..core.base_screen import BaseScreen
from ..widgets.chart_widget import ChartWidget
from ..widgets.data_table import DataTable
from ..utils.logger import get_logger


logger = get_logger(__name__)


class DashboardScreen(BaseScreen):
    """
    Main dashboard screen showing application overview.
    """
    
    @property
    def screen_name(self) -> str:
        """Get screen name."""
        return "Dashboard"
    
    @property
    def screen_icon(self) -> str:
        """Get screen icon name."""
        return "dashboard"
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("<h1>Dashboard</h1>")
        layout.addWidget(title_label)
        
        # Summary cards
        cards_layout = QGridLayout()
        
        self.jobs_card = self._create_stat_card("Active Jobs", "0", "#4CAF50")
        cards_layout.addWidget(self.jobs_card, 0, 0)
        
        self.payments_card = self._create_stat_card("Payments Today", "$0.00", "#2196F3")
        cards_layout.addWidget(self.payments_card, 0, 1)
        
        self.errors_card = self._create_stat_card("Errors", "0", "#F44336")
        cards_layout.addWidget(self.errors_card, 0, 2)
        
        self.records_card = self._create_stat_card("DB Records", "0", "#FF9800")
        cards_layout.addWidget(self.records_card, 0, 3)
        
        layout.addLayout(cards_layout)
        
        # Charts section
        charts_layout = QHBoxLayout()
        
        # Jobs chart
        jobs_chart_group = QGroupBox("Job Status")
        jobs_chart_layout = QVBoxLayout()
        self.jobs_chart = ChartWidget()
        self.jobs_chart.setTitle("Conversion Jobs")
        self.jobs_chart.setMinimumHeight(250)
        jobs_chart_layout.addWidget(self.jobs_chart)
        jobs_chart_group.setLayout(jobs_chart_layout)
        charts_layout.addWidget(jobs_chart_group)
        
        # Payments chart
        payments_chart_group = QGroupBox("Payment Analytics")
        payments_chart_layout = QVBoxLayout()
        self.payments_chart = ChartWidget()
        self.payments_chart.setTitle("Payments by Status")
        self.payments_chart.setMinimumHeight(250)
        payments_chart_layout.addWidget(self.payments_chart)
        payments_chart_group.setLayout(payments_chart_layout)
        charts_layout.addWidget(payments_chart_group)
        
        layout.addLayout(charts_layout)
        
        # Recent activity
        activity_group = QGroupBox("Recent Activity")
        activity_layout = QVBoxLayout()
        self.activity_table = DataTable()
        activity_layout.addWidget(self.activity_table)
        activity_group.setLayout(activity_layout)
        layout.addWidget(activity_group)
        
        self.setLayout(layout)
        
        logger.info("Dashboard screen UI initialized")
    
    def _create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """
        Create a statistics card widget.
        
        Args:
            title: Card title
            value: Card value
            color: Card color
            
        Returns:
            Card widget
        """
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 4px solid {color};
                border-radius: 4px;
                padding: 10px;
            }}
        """)
        
        card_layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 12px;")
        card_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        value_label.setObjectName(f"{title.lower().replace(' ', '_')}_value")
        card_layout.addWidget(value_label)
        
        card.setLayout(card_layout)
        return card
    
    def load_data(self) -> None:
        """Load screen data."""
        # Update stat cards
        self._update_stat_card(self.jobs_card, "5")
        self._update_stat_card(self.payments_card, "$12,450.00")
        self._update_stat_card(self.errors_card, "3")
        self._update_stat_card(self.records_card, "1,234")
        
        # Update jobs chart
        categories = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        jobs_data = [
            ("Completed", [5, 8, 6, 9, 7]),
            ("Failed", [1, 0, 2, 1, 0]),
        ]
        self.jobs_chart.createBarChart(categories, jobs_data, "Day", "Jobs")
        
        # Update payments chart
        payment_categories = ["Completed", "Pending", "Failed"]
        payment_data = [("Count", [150, 25, 5])]
        self.payments_chart.createBarChart(payment_categories, payment_data, "Status", "Count")
        
        # Update recent activity table
        headers = ["Time", "Type", "Description", "Status"]
        activity_data = [
            ["10:30 AM", "Job", "Payment File Conversion completed", "Success"],
            ["10:15 AM", "Payment", "Payment PAY001 processed", "Success"],
            ["10:00 AM", "Job", "Customer Data Import started", "Running"],
            ["09:45 AM", "Log", "Error detected in log file", "Warning"],
            ["09:30 AM", "XML", "XML validation completed", "Success"],
        ]
        
        self.activity_table.setData(activity_data, headers)
        
        logger.info("Dashboard data loaded")
    
    def _update_stat_card(self, card: QFrame, value: str) -> None:
        """
        Update a stat card value.
        
        Args:
            card: Card widget
            value: New value
        """
        # Find the value label in the card
        for child in card.children():
            if isinstance(child, QVBoxLayout):
                for i in range(child.count()):
                    item = child.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        if isinstance(widget, QLabel) and "font-size: 24px" in widget.styleSheet():
                            widget.setText(value)
                            break
