"""Tests for widgets."""

import pytest
from PyQt6.QtWidgets import QApplication

from src.widgets.data_table import DataTable, TableModel
from src.widgets.text_area import TextArea


@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for tests."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


class TestTableModel:
    """Tests for table model."""
    
    def test_model_creation(self):
        """Test creating a table model."""
        data = [["1", "John", "john@example.com"]]
        headers = ["ID", "Name", "Email"]
        
        model = TableModel(data, headers)
        
        assert model.rowCount() == 1
        assert model.columnCount() == 3
    
    def test_model_data_access(self):
        """Test accessing model data."""
        data = [["1", "John", "john@example.com"]]
        headers = ["ID", "Name", "Email"]
        
        model = TableModel(data, headers)
        
        index = model.index(0, 1)
        assert model.data(index) == "John"
    
    def test_model_append_row(self):
        """Test appending row to model."""
        data = [["1", "John", "john@example.com"]]
        headers = ["ID", "Name", "Email"]
        
        model = TableModel(data, headers)
        assert model.rowCount() == 1
        
        model.appendRow(["2", "Jane", "jane@example.com"])
        assert model.rowCount() == 2
    
    def test_model_clear(self):
        """Test clearing model data."""
        data = [["1", "John", "john@example.com"]]
        headers = ["ID", "Name", "Email"]
        
        model = TableModel(data, headers)
        assert model.rowCount() == 1
        
        model.clear()
        assert model.rowCount() == 0


class TestDataTable:
    """Tests for data table widget."""
    
    def test_table_creation(self, qapp):
        """Test creating a data table."""
        table = DataTable()
        
        assert table is not None
        assert table._model is not None
    
    def test_table_set_data(self, qapp):
        """Test setting table data."""
        table = DataTable()
        
        data = [["1", "John"], ["2", "Jane"]]
        headers = ["ID", "Name"]
        
        table.setData(data, headers)
        
        assert table._model.rowCount() == 2
        assert table._model.columnCount() == 2
    
    def test_table_append_row(self, qapp):
        """Test appending row to table."""
        table = DataTable()
        
        data = [["1", "John"]]
        headers = ["ID", "Name"]
        table.setData(data, headers)
        
        table.appendRow(["2", "Jane"])
        assert table._model.rowCount() == 2
    
    def test_table_clear(self, qapp):
        """Test clearing table."""
        table = DataTable()
        
        data = [["1", "John"]]
        headers = ["ID", "Name"]
        table.setData(data, headers)
        
        table.clear()
        assert table._model.rowCount() == 0


class TestTextArea:
    """Tests for text area widget."""
    
    def test_text_area_creation(self, qapp):
        """Test creating a text area."""
        text_area = TextArea()
        
        assert text_area is not None
    
    def test_text_area_set_get_text(self, qapp):
        """Test setting and getting text."""
        text_area = TextArea()
        
        text_area.setText("Test text")
        assert text_area.getText() == "Test text"
    
    def test_text_area_append(self, qapp):
        """Test appending text."""
        text_area = TextArea()
        
        text_area.setText("Line 1")
        text_area.appendText("Line 2")
        
        assert "Line 1" in text_area.getText()
        assert "Line 2" in text_area.getText()
    
    def test_text_area_clear(self, qapp):
        """Test clearing text."""
        text_area = TextArea()
        
        text_area.setText("Test text")
        text_area.clearText()
        
        assert text_area.getText() == ""
    
    def test_text_area_readonly(self, qapp):
        """Test read-only mode."""
        text_area = TextArea()
        
        text_area.setReadOnly(True)
        assert text_area.isReadOnly()
        
        text_area.setReadOnly(False)
        assert not text_area.isReadOnly()
