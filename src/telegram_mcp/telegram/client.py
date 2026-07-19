"""Telegram API service wrapper."""

from __future__ import annotations

from aiogram import Bot

from telegram_mcp.telegram.bot import create_bot_from_token
from telegram_mcp.telegram.models import BotInfo, ChatInfo


class TelegramClient:
    """Small wrapper around aiogram's Bot API client."""

    def __init__(self, bot: Bot | None = None) -> None:
        self._bot = bot

    def has_bot(self) -> bool:
        """Return whether a Telegram bot is currently configured."""
        return self._bot is not None

    async def set_bot_token(self, token: str) -> BotInfo:
        """Replace the active Telegram bot token at runtime and return bot identity."""
        new_bot = create_bot_from_token(token)
        old_bot = self._bot
        self._bot = new_bot

        try:
            bot_info = await self.get_me()
        except Exception:
            self._bot = old_bot
            await new_bot.session.close()
            raise

        if old_bot is not None:
            await old_bot.session.close()

        return bot_info

    async def get_me(self) -> BotInfo:
        """Return sanitized Telegram bot identity information."""
        if self._bot is None:
            raise RuntimeError("Telegram bot token is not configured. Call set_me first.")

        user = await self._bot.get_me()
        return BotInfo(
            id=user.id,
            is_bot=user.is_bot,
            allows_users_to_create_topics=user.allows_users_to_create_topics,
            can_manage_bots=user.can_manage_bots,
            first_name=user.first_name,
            username=user.username,
            can_join_groups=user.can_join_groups,
            can_read_all_group_messages=user.can_read_all_group_messages,
            supports_inline_queries=user.supports_inline_queries,
        )

    async def get_chat(self, chat_id: int | str) -> ChatInfo:
        """Return sanitized Telegram chat information."""
        if self._bot is None:
            raise RuntimeError("Telegram bot token is not configured. Call set_me first.")

        chat = await self._bot.get_chat(chat_id=chat_id)
        return ChatInfo(
            id=chat.id,
            type=chat.type,
            title=getattr(chat, "title", None),
            username=getattr(chat, "username", None),
            first_name=getattr(chat, "first_name", None),
            last_name=getattr(chat, "last_name", None),
            description=getattr(chat, "description", None),
            invite_link=getattr(chat, "invite_link", None),
        )
