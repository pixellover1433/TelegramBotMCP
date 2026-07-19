"""Application settings for the Telegram Bot MCP server."""

from __future__ import annotations

from functools import lru_cache
from typing import Annotated, Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Transport = Literal["stdio", "sse", "streamable-http"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def _parse_array_values(value: str) -> list[str]:
    """Parse a JSON-like array or comma-separated environment value into strings."""
    stripped_value = value.strip()
    if stripped_value in {"", "[]"}:
        return []
    if stripped_value.startswith("[") and stripped_value.endswith("]"):
        stripped_value = stripped_value[1:-1]
    return [item.strip().strip('"\'') for item in stripped_value.split(",") if item.strip()]


class Settings(BaseSettings):
    """Centralized environment-backed application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="TELEGRAM_MCP_",
        extra="ignore",
    )

    telegram_bot_token: SecretStr | None = Field(
        default=None,
        alias="TELEGRAM_BOT_TOKEN",
        description="Telegram Bot API token issued by BotFather.",
    )
    telegram_allowed_chat_ids: list[str] = Field(
        default_factory=list,
        alias="TELEGRAM_ALLOWED_CHAT_IDS",
        description="JSON-like array allowlist of Telegram chat IDs/usernames.",
    )
    telegram_blocked_chat_ids: list[str] = Field(
        default_factory=list,
        alias="TELEGRAM_BLOCKED_CHAT_IDS",
        description="JSON-like array blocklist of Telegram chat IDs/usernames.",
    )
    telegram_enable_send_messages: bool = Field(
        default=False,
        alias="TELEGRAM_ENABLE_SEND_MESSAGES",
        description="Whether MCP tools are allowed to send Telegram messages.",
    )
    telegram_enable_file_downloads: bool = Field(
        default=False,
        alias="TELEGRAM_ENABLE_FILE_DOWNLOADS",
        description="Whether MCP tools are allowed to download Telegram files.",
    )
    telegram_max_message_length: Annotated[int, Field(ge=1, le=4096)] = Field(
        default=4096,
        alias="TELEGRAM_MAX_MESSAGE_LENGTH",
        description="Maximum Telegram message text length accepted by tools.",
    )
    telegram_max_file_size_bytes: Annotated[int, Field(ge=1)] = Field(
        default=5 * 1024 * 1024,
        alias="TELEGRAM_MAX_FILE_SIZE_BYTES",
        description="Maximum Telegram file size allowed for downloads/uploads.",
    )
    telegram_request_timeout_seconds: Annotated[float, Field(gt=0)] = Field(
        default=30.0,
        alias="TELEGRAM_REQUEST_TIMEOUT_SECONDS",
        description="Timeout for Telegram Bot API requests in seconds.",
    )

    log_enabled: bool = Field(
        default=True,
        alias="LOG_ENABLED",
        description="Whether application logging is enabled.",
    )
    log_level: LogLevel = Field(
        default="INFO",
        alias="LOG_LEVEL",
        description="Application log level.",
    )
    log_aiogram_enabled: bool = Field(
        default=False,
        alias="LOG_AIOGRAM_ENABLED",
        description="Whether verbose aiogram logging is enabled.",
    )
    log_fastmcp_enabled: bool = Field(
        default=False,
        alias="LOG_FASTMCP_ENABLED",
        description="Whether verbose FastMCP logging is enabled.",
    )

    rate_limit_requests: Annotated[int, Field(ge=1)] = Field(
        default=30,
        alias="RATE_LIMIT_REQUESTS",
        description="Maximum tool calls allowed during one rate-limit window.",
    )
    rate_limit_window_seconds: Annotated[int, Field(ge=1)] = Field(
        default=60,
        alias="RATE_LIMIT_WINDOW_SECONDS",
        description="Rate-limit window size in seconds.",
    )

    mcp_server_name: str = Field(
        default="telegram-bot-mcp",
        alias="MCP_SERVER_NAME",
        description="FastMCP server name exposed to MCP clients.",
    )
    mcp_transport: Transport = Field(
        default="streamable-http",
        alias="MCP_TRANSPORT",
        description="Default FastMCP transport.",
    )
    mcp_host: str = Field(
        default="127.0.0.1",
        alias="MCP_HOST",
        description="Default host for HTTP-based MCP transports.",
    )
    mcp_port: Annotated[int, Field(ge=1, le=65535)] = Field(
        default=51000,
        alias="MCP_PORT",
        description="Default port for HTTP-based MCP transports.",
    )

    @field_validator("telegram_allowed_chat_ids", "telegram_blocked_chat_ids", mode="before")
    @classmethod
    def parse_chat_ids(cls, value: object) -> object:
        """Allow chat IDs to be configured as arrays or comma-separated strings."""
        if value is None or value == "":
            return []
        if isinstance(value, str):
            return _parse_array_values(value)
        if isinstance(value, list | tuple | set):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @property
    def telegram_bot_token_value(self) -> str | None:
        """Return the raw Telegram bot token for aiogram initialization."""
        if self.telegram_bot_token is None:
            return None
        return self.telegram_bot_token.get_secret_value()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    import os

    env_file = os.environ.get("TELEGRAM_MCP_ENV_FILE")
    if env_file:
        return Settings(_env_file=env_file)
    return Settings()
