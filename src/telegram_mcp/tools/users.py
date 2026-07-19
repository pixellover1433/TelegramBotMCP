"""User-related Telegram MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.telegram.models import BotInfo


def register_user_tools(mcp: FastMCP, client: TelegramClient) -> None:
    """Register user and bot identity tools."""

    @mcp.tool()
    async def get_me() -> BotInfo:
        """Return Telegram bot identity information for the configured token."""
        return await client.get_me()
