# Quick Start Guide

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/aaronnmajor/conversion-gui.git
cd conversion-gui

# Install required packages
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using Python directly
```bash
python main.py
```

### Method 2: Using the run script (Linux/Mac)
```bash
./run.sh
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src
```

## Project Structure

```
conversion-gui/
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── src/
│   ├── core/           # Core application (MainWindow, BaseScreen)
│   ├── models/         # Data models (Job, Payment)
│   ├── screens/        # Application screens
│   ├── widgets/        # Reusable widgets
│   ├── utils/          # Utilities (logger, settings, error handler)
│   └── plugins/        # Plugin system
└── tests/              # Unit tests
```

## Common Tasks

### Adding a New Screen

1. Create screen file in `src/screens/`:

```python
from src.core.base_screen import BaseScreen
from PyQt6.QtWidgets import QVBoxLayout, QLabel

class MyNewScreen(BaseScreen):
    @property
    def screen_name(self) -> str:
        return "My New Screen"
    
    @property
    def screen_icon(self) -> str:
        return "icon_name"
    
    def setup_ui(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>My New Screen</h2>"))
        self.setLayout(layout)
    
    def load_data(self) -> None:
        # Load your data here
        pass
```

2. Register in `src/core/main_window.py`:

```python
from ..screens.my_new_screen import MyNewScreen

# In MainWindow._setup_ui():
self._add_screen("My New Screen", MyNewScreen())
```

### Creating a Plugin

1. Create plugin file in `~/.conversion-gui/plugins/my_plugin.py`:

```python
from src.plugins.plugin_interface import PluginInterface

class MyPlugin(PluginInterface):
    @property
    def name(self) -> str:
        return "My Plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "My custom plugin"
    
    def initialize(self, app_context) -> None:
        # Initialize plugin
        print(f"Initializing {self.name}")
    
    def cleanup(self) -> None:
        # Clean up resources
        print(f"Cleaning up {self.name}")
```

2. The plugin will be automatically discovered and can be enabled through the Tools menu.

### Using Common Widgets

#### DataTable Widget

```python
from src.widgets.data_table import DataTable

table = DataTable()

# Set data
headers = ["ID", "Name", "Email"]
data = [
    ["1", "John Doe", "john@example.com"],
    ["2", "Jane Smith", "jane@example.com"]
]
table.setData(data, headers)

# Append row
table.appendRow(["3", "Bob Johnson", "bob@example.com"])

# Clear table
table.clear()
```

#### ChartWidget

```python
from src.widgets.chart_widget import ChartWidget

chart = ChartWidget()
chart.setTitle("Sales Data")

# Create bar chart
categories = ["Q1", "Q2", "Q3", "Q4"]
data = [
    ("2023", [100, 120, 140, 160]),
    ("2024", [110, 130, 150, 170])
]
chart.createBarChart(categories, data, "Quarter", "Sales")
```

#### FilterWidget

```python
from src.widgets.filter_widget import FilterWidget

filter_widget = FilterWidget()
filter_widget.setFields(["Name", "Email", "Status"])
filter_widget.filterChanged.connect(on_filter_changed)

def on_filter_changed(field: str, operator: str, value: str):
    # Apply filter to your data
    print(f"Filter: {field} {operator} {value}")
```

### Working with Settings

```python
from src.utils.settings import Settings

settings = Settings()

# Get setting with default
theme = settings.get("theme", "light")

# Set setting
settings.set("custom_key", "custom_value")

# Save settings
settings.save()

# Access nested settings
width = settings.get("window.width")
settings.set("window.height", 800)
```

### Logging

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

### Error Handling

```python
from src.utils.error_handler import error_handler, show_error_dialog

# Using decorator
@error_handler(show_dialog=True)
def my_function():
    # Code that might raise exception
    pass

# Showing error dialog manually
try:
    risky_operation()
except Exception as e:
    show_error_dialog(
        parent=self,
        title="Operation Failed",
        message=str(e),
        details="Additional details here"
    )
```

## Development Workflow

1. **Make changes** to code
2. **Run tests** to ensure nothing broke: `pytest tests/`
3. **Test manually** by running the application
4. **Commit changes** with clear message
5. **Push** to repository

## Troubleshooting

### PyQt6 Import Error
```bash
pip install PyQt6 PyQt6-Charts
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Tests Failing
```bash
# Run tests with verbose output to see details
pytest tests/ -v -s
```

### Application Won't Start
- Check Python version: `python --version` (needs 3.8+)
- Check if PyQt6 is installed: `python -c "import PyQt6"`
- Check logs in `~/.conversion-gui/app.log`

## Useful Commands

```bash
# List all Python files
find src/ -name "*.py"

# Count lines of code
find src/ -name "*.py" -exec wc -l {} + | tail -1

# Run specific test
pytest tests/test_models.py::TestJobModel::test_job_creation -v

# Format code with black (if installed)
black src/ tests/

# Check code style with flake8 (if installed)
flake8 src/ tests/

# Generate test coverage report
pytest tests/ --cov=src --cov-report=html
```

## Next Steps

- Read [README.md](README.md) for detailed documentation
- Read [ARCHITECTURE.md](ARCHITECTURE.md) for architecture details
- Explore the code in `src/` directory
- Try creating a custom screen or plugin
- Run the tests and add your own

## Resources

- PyQt6 Documentation: https://www.riverbankcomputing.com/static/Docs/PyQt6/
- Python Type Hints: https://docs.python.org/3/library/typing.html
- pytest Documentation: https://docs.pytest.org/

## Getting Help

- Check existing code for examples
- Read docstrings in source files
- Review test files for usage examples
- Check application logs in `~/.conversion-gui/app.log`

## Tips

1. **Use type hints** for better IDE support and fewer bugs
2. **Write tests** for new functionality
3. **Log important events** for debugging
4. **Handle errors gracefully** with try-except blocks
5. **Keep screens focused** - each screen should do one thing well
6. **Reuse widgets** - don't reinvent common UI components
7. **Follow existing patterns** - consistency makes the code easier to maintain
