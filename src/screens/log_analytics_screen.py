"""Log analytics screen with regex and file streaming support."""

import re
import os
from pathlib import Path
from typing import List, Optional

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QFileDialog, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from ..core.base_screen import BaseScreen
from ..widgets.text_area import TextArea
from ..utils.logger import get_logger


logger = get_logger(__name__)


class LogAnalyzerThread(QThread):
    """
    Thread for analyzing large log files.
    
    Supports streaming files larger than 6GB.
    """
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)
    
    def __init__(self, file_path: str, pattern: str, is_regex: bool, is_directory: bool):
        """
        Initialize the log analyzer thread.
        
        Args:
            file_path: Path to log file or directory
            pattern: Search pattern
            is_regex: Whether pattern is a regex
            is_directory: Whether to process directory
        """
        super().__init__()
        self.file_path = file_path
        self.pattern = pattern
        self.is_regex = is_regex
        self.is_directory = is_directory
        self._running = True
    
    def run(self) -> None:
        """Run the analysis."""
        try:
            results = []
            
            if self.is_directory:
                # Process all log files in directory
                log_dir = Path(self.file_path)
                log_files = list(log_dir.glob("*.log")) + list(log_dir.glob("*.txt"))
                
                for log_file in log_files:
                    if not self._running:
                        break
                    self.progress.emit(f"Processing {log_file.name}...")
                    file_results = self._analyze_file(str(log_file))
                    results.extend(file_results)
            else:
                # Process single file
                self.progress.emit(f"Processing file...")
                results = self._analyze_file(self.file_path)
            
            self.finished.emit(results)
            
        except Exception as e:
            logger.error(f"Error analyzing logs: {e}", exc_info=True)
            self.progress.emit(f"Error: {str(e)}")
    
    def _analyze_file(self, file_path: str) -> List[str]:
        """
        Analyze a single log file.
        
        Args:
            file_path: Path to log file
            
        Returns:
            List of matching lines
        """
        results = []
        line_number = 0
        
        # Use streaming to handle large files (>6GB)
        chunk_size = 1024 * 1024  # 1MB chunks
        
        try:
            if self.is_regex:
                regex = re.compile(self.pattern)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                buffer = ""
                
                while self._running:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    
                    buffer += chunk
                    lines = buffer.split('\n')
                    
                    # Keep last incomplete line in buffer
                    buffer = lines[-1]
                    lines = lines[:-1]
                    
                    for line in lines:
                        line_number += 1
                        
                        if self.is_regex:
                            if regex.search(line):
                                results.append(f"{line_number}: {line}")
                        else:
                            if self.pattern.lower() in line.lower():
                                results.append(f"{line_number}: {line}")
                
                # Process last line
                if buffer and self._running:
                    line_number += 1
                    if self.is_regex:
                        if regex.search(buffer):
                            results.append(f"{line_number}: {buffer}")
                    else:
                        if self.pattern.lower() in buffer.lower():
                            results.append(f"{line_number}: {buffer}")
        
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
        
        return results
    
    def stop(self) -> None:
        """Stop the analysis."""
        self._running = False


