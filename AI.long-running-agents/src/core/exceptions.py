"""Custom exceptions for the long-running-agents system."""


class AgentError(Exception):
    """Base exception for all agent-related errors."""
    pass


class LLMError(AgentError):
    """Exception raised when LLM operations fail."""
    pass


class ConfigurationError(AgentError):
    """Exception raised when configuration is invalid."""
    pass


class FeatureError(AgentError):
    """Exception raised when feature operations fail."""
    pass


class GitError(AgentError):
    """Exception raised when git operations fail."""
    pass
