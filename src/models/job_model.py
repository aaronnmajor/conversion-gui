"""Data models for conversion jobs."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class JobStatus(Enum):
    """Job status enumeration."""
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


@dataclass
class JobError:
    """
    Represents a job error.
    """
    timestamp: datetime
    message: str
    details: str = ""
    stack_trace: str = ""


@dataclass
class BatchInfo:
    """
    Represents batch processing information.
    """
    batch_id: str
    total_items: int
    processed_items: int
    failed_items: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if self.total_items == 0:
            return 0.0
        return (self.processed_items / self.total_items) * 100


@dataclass
class ConversionJob:
    """
    Represents a conversion job.
    """
    job_id: str
    name: str
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    threads: int = 1
    errors: List[JobError] = field(default_factory=list)
    batches: List[BatchInfo] = field(default_factory=list)
    source_file: str = ""
    target_file: str = ""
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate job duration in seconds."""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None
    
    @property
    def has_errors(self) -> bool:
        """Check if job has errors."""
        return len(self.errors) > 0
    
    @property
    def total_batches(self) -> int:
        """Get total number of batches."""
        return len(self.batches)
    
    @property
    def completed_batches(self) -> int:
        """Get number of completed batches."""
        return sum(1 for batch in self.batches if batch.end_time is not None)
