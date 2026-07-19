"""FastMCP server factory for the Telegram Bot MCP server."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.config import Settings, get_settings
from telegram_mcp.telegram.bot import create_bot
from telegram_mcp.telegram.client import TelegramClient
from telegram_mcp.tools.chats import register_chat_tools
from telegram_mcp.tools.messages import register_message_tools
from telegram_mcp.tools.users import register_user_tools


def create_server(settings: Settings | None = None) -> FastMCP:
    """Create and configure the Telegram Bot MCP server."""
    settings = settings or get_settings()
    mcp = FastMCP(settings.mcp_server_name)
    bot = create_bot(settings)
    telegram_client = TelegramClient(bot)
    register_user_tools(mcp, telegram_client)
    register_chat_tools(mcp, telegram_client)
    register_message_tools(mcp, telegram_client, settings)

    @mcp.tool()
    async def health_check() -> dict[str, str]:
        """Return a basic health status for the MCP server."""
        return {
            "status": "ok",
            "server": settings.mcp_server_name,
            "transport": settings.mcp_transport,
        }

    return mcp
