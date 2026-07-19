"""User-related Telegram MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.telegram.models import BotInfo


def register_user_tools(mcp: FastMCP, client: TelegramClient) -> None:
    """Register user and bot identity tools."""

    @mcp.tool()
    async def get_me(telegram_bot_token: str) -> BotInfo:
        """Return Telegram bot identity information for the supplied token."""
        return await client.get_me(telegram_bot_token)
