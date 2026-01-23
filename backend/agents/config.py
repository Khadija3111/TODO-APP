"""
Configuration for the AI Chat Agent
Sets up Cohere integration with OpenAI Agents SDK
"""

import os
from typing import Dict, Any
from openai import OpenAI
import cohere


class AgentConfig:
    """
    Configuration class for the AI Chat Agent
    """

    # Get API keys from environment variables
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # May be needed for MCP compatibility

    # Model configurations
    COHERE_MODEL = os.getenv("COHERE_MODEL", "command-r-08-2024")  # Default Cohere model (current available model)
    TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("AGENT_MAX_TOKENS", "2000"))

    # Validation
    @classmethod
    def validate_config(cls):
        """
        Validate that required configuration is present
        """
        if not cls.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY environment variable is required")

        return True

    @classmethod
    def get_cohere_client(cls):
        """
        Initialize and return a Cohere client
        """
        if not cls.COHERE_API_KEY:
            raise ValueError("COHERE_API_KEY is not set in environment variables")

        return cohere.Client(api_key=cls.COHERE_API_KEY)

    @classmethod
    def get_openai_client(cls):
        """
        Initialize and return an OpenAI client (for MCP compatibility)
        """
        # We'll configure this to work with Cohere through proxy or compatible endpoint
        # In a real implementation, this would point to a Cohere-compatible endpoint
        api_key = cls.OPENAI_API_KEY or cls.COHERE_API_KEY

        if not api_key:
            raise ValueError("Either OPENAI_API_KEY or COHERE_API_KEY must be set")

        # Use a dummy OpenAI client setup for MCP compatibility
        # Actual implementation would use Cohere's API directly or through a compatible interface
        return OpenAI(api_key=api_key)


# Global configuration instance
agent_config = AgentConfig()


def init_agent():
    """
    Initialize the agent with required configuration
    """
    agent_config.validate_config()
    print("Agent configuration initialized successfully")