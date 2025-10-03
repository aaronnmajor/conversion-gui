"""XML issues helper screen."""

import xml.etree.ElementTree as ET
from xml.dom import minidom

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QGroupBox, QSplitter
)
from PyQt6.QtCore import Qt

from ..core.base_screen import BaseScreen
from ..widgets.text_area import TextArea
from ..utils.logger import get_logger


logger = get_logger(__name__)


class XMLHelperScreen(BaseScreen):
    """
    XML issues helper screen for validating and fixing XML files.
    """
    
    @property
    def screen_name(self) -> str:
        """Get screen name."""
        return "XML Helper"
    
    @property
    def screen_icon(self) -> str:
        """Get screen icon name."""
        return "xml"
    
    def setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel("<h2>XML Issues Helper</h2>")
        layout.addWidget(title_label)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        load_button = QPushButton("Load XML")
        load_button.clicked.connect(self._on_load_clicked)
        controls_layout.addWidget(load_button)
        
        validate_button = QPushButton("Validate")
        validate_button.clicked.connect(self._on_validate_clicked)
        controls_layout.addWidget(validate_button)
        
        format_button = QPushButton("Format (Pretty Print)")
        format_button.clicked.connect(self._on_format_clicked)
        controls_layout.addWidget(format_button)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self._on_save_clicked)
        controls_layout.addWidget(save_button)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Splitter for input and output
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Input group
        input_group = QGroupBox("XML Input")
        input_layout = QVBoxLayout()
        self.input_text = TextArea()
        self.input_text.setPlaceholderText("Enter or load XML content...")
        input_layout.addWidget(self.input_text)
        input_group.setLayout(input_layout)
        splitter.addWidget(input_group)
        
        # Output group
        output_group = QGroupBox("Validation / Output")
        output_layout = QVBoxLayout()
        self.output_text = TextArea()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        splitter.addWidget(output_group)
        
        layout.addWidget(splitter)
        self.setLayout(layout)
        
        logger.info("XML Helper screen UI initialized")
    
    def load_data(self) -> None:
        """Load screen data."""
        sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<data>
    <item id="1">
        <name>Sample Item</name>
        <value>100</value>
    </item>
</data>"""
        
        self.input_text.setText(sample_xml)
        self.output_text.setText("Ready. Load or enter XML to validate.")
        
        logger.info("XML Helper screen loaded")
    
    def _on_load_clicked(self) -> None:
        """Handle load button click."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load XML File",
            "",
            "XML Files (*.xml);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.input_text.setText(content)
                self.output_text.setText(f"Loaded: {file_path}")
                logger.info(f"Loaded XML file: {file_path}")
                
            except Exception as e:
                self.output_text.setText(f"Error loading file: {str(e)}")
                logger.error(f"Error loading XML file: {e}", exc_info=True)
    
    def _on_validate_clicked(self) -> None:
        """Handle validate button click."""
        xml_content = self.input_text.getText()
        
        if not xml_content.strip():
            self.output_text.setText("Error: No XML content to validate")
            return
        
        try:
            # Parse XML
            root = ET.fromstring(xml_content)
            
            # Get validation info
            tag_counts = {}
            self._count_tags(root, tag_counts)
            
            # Build output
            output = "✓ XML is well-formed and valid\n\n"
            output += f"Root element: {root.tag}\n"
            output += f"Root attributes: {root.attrib}\n\n"
            output += "Tag statistics:\n"
            
            for tag, count in sorted(tag_counts.items()):
                output += f"  {tag}: {count}\n"
            
            self.output_text.setText(output)
            logger.info("XML validation successful")
            
        except ET.ParseError as e:
            error_msg = f"✗ XML Parse Error:\n\n{str(e)}\n\n"
            error_msg += "Common issues:\n"
            error_msg += "- Unclosed tags\n"
            error_msg += "- Missing quotes around attributes\n"
            error_msg += "- Invalid characters in tag names\n"
            error_msg += "- Mismatched opening/closing tags\n"
            
            self.output_text.setText(error_msg)
            logger.warning(f"XML validation failed: {e}")
            
        except Exception as e:
            self.output_text.setText(f"✗ Error: {str(e)}")
            logger.error(f"XML validation error: {e}", exc_info=True)
    
    def _count_tags(self, element: ET.Element, counts: dict) -> None:
        """
        Count tag occurrences recursively.
        
        Args:
            element: XML element
            counts: Dictionary to store counts
        """
        counts[element.tag] = counts.get(element.tag, 0) + 1
        
        for child in element:
            self._count_tags(child, counts)
    
    def _on_format_clicked(self) -> None:
        """Handle format button click."""
        xml_content = self.input_text.getText()
        
        if not xml_content.strip():
            self.output_text.setText("Error: No XML content to format")
            return
        
        try:
            # Parse and format XML
            root = ET.fromstring(xml_content)
            xml_str = ET.tostring(root, encoding='unicode')
            
            # Pretty print
            dom = minidom.parseString(xml_str)
            formatted = dom.toprettyxml(indent="  ")
            
            # Remove empty lines
            lines = [line for line in formatted.split('\n') if line.strip()]
            formatted = '\n'.join(lines)
            
            self.input_text.setText(formatted)
            self.output_text.setText("✓ XML formatted successfully")
            logger.info("XML formatted successfully")
            
        except Exception as e:
            self.output_text.setText(f"✗ Error formatting XML: {str(e)}")
            logger.error(f"XML formatting error: {e}", exc_info=True)
    
    def _on_save_clicked(self) -> None:
        """Handle save button click."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save XML File",
            "",
            "XML Files (*.xml);;All Files (*)"
        )
        
        if file_path:
            try:
                xml_content = self.input_text.getText()
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                
                self.output_text.setText(f"✓ Saved to: {file_path}")
                logger.info(f"Saved XML file: {file_path}")
                
            except Exception as e:
                self.output_text.setText(f"✗ Error saving file: {str(e)}")
                logger.error(f"Error saving XML file: {e}", exc_info=True)
