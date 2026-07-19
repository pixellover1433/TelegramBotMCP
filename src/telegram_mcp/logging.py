"""Logging configuration for the Telegram Bot MCP server."""

from __future__ import annotations

import logging
import sys

from telegram_mcp.config import Settings, get_settings

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(settings: Settings | None = None) -> None:
    """Configure application logging from settings."""
    settings = settings or get_settings()

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    if not settings.log_enabled:
        logging.disable(logging.CRITICAL)
        root_logger.addHandler(logging.NullHandler())
        return

    logging.disable(logging.NOTSET)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT))

    root_logger.addHandler(handler)
    root_logger.setLevel(settings.log_level)

    logging.getLogger("telegram_mcp").setLevel(settings.log_level)

    if not settings.log_aiogram_enabled:
        logging.getLogger("aiogram").setLevel(logging.WARNING)

    if not settings.log_fastmcp_enabled:
        logging.getLogger("fastmcp").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger for application modules."""
    return logging.getLogger(name)
