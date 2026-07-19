"""aiogram bot factory."""

from __future__ import annotations

from aiogram import Bot

from telegram_mcp.config import Settings


def create_bot(settings: Settings) -> Bot:
    """Create an aiogram bot from application settings."""
    token = settings.telegram_bot_token_value
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is required to use Telegram tools.")

    return Bot(token=token)
