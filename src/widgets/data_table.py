"""Data table widget with ListView wrapper."""

from typing import Any, List, Optional

from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant
from PyQt6.QtWidgets import QTableView, QHeaderView, QAbstractItemView


class TableModel(QAbstractTableModel):
    """
    Table model for displaying data in a table view.
    """
    
    def __init__(self, data: Optional[List[List[Any]]] = None, 
                 headers: Optional[List[str]] = None):
        """
        Initialize the table model.
        
        Args:
            data: Table data as list of rows
            headers: Column headers
        """
        super().__init__()
        self._data = data or []
        self._headers = headers or []
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get row count."""
        return len(self._data)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Get column count."""
        return len(self._headers) if self._headers else (len(self._data[0]) if self._data else 0)
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Get data at index."""
        if not index.isValid():
            return QVariant()
        
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            try:
                return self._data[index.row()][index.column()]
            except (IndexError, KeyError):
                return QVariant()
        
        return QVariant()
    
    def headerData(self, section: int, orientation: Qt.Orientation, 
                   role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        """Get header data."""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal and section < len(self._headers):
                return self._headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        
        return QVariant()
    
    def setData(self, data: List[List[Any]], headers: Optional[List[str]] = None) -> None:
        """
        Set table data.
        
        Args:
            data: Table data as list of rows
            headers: Optional column headers
        """
        self.beginResetModel()
        self._data = data
        if headers:
            self._headers = headers
        self.endResetModel()
    
    def appendRow(self, row: List[Any]) -> None:
        """
        Append a row to the table.
        
        Args:
            row: Row data to append
        """
        self.beginInsertRows(QModelIndex(), len(self._data), len(self._data))
        self._data.append(row)
        self.endInsertRows()
    
    def clear(self) -> None:
        """Clear all data from the table."""
        self.beginResetModel()
        self._data = []
        self.endResetModel()


class DataTable(QTableView):
    """
    Enhanced table view widget with common functionality.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the data table widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self._model = TableModel()
        self.setModel(self._model)
        
        # Configure table
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        
        # Configure headers
        horizontal_header = self.horizontalHeader()
        if horizontal_header:
            horizontal_header.setStretchLastSection(True)
            horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        vertical_header = self.verticalHeader()
        if vertical_header:
            vertical_header.setVisible(False)
    
    def setData(self, data: List[List[Any]], headers: Optional[List[str]] = None) -> None:
        """
        Set table data.
        
        Args:
            data: Table data as list of rows
            headers: Optional column headers
        """
        self._model.setData(data, headers)
        self.resizeColumnsToContents()
    
    def appendRow(self, row: List[Any]) -> None:
        """
        Append a row to the table.
        
        Args:
            row: Row data to append
        """
        self._model.appendRow(row)
    
    def clear(self) -> None:
        """Clear all data from the table."""
        self._model.clear()
    
    def getSelectedRow(self) -> Optional[int]:
        """
        Get the currently selected row index.
        
        Returns:
            Selected row index or None
        """
        indexes = self.selectedIndexes()
        return indexes[0].row() if indexes else None
    
    def getRowData(self, row: int) -> List[Any]:
        """
        Get data for a specific row.
        
        Args:
            row: Row index
            
        Returns:
            List of values for the row
        """
        return self._model._data[row] if 0 <= row < len(self._model._data) else []
