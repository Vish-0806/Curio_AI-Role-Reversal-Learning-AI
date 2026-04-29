"""
Curio AI — Structured Logging Setup.

Provides JSON-like structured logging with request ID propagation.
Usage:
    from app.utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Something happened", extra={"request_id": "req-123"})
"""

import logging
import json
import sys
from datetime import datetime, timezone
from typing import Optional


class StructuredFormatter(logging.Formatter):
    """Format log records as JSON-like structured dicts."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include request_id if available
        request_id = getattr(record, "request_id", None)
        if request_id:
            log_entry["request_id"] = request_id

        # Include extra fields
        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = {
                "type": type(record.exc_info[1]).__name__,
                "message": str(record.exc_info[1]),
            }

        # Include any custom extra fields
        standard_attrs = {
            "name", "msg", "args", "created", "relativeCreated",
            "exc_info", "exc_text", "stack_info", "lineno", "funcName",
            "filename", "module", "pathname", "levelname", "levelno",
            "msecs", "thread", "threadName", "process", "processName",
            "taskName", "message", "request_id",
        }
        for key, value in record.__dict__.items():
            if key not in standard_attrs:
                log_entry[key] = value

        return json.dumps(log_entry, default=str)


def _setup_root_logger(level: str = "INFO") -> None:
    """Configure the root logger with structured formatting."""
    root_logger = logging.getLogger("curio")
    if root_logger.handlers:
        return  # Already configured

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Get a named logger under the 'curio' namespace.

    Args:
        name: Logger name (typically __name__)
        level: Optional override for log level

    Returns:
        Configured logger instance
    """
    _setup_root_logger(level or "INFO")
    logger = logging.getLogger(f"curio.{name}")
    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    return logger
