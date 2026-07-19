"""Telegram API service wrapper."""

from __future__ import annotations

from telegram_mcp.telegram.bot import create_bot_from_token
from telegram_mcp.telegram.models import (
    BotInfo,
    ChatInfo,
    DeleteForumTopicResult,
    DeleteMessagesResult,
)


class TelegramClient:
    """Small wrapper around aiogram's Bot API client."""

    async def get_me(self, telegram_bot_token: str) -> BotInfo:
        """Return sanitized Telegram bot identity information."""
        bot = create_bot_from_token(telegram_bot_token)
        try:
            user = await bot.get_me()
        finally:
            await bot.session.close()
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

    async def delete_messages(
        self,
        telegram_bot_token: str,
        chat_id: int | str,
        message_ids: list[int],
    ) -> DeleteMessagesResult:
        """Best-effort delete Telegram messages by explicit message IDs."""
        bot = create_bot_from_token(telegram_bot_token)
        deleted_message_ids: list[int] = []
        failed_message_ids: list[int] = []

        try:
            for message_id in message_ids:
                try:
                    deleted = await bot.delete_message(chat_id=chat_id, message_id=message_id)
                except Exception:
                    failed_message_ids.append(message_id)
                    continue

                if deleted:
                    deleted_message_ids.append(message_id)
                else:
                    failed_message_ids.append(message_id)
        finally:
            await bot.session.close()

        return DeleteMessagesResult(
            chat_id=chat_id,
            requested_message_ids=message_ids,
            deleted_message_ids=deleted_message_ids,
            failed_message_ids=failed_message_ids,
            deleted_count=len(deleted_message_ids),
            failed_count=len(failed_message_ids),
            note=(
                "Telegram Bot API can delete only messages the bot is allowed to delete, "
                "usually recent messages in chats where it has sufficient permissions. "
                "It cannot enumerate and wipe an entire chat history automatically."
            ),
        )

    async def delete_forum_topic(
        self,
        telegram_bot_token: str,
        chat_id: int | str,
        message_thread_id: int,
    ) -> DeleteForumTopicResult:
        """Delete a Telegram forum topic by message thread ID."""
        bot = create_bot_from_token(telegram_bot_token)
        try:
            deleted = await bot.delete_forum_topic(
                chat_id=chat_id,
                message_thread_id=message_thread_id,
            )
        finally:
            await bot.session.close()
        return DeleteForumTopicResult(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
            deleted=deleted,
            note=(
                "Telegram can delete forum topics only in forum supergroups where "
                "the bot has sufficient administrator permissions."
            ),
        )

    async def get_chat_infomations(self, telegram_bot_token: str, chat_id: int | str) -> ChatInfo:
        """Return sanitized Telegram chat information."""
        bot = create_bot_from_token(telegram_bot_token)
        try:
            chat = await bot.get_chat(chat_id=chat_id)
        finally:
            await bot.session.close()
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
