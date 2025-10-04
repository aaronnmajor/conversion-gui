"""Chart widget for data visualization."""

from typing import List, Tuple

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis


class ChartWidget(QWidget):
    """
    Chart widget for displaying various types of charts.
    """
    
    def __init__(self, parent=None):
        """
        Initialize the chart widget.
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(Qt.RenderHint.Antialiasing)
        
        layout = QVBoxLayout()
        layout.addWidget(self.chart_view)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def setTitle(self, title: str) -> None:
        """
        Set chart title.
        
        Args:
            title: Chart title
        """
        self.chart.setTitle(title)
    
    def clear(self) -> None:
        """Clear the chart."""
        self.chart.removeAllSeries()
    
    def createBarChart(
        self,
        categories: List[str],
        data: List[Tuple[str, List[float]]],
        x_label: str = "",
        y_label: str = ""
    ) -> None:
        """
        Create a bar chart.
        
        Args:
            categories: X-axis categories
            data: List of (series_name, values) tuples
            x_label: X-axis label
            y_label: Y-axis label
        """
        self.clear()
        
        series = QBarSeries()
        
        for name, values in data:
            bar_set = QBarSet(name)
            bar_set.append(values)
            series.append(bar_set)
        
        self.chart.addSeries(series)
        
        # X-axis
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        if x_label:
            axis_x.setTitleText(x_label)
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        # Y-axis
        axis_y = QValueAxis()
        if y_label:
            axis_y.setTitleText(y_label)
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