class LogAnalyticsScreen(BaseScreen):
    """
    Log analytics screen with regex support and large file handling.
    
    Can process files larger than 6GB using streaming.
    """
    
    @property
    def screen_name(self) -> str:
        """Get screen name."""
        return "Log Analytics"
    
    @property
    def screen_icon(self) -> str:
        """Get screen icon name."""
        return "analytics"
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("<h2>Log Analytics</h2>")
        layout.addWidget(title_label)
        
        # File/Directory selection
        file_group = QGroupBox("Source")
        file_layout = QVBoxLayout()
        
        # File path
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Path:"))
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select log file or directory...")
        path_layout.addWidget(self.path_input)
        
        self.browse_file_button = QPushButton("Browse File")
        self.browse_file_button.clicked.connect(self._on_browse_file_clicked)
        path_layout.addWidget(self.browse_file_button)
        
        self.browse_dir_button = QPushButton("Browse Directory")
        self.browse_dir_button.clicked.connect(self._on_browse_dir_clicked)
        path_layout.addWidget(self.browse_dir_button)
        
        file_layout.addLayout(path_layout)
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Search configuration
        search_group = QGroupBox("Search")
        search_layout = QVBoxLayout()
        
        # Pattern input
        pattern_layout = QHBoxLayout()
        pattern_layout.addWidget(QLabel("Pattern:"))
        self.pattern_input = QLineEdit()
        self.pattern_input.setPlaceholderText("Enter search pattern...")
        pattern_layout.addWidget(self.pattern_input)
        
        self.regex_checkbox = QCheckBox("Use Regex")
        pattern_layout.addWidget(self.regex_checkbox)
        
        search_layout.addLayout(pattern_layout)
        
        # Presets
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Presets:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Custom",
            "Error Messages",
            "Warning Messages",
            "Exception Stack Traces",
            "Database Queries",
            "HTTP Requests",
            "Email Addresses",
            "IP Addresses",
            "Timestamps"
        ])
        self.preset_combo.currentTextChanged.connect(self._on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        preset_layout.addStretch()
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._on_search_clicked)
        preset_layout.addWidget(self.search_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self._on_cancel_clicked)
        self.cancel_button.setEnabled(False)
        preset_layout.addWidget(self.cancel_button)
        
        search_layout.addLayout(preset_layout)
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        # Results
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        
        self.results_text = TextArea()
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        self.setLayout(layout)
        
        self._analyzer_thread: Optional[LogAnalyzerThread] = None
        
        # Preset patterns
        self._preset_patterns = {
            "Error Messages": (r"\b(error|ERROR|Error)\b", True),
            "Warning Messages": (r"\b(warning|WARNING|Warning|warn|WARN)\b", True),
            "Exception Stack Traces": (r"Exception|Traceback|at \w+\.\w+\(", True),
            "Database Queries": (r"(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP)\b", True),
            "HTTP Requests": (r"(GET|POST|PUT|DELETE|PATCH)\s+/\S+", True),
            "Email Addresses": (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", True),
            "IP Addresses": (r"\b(?:\d{1,3}\.){3}\d{1,3}\b", True),
            "Timestamps": (r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}", True),
        }
        
        logger.info("Log Analytics screen UI initialized")
    
    def load_data(self) -> None:
        """Load screen data."""
        self.results_text.setText("No results yet. Select a log file and search pattern.")
        logger.info("Log Analytics screen loaded")
    
    def _on_browse_file_clicked(self) -> None:
        """Handle browse file button click."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Log File",
            "",
            "Log Files (*.log *.txt);;All Files (*)"
        )
        
        if file_path:
            self.path_input.setText(file_path)
            logger.info(f"Selected log file: {file_path}")
    
    def _on_browse_dir_clicked(self) -> None:
        """Handle browse directory button click."""
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Select Log Directory"
        )
        
        if dir_path:
            self.path_input.setText(dir_path)
            logger.info(f"Selected log directory: {dir_path}")
    
    def _on_preset_changed(self, preset: str) -> None:
        """
        Handle preset change.
        
        Args:
            preset: Selected preset name
        """
        if preset in self._preset_patterns:
            pattern, is_regex = self._preset_patterns[preset]
            self.pattern_input.setText(pattern)
            self.regex_checkbox.setChecked(is_regex)
    
    def _on_search_clicked(self) -> None:
        """Handle search button click."""
        file_path = self.path_input.text()
        pattern = self.pattern_input.text()
        
        if not file_path or not pattern:
            self.status_label.setText("Error: Please select a file/directory and enter a pattern")
            return
        
        if not os.path.exists(file_path):
            self.status_label.setText("Error: Path does not exist")
            return
        
        is_regex = self.regex_checkbox.isChecked()
        is_directory = os.path.isdir(file_path)
        
        # Start analysis thread
        self._analyzer_thread = LogAnalyzerThread(file_path, pattern, is_regex, is_directory)
        self._analyzer_thread.progress.connect(self._on_analysis_progress)
        self._analyzer_thread.finished.connect(self._on_analysis_finished)
        self._analyzer_thread.start()
        
        self.search_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.status_label.setText("Analyzing...")
        self.results_text.setText("Searching...\n")
        
        logger.info(f"Started log analysis: {file_path} with pattern: {pattern}")
    
    def _on_cancel_clicked(self) -> None:
        """Handle cancel button click."""
        if self._analyzer_thread and self._analyzer_thread.isRunning():
            self._analyzer_thread.stop()
            self._analyzer_thread.wait()
            self.status_label.setText("Analysis cancelled")
            self.search_button.setEnabled(True)
            self.cancel_button.setEnabled(False)
    
    def _on_analysis_progress(self, message: str) -> None:
        """
        Handle analysis progress update.
        
        Args:
            message: Progress message
        """
        self.status_label.setText(message)
    
    def _on_analysis_finished(self, results: List[str]) -> None:
        """
        Handle analysis completion.
        
        Args:
            results: List of matching lines
        """
        self.search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        if results:
            self.results_text.setText(f"Found {len(results)} matches:\n\n")
            self.results_text.appendText("\n".join(results[:1000]))  # Limit display to first 1000
            
            if len(results) > 1000:
                self.results_text.appendText(f"\n\n... and {len(results) - 1000} more matches")
            
            self.status_label.setText(f"Analysis complete: {len(results)} matches found")
        else:
            self.results_text.setText("No matches found")
            self.status_label.setText("Analysis complete: No matches found")
        
        logger.info(f"Log analysis complete: {len(results)} matches found")
    
    def cleanup(self) -> None:
        """Clean up resources."""
        if self._analyzer_thread and self._analyzer_thread.isRunning():
            self._analyzer_thread.stop()
            self._analyzer_thread.wait()
        super().cleanup()
