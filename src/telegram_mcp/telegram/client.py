"""Telegram API service wrapper."""

from __future__ import annotations

from aiogram import Bot

from telegram_mcp.telegram.models import BotInfo


class TelegramClient:
    """Small wrapper around aiogram's Bot API client."""

    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def get_me(self) -> BotInfo:
        """Return sanitized Telegram bot identity information."""
        user = await self._bot.get_me()
        return BotInfo(
            id=user.id,
            is_bot=user.is_bot,
            first_name=user.first_name,
            username=user.username,
            can_join_groups=user.can_join_groups,
            can_read_all_group_messages=user.can_read_all_group_messages,
            supports_inline_queries=user.supports_inline_queries,
        )
