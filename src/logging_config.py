"""Centralized logging configuration for the Eden Agent."""

import logging
import sys
from typing import Optional
from rich.logging import RichHandler
from rich.console import Console

# Create console for rich output
console = Console()


def setup_logging(
    level: str = "INFO",
    format_string: Optional[str] = None,
    enable_rich: bool = True,
) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string for log messages
        enable_rich: Whether to use rich formatting
        
    Returns:
        Configured logger instance
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Default format if none provided
    if format_string is None:
        format_string = "%(message)s"
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add appropriate handler
    if enable_rich:
        handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_time=True,
            show_path=True,
        )
    else:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(format_string)
        handler.setFormatter(formatter)
    
    handler.setLevel(numeric_level)
    root_logger.addHandler(handler)
    
    # Get application logger
    logger = logging.getLogger("eden_agent")
    logger.setLevel(numeric_level)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a specific module."""
    return logging.getLogger(f"eden_agent.{name}")


# Initialize default logger
logger = setup_logging()
