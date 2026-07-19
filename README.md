# Telegram Bot MCP

A FastMCP server that exposes Telegram Bot API operations as Model Context Protocol (MCP) tools. The server uses `aiogram` for Telegram Bot API calls and `pydantic-settings` for environment-based configuration.

## Requirements

- Python 3.10 or newer
- A Telegram bot token from [BotFather](https://t.me/BotFather)
- An MCP-compatible client that can connect over `streamable-http`, `sse`, or `stdio`

## Installation

1. Clone or download this project.

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```


3. Create your environment file.

   ```bash
   cp .env.example .env
   ```

   On Windows PowerShell:

   ```powershell
   Copy-Item .env.example .env
   ```

5. Edit `.env` as needed for server transport, logging, and safety limits. (logging and safety limits currently not working)

## Running the server

Run from the project root:

```bash
python telegram_bot_mcp.py
```

The default transport is `streamable-http` on `127.0.0.1:51000`.

You can override transport, host, and port with command-line arguments:

```bash
python telegram_bot_mcp.py --transport streamable-http --host 127.0.0.1 --port 51000
```

Supported transport values are:

- `streamable-http`
- `sse`
- `stdio`

## MCP client configuration example

For a client that launches the server with a command, use a configuration similar to:

```json
{
  "mcpServers": {
    "telegram-bot-mcp": {
      "command": "python",
      "args": ["telegram_bot_mcp.py", "--transport", "stdio"]
    }
  }
}
```

For HTTP-based clients, start the server with `streamable-http` and configure the client to connect to:

```text
http://127.0.0.1:51000/mcp
```

## Supported MCP tools

### Server tools

| Tool | Description |
| --- | --- |
| `health_check` | Returns basic MCP server status, server name, and active transport. |

### User and bot identity tools

| Tool | Parameters | Description |
| --- | --- | --- |
| `get_me` | `telegram_bot_token: string` | Returns sanitized identity information for the supplied Telegram bot token. |

### Chat tools

| Tool | Parameters | Description |
| --- | --- | --- |
| `get_chat_infomations` | `telegram_bot_token: string`, `chat_id: int \| string` | Returns sanitized Telegram chat information for a chat ID or username. Note: the tool name currently uses `infomations` as implemented in the project. |
| `delete_forum_topic` | `telegram_bot_token: string`, `chat_id: int \| string`, `message_thread_id: int`, `confirm: boolean = false` | Deletes a forum topic from a Telegram forum supergroup. Requires `confirm=true`. |

### Message tools

| Tool | Parameters | Description |
| --- | --- | --- |
| `delete_message` | `telegram_bot_token: string`, `chat_id: int \| string`, `message_id: int` | Deletes one Telegram message from a conversation. |
| `delete_messages` | `telegram_bot_token: string`, `chat_id: int \| string`, `message_ids: int[]` | Deletes multiple Telegram messages by explicit message IDs. Limited to 100 message IDs per call. |
| `delete_message_history_range` | `telegram_bot_token: string`, `chat_id: int \| string`, `start_message_id: int`, `end_message_id: int`, `confirm: boolean = false` | Best-effort deletion of every message ID in an inclusive range. Requires `confirm=true` and is limited to 100 message IDs per call. |

## Telegram Bot API limitations

Telegram bots can only perform actions allowed by the Telegram Bot API and the bot's permissions in each chat. In particular:

- The bot must be a member of the target chat.
- Administrative permissions may be required for deleting messages or forum topics.
- The Telegram Bot API cannot enumerate an entire chat history for deletion.
- Message deletion is best-effort and may fail for messages the bot is not allowed to delete.