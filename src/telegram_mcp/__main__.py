"""Command-line entrypoint for the Telegram Bot MCP server."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="telegram-mcp",
        description="Run the Telegram Bot MCP server.",
    )
    parser.add_argument(
        "--transport",
        choices=("stdio", "sse", "streamable-http"),
        default=None,
        help="FastMCP transport to use. Defaults to MCP_TRANSPORT from settings.",
    )
    parser.add_argument(
        "--host",
        default=None,
        help="Host to bind when using an HTTP-based transport. Defaults to MCP_HOST from settings.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=None,
        help="Port to bind when using an HTTP-based transport. Defaults to MCP_PORT from settings.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Run the Telegram Bot MCP server."""
    from telegram_mcp.config import get_settings
    from telegram_mcp.server import create_server

    args = build_parser().parse_args(argv)
    settings = get_settings()
    server = create_server(settings)

    run_kwargs: dict[str, object] = {
        "transport": args.transport or settings.mcp_transport,
        "host": args.host or settings.mcp_host,
        "port": args.port or settings.mcp_port,
    }

    server.run(**run_kwargs)


if __name__ == "__main__":
    main()
