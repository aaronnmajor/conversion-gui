# Architecture Documentation

## Overview

The Conversion GUI is built using the Model-View-Controller (MVC) architectural pattern with PyQt6 as the UI framework. This document describes the architecture, design decisions, and key components.

## Design Principles

1. **Separation of Concerns**: Clear separation between data (models), presentation (views), and business logic (controllers)
2. **Modularity**: Each component is self-contained and can be developed/tested independently
3. **Extensibility**: Plugin system allows adding new features without modifying core code
4. **Type Safety**: Full type hints throughout the codebase
5. **Error Handling**: Comprehensive error handling and logging at all levels

## Architecture Layers

### 1. Core Layer (`src/core/`)

The foundation of the application, providing:

- **BaseScreen**: Abstract base class for all screens
  - Defines common interface (screen_name, screen_icon, setup_ui, load_data)
  - Manages initialization lifecycle
  - Provides refresh and cleanup hooks

- **MainWindow**: Primary application window
  - Left navigation panel for screen selection
  - Stacked widget for content display
  - Menu bar with File, Edit, View, Tools, Help menus
  - Toolbar with quick actions
  - Status bar for user feedback
  - Integration with settings and plugin systems

### 2. Model Layer (`src/models/`)

Data structures and business entities:

- **ConversionJob**: Represents conversion job with status, progress, threads, errors, batches
  - JobStatus enum: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
  - JobError: Error information with timestamp, message, details, stack trace
  - BatchInfo: Batch processing information with progress tracking

- **Payment**: Represents payment transaction with amount, status, method
  - PaymentStatus enum: PENDING, PROCESSING, COMPLETED, FAILED, REFUNDED
  - PaymentMethod enum: CREDIT_CARD, DEBIT_CARD, BANK_TRANSFER, PAYPAL, OTHER

### 3. View Layer (`src/screens/`)

User interface screens:

- **DashboardScreen**: Overview with statistics cards and charts
- **DBBrowserScreen**: Database browser with filtering
- **PaymentsScreen**: Payment management with analytics
- **ConversionJobsScreen**: Job tracking with detailed views
- **LogAnalyticsScreen**: Log file analysis with regex support
- **XMLHelperScreen**: XML validation and formatting
- **SearchScreen**: Global search functionality

### 4. Widget Layer (`src/widgets/`)

Reusable UI components:

- **DataTable**: Enhanced table view with sorting, filtering, selection
- **ChartWidget**: Visualization widget for bar charts
- **FilterWidget**: Data filtering with multiple operators
- **TextArea**: Enhanced text area with monospace font and read-only mode

### 5. Controller Layer (`src/controllers/`)

Business logic and data management (extensible for future needs)

### 6. Utility Layer (`src/utils/`)

Cross-cutting concerns:

- **Logger**: Centralized logging with file and console output
- **Settings**: JSON-based settings management with nested keys
- **ErrorHandler**: Global exception handling and error dialogs

### 7. Plugin System (`src/plugins/`)

Extensibility framework:

- **PluginInterface**: Abstract interface for plugins
- **PluginManager**: Plugin discovery, loading, enabling/disabling

## Data Flow

### Screen Initialization Flow

```
User clicks navigation item
    ↓
MainWindow._on_nav_changed()
    ↓
content_stack.setCurrentIndex()
    ↓
Screen.initialize() (if first time)
    ↓
Screen.setup_ui()
    ↓
Screen.load_data()
```

### Data Update Flow

```
User action (button click, filter change)
    ↓
Screen event handler
    ↓
Update model/data
    ↓
Update view/widgets
    ↓
Log action
```

### Error Handling Flow

```
Exception occurs
    ↓
Try-catch block or @error_handler decorator
    ↓
Log error with stack trace
    ↓
Show error dialog to user (if appropriate)
    ↓
Graceful recovery or cleanup
```

## Key Design Patterns

### 1. Template Method Pattern

BaseScreen defines the template for screen lifecycle:
- initialize() → setup_ui() → load_data()
- Subclasses implement specific behavior

