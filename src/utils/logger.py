"""Logging configuration"""
from loguru import logger
import sys
from pathlib import Path
from src.config import LOGS_DIR, LOG_LEVEL

# Remove default logger
logger.remove()

# Add console handler
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=LOG_LEVEL
)

# Add file handler
logger.add(
    LOGS_DIR / "app_{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="30 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=LOG_LEVEL
)

# Export logger
__all__ = ["logger"]