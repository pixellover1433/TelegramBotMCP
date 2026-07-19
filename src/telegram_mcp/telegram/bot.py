"""aiogram bot factory."""

from __future__ import annotations

from aiogram import Bot

from telegram_mcp.config import Settings


def create_bot_from_token(token: str) -> Bot:
    """Create an aiogram bot from a Telegram Bot API token."""
    if not token:
        raise ValueError("Telegram bot token is required.")

    return Bot(token=token)


def create_bot(settings: Settings) -> Bot | None:
    """Create an aiogram bot from application settings when a token is configured."""
    token = settings.telegram_bot_token_value
    if not token:
        return None

    return create_bot_from_token(token)
