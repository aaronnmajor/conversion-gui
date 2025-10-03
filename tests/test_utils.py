"""Tests for utility functions."""

import pytest
import logging
from pathlib import Path
import tempfile
import json

from src.utils.logger import setup_logger, get_logger
from src.utils.settings import Settings


class TestLogger:
    """Tests for logger utilities."""
    
    def test_setup_logger(self):
        """Test logger setup."""
        logger = setup_logger("test_logger")
        
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO
        assert len(logger.handlers) > 0
    
    def test_setup_logger_with_file(self):
        """Test logger setup with file output."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            logger = setup_logger("test_logger_file", str(log_file))
            
            logger.info("Test message")
            
            assert log_file.exists()
            content = log_file.read_text()
            assert "Test message" in content
    
    def test_get_logger(self):
        """Test getting existing logger."""
        logger1 = setup_logger("test_logger_get")
        logger2 = get_logger("test_logger_get")
        
        assert logger1.name == logger2.name


class TestSettings:
    """Tests for settings manager."""
    
    def test_settings_creation(self):
        """Test settings creation with defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"
            settings = Settings(str(settings_file))
            
            assert settings.get("theme") == "light"
            assert settings.get("window.width") == 1280
            assert settings.get("window.height") == 720
    
    def test_settings_get_set(self):
        """Test getting and setting values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"
            settings = Settings(str(settings_file))
            
            settings.set("test_key", "test_value")
            assert settings.get("test_key") == "test_value"
            
            settings.set("nested.key", "nested_value")
            assert settings.get("nested.key") == "nested_value"
    
    def test_settings_save_load(self):
        """Test saving and loading settings."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"
            
            # Create and save settings
            settings1 = Settings(str(settings_file))
            settings1.set("custom_key", "custom_value")
            settings1.save()
            
            # Load settings in new instance
            settings2 = Settings(str(settings_file))
            assert settings2.get("custom_key") == "custom_value"
    
    def test_settings_reset(self):
        """Test resetting settings to defaults."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"
            settings = Settings(str(settings_file))
            
            settings.set("custom_key", "custom_value")
            assert settings.get("custom_key") == "custom_value"
            
            settings.reset()
            assert settings.get("custom_key") is None
            assert settings.get("theme") == "light"
    
    def test_settings_get_with_default(self):
        """Test getting value with default."""
        with tempfile.TemporaryDirectory() as tmpdir:
            settings_file = Path(tmpdir) / "settings.json"
            settings = Settings(str(settings_file))
            
            value = settings.get("nonexistent", "default_value")
            assert value == "default_value"
