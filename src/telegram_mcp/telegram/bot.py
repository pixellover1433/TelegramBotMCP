"""aiogram bot factory."""

from __future__ import annotations

from aiogram import Bot


def create_bot_from_token(token: str) -> Bot:
    """Create an aiogram bot from a Telegram Bot API token."""
    if not token:
        raise ValueError("Telegram bot token is required.")

    return Bot(token=token)


