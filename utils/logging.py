"""Centralized logging configuration for the framework."""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str,
    level: Optional[int] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Creates and configures a logger for a module.
    
    Args:
        name: Logger name (typically __name__ of the module)
        level: Logging level (defaults to INFO)
        format_string: Log format string (defaults to standard format)
        
    Returns:
        Configured Logger object
    """
    logger = logging.getLogger(name)
    
    # If logger is already configured, return it
    if logger.handlers:
        return logger
    
    # Set logging level
    if level is None:
        level = logging.INFO
    
    logger.setLevel(level)
    
    # Set log format
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    formatter = logging.Formatter(format_string)
    
    # Console output handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # Prevent log duplication
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a module.
    
    Convenient function for quickly obtaining a configured logger.
    
    Args:
        name: Logger name (typically __name__ of the module)
        
    Returns:
        Configured Logger object
        
    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("Test message")
    """
    return setup_logger(name)



