# Conversion GUI

A modular PyQt6 application for data conversion, analytics, and management with an extensible plugin system.

## Features

### Core Functionality
- **Extensible Dashboard**: Overview of all activities with charts and statistics
- **Database Browser**: Browse database records with advanced filtering
- **Payment Management**: Track and analyze payment transactions
- **Conversion Jobs**: Monitor conversion jobs with detailed views including:
  - Thread management
  - Batch progress tracking
  - Error logging and reporting
  - Job history and statistics
- **Log Analytics**: Analyze log files with:
  - Regular expression support
  - Pattern presets (errors, warnings, exceptions, etc.)
  - Large file support (>6GB) using streaming
  - Directory-wide search
- **XML Helper**: Validate and format XML files
- **Global Search**: Search across all application content
- **Settings Management**: Configurable application settings
- **Plugin System**: Extensible architecture for custom functionality

### Architecture
- **MVC Pattern**: Clean separation of concerns
- **Type Hints**: Full typing support throughout the codebase
- **Error Handling**: Comprehensive error handling and logging
- **Modular Design**: Easy to extend and maintain

## Installation

### Requirements
- Python 3.8 or higher
- PyQt6 6.6.0 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/aaronnmajor/conversion-gui.git
cd conversion-gui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Running Tests

```bash
pytest tests/
```

## Project Structure

```
conversion-gui/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/
│   ├── core/              # Core application components
│   │   ├── base_screen.py # Base class for screens
│   │   └── main_window.py # Main application window
│   ├── models/            # Data models
│   │   ├── job_model.py   # Conversion job models
│   │   └── payment_model.py # Payment models
│   ├── views/             # View components
│   ├── controllers/       # Controller logic
│   ├── widgets/           # Reusable widgets
│   │   ├── data_table.py  # Table/ListView wrapper
│   │   ├── chart_widget.py # Chart visualization
│   │   ├── filter_widget.py # Data filtering
│   │   └── text_area.py   # Enhanced text area
│   ├── screens/           # Application screens
│   │   ├── dashboard_screen.py
│   │   ├── db_browser_screen.py
│   │   ├── payments_screen.py
│   │   ├── conversion_jobs_screen.py
│   │   ├── log_analytics_screen.py
│   │   ├── xml_helper_screen.py
│   │   └── search_screen.py
│   ├── utils/             # Utility functions
│   │   ├── logger.py      # Logging utilities
│   │   ├── error_handler.py # Error handling
│   │   └── settings.py    # Settings management
│   └── plugins/           # Plugin system
│       ├── plugin_interface.py
│       └── plugin_manager.py
└── tests/                 # Unit tests
    ├── test_models.py
    ├── test_utils.py
    ├── test_widgets.py
    └── test_plugins.py
```

## Screens

### Dashboard
The main landing page showing:
- Active job statistics
- Payment summaries
- Error counts
- Recent activity
- Visual charts and graphs

### Database Browser
- Browse database records
- Filter by multiple criteria
- Sort and search functionality
- Export capabilities

### Payments
- View payment transactions
- Filter by status, method, date
- Payment analytics with charts
- Transaction details

### Conversion Jobs
- List all conversion jobs
- Detailed job view showing:
  - Job status and progress
  - Thread count
  - Batch processing details
  - Error logs
  - Execution timeline
- Create and monitor new jobs

### Log Analytics
- Load single log files or entire directories
- Search with plain text or regular expressions
- Pre-configured patterns for common searches:
  - Error messages
  - Warnings
  - Exception stack traces
  - Database queries
  - HTTP requests
  - Email addresses
  - IP addresses
  - Timestamps
- Handles files larger than 6GB using streaming
- Real-time progress updates

### XML Helper
- Load and edit XML files
- Validate XML structure
- Format (pretty print) XML
- Tag statistics
- Error detection and reporting

### Search
- Global search across all content
- Filter by content type
- Quick access to results

## Common Widgets

### DataTable
Enhanced table widget with:
- Sortable columns
- Row selection
- Alternating row colors
- Dynamic data updates

### ChartWidget
Visualization widget supporting:
- Bar charts
- Multiple data series
- Customizable axes and labels
- Animation effects

### FilterWidget
Data filtering widget with:
- Multiple filter operators
- Quick search
- Field selection
- Apply/Clear actions

### TextArea
Enhanced text area with:
- Monospace font
- Read-only mode
- Line wrapping
- Append functionality

## Plugin System

The application supports custom plugins to extend functionality.

### Creating a Plugin

1. Create a Python file in `~/.conversion-gui/plugins/`
2. Implement the `PluginInterface`:

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
        # Plugin initialization code
        pass
    
    def cleanup(self) -> None:
        # Plugin cleanup code
        pass
```

### Plugin Features
- Access to application context
- Custom menu items
- Custom toolbar items
- Settings widget integration

## Settings

Application settings are stored in `~/.conversion-gui/settings.json`

Default settings:
```json
{
  "window": {
    "width": 1280,
    "height": 720,
    "maximized": false
  },
  "theme": "light",
  "log_level": "INFO",
  "plugins_enabled": true,
  "recent_files": [],
  "database": {
    "type": "sqlite",
    "path": ""
  }
}
```

## Logging

Application logs are stored in `~/.conversion-gui/app.log`

Log levels:
- DEBUG: Detailed information for debugging
- INFO: General informational messages
- WARNING: Warning messages
- ERROR: Error messages
- CRITICAL: Critical errors

## Error Handling

The application includes comprehensive error handling:
- Global exception handler
- Error dialogs for user-facing errors
- Detailed error logging
- Stack trace capture

## Development

### Adding a New Screen

1. Create a new screen class in `src/screens/`:

```python
from src.core.base_screen import BaseScreen

class MyScreen(BaseScreen):
    @property
    def screen_name(self) -> str:
        return "My Screen"
    
    @property
    def screen_icon(self) -> str:
        return "icon_name"
    
    def setup_ui(self) -> None:
        # Set up UI components
        pass
    
    def load_data(self) -> None:
        # Load screen data
        pass
```

2. Register the screen in `main_window.py`:

```python
self._add_screen("My Screen", MyScreen())
```

### Adding a New Widget

1. Create a widget class in `src/widgets/`
2. Inherit from appropriate PyQt6 widget class
3. Add docstrings and type hints
4. Add tests in `tests/test_widgets.py`

### Code Style

- Follow PEP 8 guidelines
- Use type hints throughout
- Write comprehensive docstrings
- Add unit tests for new functionality
- Use meaningful variable and function names

## License

This project is provided as-is for educational and development purposes.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## Support

For issues, questions, or suggestions, please open an issue on GitHub.