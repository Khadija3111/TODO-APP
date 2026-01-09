"""
Configuration service for the Todo application.

This module handles persistent configuration preferences like sort settings.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigService:
    """
    Service for managing persistent configuration preferences.
    """

    def __init__(self):
        """
        Initialize the config service and ensure config directory exists.
        """
        # Create the config directory in the user's home directory
        self.config_dir = Path.home() / '.todo'
        self.config_file = self.config_dir / 'config.json'

        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)

        # Initialize config file with defaults if it doesn't exist
        if not self.config_file.exists():
            self._create_default_config()

    def _create_default_config(self) -> None:
        """
        Create a default configuration file.
        """
        default_config = {
            'default_sort_field': 'created',
            'default_sort_order': 'asc',
            'last_used_sort_field': 'created',
            'last_used_sort_order': 'asc'
        }

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)

    def load_config(self) -> Dict[str, Any]:
        """
        Load the configuration from the config file.

        Returns:
            Dictionary containing the configuration settings
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If config file is corrupted or missing, create default config
            self._create_default_config()
            return self.load_config()

    def save_config(self, config: Dict[str, Any]) -> None:
        """
        Save the configuration to the config file.

        Args:
            config: Dictionary containing the configuration settings to save
        """
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Get a specific configuration value.

        Args:
            key: The configuration key to retrieve
            default: Default value to return if key doesn't exist

        Returns:
            The configuration value or default if not found
        """
        config = self.load_config()
        return config.get(key, default)

    def set_config_value(self, key: str, value: Any) -> None:
        """
        Set a specific configuration value.

        Args:
            key: The configuration key to set
            value: The value to set for the key
        """
        config = self.load_config()
        config[key] = value
        self.save_config(config)