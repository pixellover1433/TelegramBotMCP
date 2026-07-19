"""Chat-related Telegram MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.config import Settings
from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.telegram.models import ChatInfo, DeleteForumTopicResult


def register_chat_tools(mcp: FastMCP, client: TelegramClient) -> None:
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
        if not confirm:
            raise RuntimeError("Set confirm=true to delete a forum topic.")
        return await client.delete_forum_topic(
            chat_id=chat_id,
            message_thread_id=message_thread_id,
        )
