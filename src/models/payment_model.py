"""Data models for payments."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class PaymentStatus(Enum):
    """Payment status enumeration."""
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


class PaymentMethod(Enum):
    """Payment method enumeration."""
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    BANK_TRANSFER = "Bank Transfer"
    PAYPAL = "PayPal"
    OTHER = "Other"


@dataclass
class Payment:
    """
    Represents a payment transaction.
    """
    payment_id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    method: PaymentMethod
    created_at: datetime
    processed_at: Optional[datetime] = None
    customer_id: str = ""
    customer_name: str = ""
    transaction_id: str = ""
    description: str = ""
    
    @property
    def is_completed(self) -> bool:
        """Check if payment is completed."""
        return self.status == PaymentStatus.COMPLETED
    
    @property
    def is_pending(self) -> bool:
        """Check if payment is pending."""
        return self.status == PaymentStatus.PENDING
    
    @property
    def formatted_amount(self) -> str:
        """Get formatted amount string."""
        return f"{self.currency} {self.amount:.2f}"
