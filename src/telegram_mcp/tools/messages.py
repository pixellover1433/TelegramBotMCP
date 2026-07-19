"""Message-related Telegram MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.config import Settings
from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.telegram.models import DeleteMessagesResult, MessageHistoryResult


def _validate_delete_enabled(settings: Settings, message_count: int) -> None:
    """Validate whether message deletion is enabled and within configured limits."""
    if not settings.telegram_enable_delete_messages:
        raise RuntimeError("Message deletion is disabled. Set TELEGRAM_ENABLE_DELETE_MESSAGES=true.")
    if message_count < 1:
        raise ValueError("At least one message ID is required.")
    if message_count > settings.telegram_max_delete_messages:
        raise ValueError(
            f"Cannot delete more than {settings.telegram_max_delete_messages} messages in one call."
        )


def _validate_history_limit(settings: Settings, limit: int) -> None:
    """Validate message history read limits."""
    if limit < 1:
        raise ValueError("limit must be greater than or equal to 1.")
    if limit > settings.telegram_max_history_messages:
        raise ValueError(
            f"Cannot read more than {settings.telegram_max_history_messages} history messages."
        )


def register_message_tools(mcp: FastMCP, client: TelegramClient, settings: Settings) -> None:
    """Register Telegram message tools."""

    @mcp.tool()
    async def delete_message(chat_id: int | str, message_id: int) -> DeleteMessagesResult:
        """Delete one Telegram message from a conversation."""
        _validate_delete_enabled(settings, 1)
        return await client.delete_messages(chat_id=chat_id, message_ids=[message_id])

    @mcp.tool()
    async def delete_messages(chat_id: int | str, message_ids: list[int]) -> DeleteMessagesResult:
        """Delete multiple Telegram messages from a conversation by message IDs."""
        _validate_delete_enabled(settings, len(message_ids))
        return await client.delete_messages(chat_id=chat_id, message_ids=message_ids)

    @mcp.tool()
    async def delete_message_history_range(
        chat_id: int | str,
        start_message_id: int,
        end_message_id: int,
        confirm: bool = False,
    ) -> DeleteMessagesResult:
        """Best-effort delete a message ID range from a conversation.

        Telegram Bot API cannot enumerate an entire conversation history. This tool
        deletes every message ID in the supplied inclusive range. Use only when you
        already know the message ID range to remove.
        """
        if not confirm:
            raise RuntimeError("Set confirm=true to delete a message history range.")
        if start_message_id > end_message_id:
            raise ValueError("start_message_id must be less than or equal to end_message_id.")

        message_ids = list(range(start_message_id, end_message_id + 1))
        _validate_delete_enabled(settings, len(message_ids))
        return await client.delete_messages(chat_id=chat_id, message_ids=message_ids)
