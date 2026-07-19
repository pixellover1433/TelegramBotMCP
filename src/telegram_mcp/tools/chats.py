"""Chat-related Telegram MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.telegram.models import ChatInfo


def register_chat_tools(mcp: FastMCP, client: TelegramClient) -> None:
    """Register Telegram chat tools."""

    @mcp.tool()
    async def get_chat(chat_id: int | str) -> ChatInfo:
        """Return Telegram chat information for a chat ID or username."""
        return await client.get_chat(chat_id)
