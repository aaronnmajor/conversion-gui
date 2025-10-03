"""Tests for data models."""

import pytest
from datetime import datetime
from decimal import Decimal

from src.models.job_model import ConversionJob, JobStatus, JobError, BatchInfo
from src.models.payment_model import Payment, PaymentStatus, PaymentMethod


class TestJobModel:
    """Tests for job model."""
    
    def test_job_creation(self):
        """Test creating a conversion job."""
        job = ConversionJob(
            job_id="TEST001",
            name="Test Job",
            status=JobStatus.PENDING,
            created_at=datetime.now()
        )
        
        assert job.job_id == "TEST001"
        assert job.name == "Test Job"
        assert job.status == JobStatus.PENDING
        assert job.progress == 0.0
        assert job.threads == 1
    
    def test_job_duration(self):
        """Test job duration calculation."""
        start = datetime(2024, 1, 1, 10, 0, 0)
        end = datetime(2024, 1, 1, 10, 5, 30)
        
        job = ConversionJob(
            job_id="TEST001",
            name="Test Job",
            status=JobStatus.COMPLETED,
            created_at=start,
            started_at=start,
            completed_at=end
        )
        
        assert job.duration == 330.0  # 5 minutes 30 seconds
    
    def test_job_has_errors(self):
        """Test job error checking."""
        job = ConversionJob(
            job_id="TEST001",
            name="Test Job",
            status=JobStatus.FAILED,
            created_at=datetime.now()
        )
        
        assert not job.has_errors
        
        job.errors.append(JobError(
            timestamp=datetime.now(),
            message="Test error"
        ))
        
        assert job.has_errors
    
    def test_batch_progress(self):
        """Test batch progress calculation."""
        batch = BatchInfo(
            batch_id="BATCH001",
            total_items=100,
            processed_items=50,
            failed_items=5
        )
        
        assert batch.progress_percentage == 50.0


class TestPaymentModel:
    """Tests for payment model."""
    
    def test_payment_creation(self):
        """Test creating a payment."""
        payment = Payment(
            payment_id="PAY001",
            amount=Decimal("100.50"),
            currency="USD",
            status=PaymentStatus.PENDING,
            method=PaymentMethod.CREDIT_CARD,
            created_at=datetime.now()
        )
        
        assert payment.payment_id == "PAY001"
        assert payment.amount == Decimal("100.50")
        assert payment.currency == "USD"
        assert payment.status == PaymentStatus.PENDING
    
    def test_payment_status_checks(self):
        """Test payment status check methods."""
        payment = Payment(
            payment_id="PAY001",
            amount=Decimal("100.00"),
            currency="USD",
            status=PaymentStatus.COMPLETED,
            method=PaymentMethod.CREDIT_CARD,
            created_at=datetime.now()
        )
        
        assert payment.is_completed
        assert not payment.is_pending
    
    def test_payment_formatted_amount(self):
        """Test formatted amount display."""
        payment = Payment(
            payment_id="PAY001",
            amount=Decimal("1234.56"),
            currency="USD",
            status=PaymentStatus.COMPLETED,
            method=PaymentMethod.CREDIT_CARD,
            created_at=datetime.now()
        )
        
        assert payment.formatted_amount == "USD 1234.56"
