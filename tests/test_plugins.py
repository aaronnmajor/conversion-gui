"""Tests for plugin system."""

import pytest
from pathlib import Path
import tempfile

from src.plugins.plugin_interface import PluginInterface
from src.plugins.plugin_manager import PluginManager


class TestPlugin(PluginInterface):
    """Test plugin implementation."""
    
    @property
    def name(self) -> str:
        return "Test Plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "A test plugin"
    
    def initialize(self, app_context) -> None:
        self.initialized = True
    
    def cleanup(self) -> None:
        self.initialized = False


class TestPluginInterface:
    """Tests for plugin interface."""
    
    def test_plugin_creation(self):
        """Test creating a plugin."""
        plugin = TestPlugin()
        
        assert plugin.name == "Test Plugin"
        assert plugin.version == "1.0.0"
        assert plugin.description == "A test plugin"
    
    def test_plugin_initialization(self):
        """Test plugin initialization."""
        plugin = TestPlugin()
        
        plugin.initialize(None)
        assert plugin.initialized
        
        plugin.cleanup()
        assert not plugin.initialized


class TestPluginManager:
    """Tests for plugin manager."""
    
    def test_manager_creation(self):
        """Test creating a plugin manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(tmpdir)
            
            assert manager.plugin_dir == Path(tmpdir)
            assert manager.plugin_dir.exists()
    
    def test_discover_plugins(self):
        """Test discovering plugins."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test plugin file
            plugin_file = Path(tmpdir) / "test_plugin.py"
            plugin_file.write_text("""
from src.plugins.plugin_interface import PluginInterface

class TestPlugin(PluginInterface):
    @property
    def name(self):
        return "Test"
    
    @property
    def version(self):
        return "1.0"
    
    @property
    def description(self):
        return "Test"
    
    def initialize(self, app_context):
        pass
    
    def cleanup(self):
        pass
""")
            
            manager = PluginManager(tmpdir)
            plugins = manager.discover_plugins()
            
            assert "test_plugin" in plugins
    
    def test_get_all_plugins(self):
        """Test getting all plugins."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(tmpdir)
            
            plugins = manager.get_all_plugins()
            assert isinstance(plugins, list)
    
    def test_get_enabled_plugins(self):
        """Test getting enabled plugins."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = PluginManager(tmpdir)
            
            plugins = manager.get_enabled_plugins()
            assert isinstance(plugins, list)