### 2. Observer Pattern

Qt's signal-slot mechanism for event handling:
- FilterWidget.filterChanged signal
- Button.clicked signal
- Navigation item selection

### 3. Factory Pattern

Plugin system for creating plugin instances dynamically

### 4. Singleton Pattern

Settings and PluginManager are effectively singletons in the application context

## Threading Model

### Main Thread
- UI operations
- Event handling
- Widget updates

### Worker Threads
- LogAnalyzerThread: Log file processing
- Future: Job execution threads

Thread communication via PyQt signals/slots for thread-safe updates.

## State Management

### Application State
- Stored in Settings class
- Persisted to ~/.conversion-gui/settings.json
- Includes window geometry, theme, preferences

### Screen State
- Each screen maintains its own state
- State preserved between navigation
- Lazy initialization on first view

### Session State
- In-memory only
- Reset on application restart
- Includes current selection, filters, search terms

## Security Considerations

1. **Input Validation**: All user inputs validated before processing
2. **File Operations**: Path validation to prevent directory traversal
3. **Error Messages**: Sanitized to avoid exposing sensitive information
4. **Logging**: Sensitive data excluded from logs

## Performance Optimizations

1. **Lazy Loading**: Screens initialized only when first viewed
2. **Streaming**: Large file processing (>6GB) uses streaming to avoid memory issues
3. **Chunked Processing**: Log analysis processes data in chunks
4. **Indexed Data**: Future: Database queries use indexes
5. **Caching**: Settings cached in memory

## Testing Strategy

### Unit Tests
- Models: Test data structures and business logic
- Utils: Test utility functions independently
- Plugins: Test plugin interface and manager
- Widgets: Test widget functionality (where possible without full GUI)

### Integration Tests
- Future: Test screen interactions
- Future: Test data flow between components

### Manual Testing
- UI interactions
- Visual appearance
- User workflows

## Future Enhancements

1. **Database Layer**: Add ORM (e.g., SQLAlchemy) for database operations
2. **Async Operations**: More async processing for long-running tasks
3. **Caching Layer**: Add caching for frequently accessed data
4. **API Layer**: REST API for external integration
5. **Theming**: Dark mode and custom themes
6. **Localization**: Multi-language support
7. **Auto-update**: Automatic application updates
8. **Advanced Charts**: More chart types and interactive visualizations

## Dependencies

### Core Dependencies
- PyQt6: UI framework
- PyQt6-Charts: Chart widgets
- typing-extensions: Enhanced type hints

### Development Dependencies
- pytest: Testing framework
- pytest-qt: PyQt testing utilities

### Optional Dependencies
- SQLAlchemy: Future database ORM
- requests: Future API integration
- beautifulsoup4: Future HTML parsing

## Build and Deployment

### Development
```bash
pip install -r requirements.txt
python main.py
```

### Testing
```bash
pytest tests/
```

### Packaging
Future: PyInstaller or cx_Freeze for standalone executables

## Maintenance Guidelines

1. **Code Style**: Follow PEP 8
2. **Documentation**: Update docstrings for all public APIs
3. **Testing**: Add tests for new features
4. **Logging**: Use appropriate log levels
5. **Error Handling**: Handle exceptions gracefully
6. **Type Hints**: Add type hints to all functions
7. **Commits**: Clear, descriptive commit messages

## Troubleshooting

### Common Issues

1. **ImportError for PyQt6**: Install PyQt6 packages
2. **Settings not persisting**: Check file permissions on ~/.conversion-gui/
3. **Plugin not loading**: Check plugin file syntax and interface implementation
4. **Large file processing slow**: Normal for >6GB files, uses streaming to avoid memory issues

## Glossary

- **Screen**: Full-page view in the application
- **Widget**: Reusable UI component
- **Plugin**: External module that extends functionality
- **Model**: Data structure representing business entity
- **Controller**: Business logic and data management
- **View**: UI presentation layer
