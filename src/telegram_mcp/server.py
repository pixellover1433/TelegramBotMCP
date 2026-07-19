"""FastMCP server factory for the Telegram Bot MCP server."""

from __future__ import annotations

from fastmcp import FastMCP

from telegram_mcp.config import Settings, get_settings


def create_server(settings: Settings | None = None) -> FastMCP:
    """Create and configure the Telegram Bot MCP server."""
    settings = settings or get_settings()
    mcp = FastMCP(settings.mcp_server_name)

    @mcp.tool()
    async def health_check() -> dict[str, str]:
        """Return a basic health status for the MCP server."""
        return {
            "status": "ok",
            "server": settings.mcp_server_name,
            "transport": settings.mcp_transport,
        }

    return mcp
