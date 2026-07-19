"""Chat-related Telegram MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.config import Settings
from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.telegram.models import ChatInfo, DeleteForumTopicResult


def register_chat_tools(mcp: FastMCP, client: TelegramClient, settings: Settings) -> None:
    """Register Telegram chat tools."""

    @mcp.tool()
    async def get_chat_infomations(chat_id: int | str) -> ChatInfo:
        """Return Telegram chat information for a chat ID or username."""
        return await client.get_chat_infomations(chat_id)

    @mcp.tool()
    async def delete_forum_topic(
        chat_id: int | str,
        message_thread_id: int,
        confirm: bool = False,
    ) -> DeleteForumTopicResult:
        """Delete a forum topic from a Telegram forum supergroup."""
        if not settings.telegram_enable_delete_topics:
            raise RuntimeError("Forum topic deletion is disabled. Set TELEGRAM_ENABLE_DELETE_TOPICS=true.")
        if not confirm:
            raise RuntimeError("Set confirm=true to delete a forum topic.")
        return await client.delete_forum_topic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        )
