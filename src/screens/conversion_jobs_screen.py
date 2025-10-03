"""Conversion jobs screen with detailed job view."""

from datetime import datetime
from typing import Optional

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSplitter, QGroupBox, QProgressBar, QTextEdit
)
from PyQt6.QtCore import Qt

from ..core.base_screen import BaseScreen
from ..widgets.data_table import DataTable
from ..models.job_model import ConversionJob, JobStatus, JobError, BatchInfo
from ..utils.logger import get_logger


logger = get_logger(__name__)


class ConversionJobsScreen(BaseScreen):
    """
    Conversion jobs screen with job detail view.
    
    Shows list of jobs and detailed information including threads, errors, and batch progress.
    """
    
    @property
    def screen_name(self) -> str:
        """Get screen name."""
        return "Conversion Jobs"
    
    @property
    def screen_icon(self) -> str:
        """Get screen icon name."""
        return "jobs"
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Title and controls
        header_layout = QHBoxLayout()
        title_label = QLabel("<h2>Conversion Jobs</h2>")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        new_job_button = QPushButton("New Job")
        new_job_button.clicked.connect(self._on_new_job_clicked)
        header_layout.addWidget(new_job_button)
        
        refresh_button = QPushButton("Refresh")
        refresh_button.clicked.connect(self.refresh)
        header_layout.addWidget(refresh_button)
        
        layout.addLayout(header_layout)
        
        # Create splitter for job list and detail view
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Job list table
        self.jobs_table = DataTable()
        self.jobs_table.doubleClicked.connect(self._on_job_double_clicked)
        splitter.addWidget(self.jobs_table)
        
        # Job detail view
        detail_widget = self._create_detail_view()
        splitter.addWidget(detail_widget)
        
        # Set splitter sizes (60% list, 40% detail)
        splitter.setSizes([600, 400])
        
        layout.addWidget(splitter)
        self.setLayout(layout)
        
        self._current_job: Optional[ConversionJob] = None
        self._sample_jobs = []
        
        logger.info("Conversion Jobs screen UI initialized")
    
    def _create_detail_view(self) -> QGroupBox:
        """
        Create the job detail view widget.
        
        Returns:
            Detail view widget
        """
        detail_group = QGroupBox("Job Details")
        detail_layout = QVBoxLayout()
        
        # Job info
        info_layout = QHBoxLayout()
        
        self.job_id_label = QLabel("Job ID: -")
        info_layout.addWidget(self.job_id_label)
        
        self.job_status_label = QLabel("Status: -")
        info_layout.addWidget(self.job_status_label)
        
        self.job_threads_label = QLabel("Threads: -")
        info_layout.addWidget(self.job_threads_label)
        
        info_layout.addStretch()
        detail_layout.addLayout(info_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        detail_layout.addWidget(self.progress_bar)
        
        # Batch info
        batch_group = QGroupBox("Batch Progress")
        batch_layout = QVBoxLayout()
        self.batch_info_label = QLabel("No batches")
        batch_layout.addWidget(self.batch_info_label)
        batch_group.setLayout(batch_layout)
        detail_layout.addWidget(batch_group)
        
        # Errors
        error_group = QGroupBox("Errors")
        error_layout = QVBoxLayout()
        self.error_text = QTextEdit()
        self.error_text.setReadOnly(True)
        self.error_text.setMaximumHeight(150)
        error_layout.addWidget(self.error_text)
        error_group.setLayout(error_layout)
        detail_layout.addWidget(error_group)
        
        detail_group.setLayout(detail_layout)
        return detail_group
    
    def load_data(self) -> None:
        """Load screen data."""
        # Sample job data
        self._sample_jobs = [
            ConversionJob(
                job_id="JOB001",
                name="Payment File Conversion",
                status=JobStatus.COMPLETED,
                created_at=datetime(2024, 1, 1, 10, 0),
                started_at=datetime(2024, 1, 1, 10, 1),
                completed_at=datetime(2024, 1, 1, 10, 30),
                progress=100.0,
                threads=4,
                source_file="payments_2024.csv",
                target_file="payments_2024.xml",
                batches=[
                    BatchInfo("BATCH1", 1000, 1000, 0, datetime(2024, 1, 1, 10, 1), datetime(2024, 1, 1, 10, 15)),
                    BatchInfo("BATCH2", 1000, 1000, 0, datetime(2024, 1, 1, 10, 15), datetime(2024, 1, 1, 10, 30)),
                ]
            ),
            ConversionJob(
                job_id="JOB002",
                name="Customer Data Import",
                status=JobStatus.RUNNING,
                created_at=datetime(2024, 1, 2, 11, 0),
                started_at=datetime(2024, 1, 2, 11, 1),
                progress=65.0,
                threads=2,
                source_file="customers.json",
                target_file="customers.db",
                batches=[
                    BatchInfo("BATCH1", 500, 325, 5, datetime(2024, 1, 2, 11, 1), None),
                ]
            ),
            ConversionJob(
                job_id="JOB003",
                name="Legacy System Migration",
                status=JobStatus.FAILED,
                created_at=datetime(2024, 1, 3, 12, 0),
                started_at=datetime(2024, 1, 3, 12, 1),
                completed_at=datetime(2024, 1, 3, 12, 5),
                progress=25.0,
                threads=1,
                source_file="legacy_data.txt",
                target_file="new_system.db",
                errors=[
                    JobError(
                        datetime(2024, 1, 3, 12, 5),
                        "Database connection failed",
                        "Unable to connect to target database",
                        "Connection timeout after 30 seconds"
                    )
                ]
            ),
        ]
        
        # Update table
        headers = ["Job ID", "Name", "Status", "Progress", "Threads", "Created", "Duration"]
        data = [
            [
                job.job_id,
                job.name,
                job.status.value,
                f"{job.progress:.1f}%",
                str(job.threads),
                job.created_at.strftime("%Y-%m-%d %H:%M"),
                f"{job.duration:.1f}s" if job.duration else "-"
            ]
            for job in self._sample_jobs
        ]
        
        self.jobs_table.setData(data, headers)
        
        logger.info("Conversion Jobs data loaded")
    
    def _on_job_double_clicked(self, index) -> None:
        """
        Handle job double-click to show details.
        
        Args:
            index: Clicked index
        """
        row = index.row()
        if 0 <= row < len(self._sample_jobs):
            self._show_job_details(self._sample_jobs[row])
    
    def _show_job_details(self, job: ConversionJob) -> None:
        """
        Show details for a specific job.
        
        Args:
            job: Job to show details for
        """
        self._current_job = job
        
        # Update labels
        self.job_id_label.setText(f"Job ID: {job.job_id}")
        self.job_status_label.setText(f"Status: {job.status.value}")
        self.job_threads_label.setText(f"Threads: {job.threads}")
        
        # Update progress bar
        self.progress_bar.setValue(int(job.progress))
        
        # Update batch info
        if job.batches:
            batch_text = f"Total Batches: {job.total_batches}\n"
            batch_text += f"Completed Batches: {job.completed_batches}\n\n"
            
            for batch in job.batches:
                batch_text += f"{batch.batch_id}: {batch.processed_items}/{batch.total_items} "
                batch_text += f"({batch.progress_percentage:.1f}%) "
                batch_text += f"Failed: {batch.failed_items}\n"
            
            self.batch_info_label.setText(batch_text)
        else:
            self.batch_info_label.setText("No batches")
        
        # Update errors
        if job.errors:
            error_text = ""
            for error in job.errors:
                error_text += f"[{error.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {error.message}\n"
                error_text += f"Details: {error.details}\n"
                if error.stack_trace:
                    error_text += f"Stack Trace: {error.stack_trace}\n"
                error_text += "\n"
            
            self.error_text.setPlainText(error_text)
        else:
            self.error_text.setPlainText("No errors")
        
        logger.info(f"Showing details for job {job.job_id}")
    
    def _on_new_job_clicked(self) -> None:
        """Handle new job button click."""
        logger.info("New job button clicked")
        # In real implementation, this would open a dialog to create a new job
    
    def refresh(self) -> None:
        """Refresh screen data."""
        super().refresh()
        logger.info("Conversion Jobs screen refreshed")
