"""Script entrypoint for running the Telegram Bot MCP server directly.

This file allows running the project from the src directory with:

    python telegram_bot_mcp.py

It also works when invoked from another working directory, for example:

    python src/telegram_bot_mcp.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    """Run the Telegram Bot MCP server using the package CLI entrypoint."""
    src_dir = Path(__file__).resolve().parent
    src_dir_text = str(src_dir)
    env_file = src_dir / ".env"

    if src_dir_text not in sys.path:
        sys.path.insert(0, src_dir_text)

    # Make settings load the .env file that lives beside this runner, regardless
    # of the current working directory used to start the process.
    os.environ.setdefault("TELEGRAM_MCP_ENV_FILE", str(env_file))

    from telegram_mcp.__main__ import main as package_main

    package_main()


if __name__ == "__main__":
    main()
