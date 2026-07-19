"""User-related Telegram MCP tools."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.telegram.models import BotInfo, SetMeResult


def register_user_tools(mcp: FastMCP, client: TelegramClient) -> None:
    """Register user and bot identity tools."""

    @mcp.tool()
    async def get_me() -> BotInfo:
        """Return Telegram bot identity information for the configured token."""
        return await client.get_me()

    @mcp.tool()
    async def set_me(token: str) -> SetMeResult:
        """Change the active Telegram bot token at runtime and return the new bot identity."""
        bot_info = await client.set_bot_token(token)
        return SetMeResult(
            status="ok",
            message="Telegram bot token changed for the current server process.",
            bot=bot_info,
        )
