"""Payments screen."""

from datetime import datetime
from decimal import Decimal

from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

from ..core.base_screen import BaseScreen
from ..widgets.data_table import DataTable
from ..widgets.chart_widget import ChartWidget
from ..models.payment_model import Payment, PaymentStatus, PaymentMethod
from ..utils.logger import get_logger


logger = get_logger(__name__)


class PaymentsScreen(BaseScreen):
    """
    Payments management screen.
    """
    
    @property
    def screen_name(self) -> str:
        """Get screen name."""
        return "Payments"
    
    @property
    def screen_icon(self) -> str:
        """Get screen icon name."""
        return "payment"
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Title and controls
        header_layout = QHBoxLayout()
        title_label = QLabel("<h2>Payments</h2>")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)
        header_layout.addWidget(refresh_button)
        
        layout.addLayout(header_layout)
        
        # Chart widget
        self.chart_widget = ChartWidget()
        self.chart_widget.setTitle("Payment Statistics")
        self.chart_widget.setMaximumHeight(300)
        layout.addWidget(self.chart_widget)
        
        # Data table
        self.data_table = DataTable()
        layout.addWidget(self.data_table)
        
        self.setLayout(layout)
        
        logger.info("Payments screen UI initialized")
    
    def load_data(self) -> None:
        """Load screen data."""
        # Sample payment data
        payments = [
            Payment(
                payment_id="PAY001",
                amount=Decimal("100.50"),
                currency="USD",
                status=PaymentStatus.COMPLETED,
                method=PaymentMethod.CREDIT_CARD,
                created_at=datetime(2024, 1, 1, 10, 0),
                customer_name="John Doe"
            ),
            Payment(
                payment_id="PAY002",
                amount=Decimal("250.00"),
                currency="USD",
                status=PaymentStatus.COMPLETED,
                method=PaymentMethod.BANK_TRANSFER,
                created_at=datetime(2024, 1, 2, 11, 0),
                customer_name="Jane Smith"
            ),
            Payment(
                payment_id="PAY003",
                amount=Decimal("75.25"),
                currency="USD",
                status=PaymentStatus.PENDING,
                method=PaymentMethod.PAYPAL,
                created_at=datetime(2024, 1, 3, 12, 0),
                customer_name="Bob Johnson"
            ),
        ]
        
        # Update table
        headers = ["Payment ID", "Customer", "Amount", "Method", "Status", "Date"]
        data = [
            [
                p.payment_id,
                p.customer_name,
                p.formatted_amount,
                p.method.value,
                p.status.value,
                p.created_at.strftime("%Y-%m-%d %H:%M")
            ]
            for p in payments
        ]
        
        self.data_table.setData(data, headers)
        
        # Update chart
        categories = ["Jan", "Feb", "Mar"]
        chart_data = [
            ("Completed", [3, 5, 4]),
            ("Pending", [1, 2, 1]),
            ("Failed", [0, 1, 0])
        ]
        self.chart_widget.createBarChart(
            categories,
            chart_data,
            "Month",
            "Number of Payments"
        )
        
        logger.info("Payments data loaded")
    
    def refresh(self) -> None:
        """Refresh screen data."""
        super().refresh()
        logger.info("Payments screen refreshed")
