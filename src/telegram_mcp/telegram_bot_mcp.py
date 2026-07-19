"""Compatibility runner for the Telegram Bot MCP server.

The main script was moved to ../telegram_bot_mcp.py. This wrapper keeps this
command working from inside src/telegram_mcp:

    python telegram_bot_mcp.py
"""

from __future__ import annotations

import runpy
from pathlib import Path


def main() -> None:
    """Run the moved script entrypoint."""
    runner = Path(__file__).resolve().parent.parent / "telegram_bot_mcp.py"
    runpy.run_path(str(runner), run_name="__main__")


if __name__ == "__main__":
    main()
