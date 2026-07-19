"""Sanitized Telegram response models exposed through MCP tools."""

from __future__ import annotations

from pydantic import BaseModel


class BotInfo(BaseModel):
    """Basic Telegram bot identity information."""

    id: int
    is_bot: bool
    is_premium: bool
    allows_users_to_create_topics: bool
    can_manage_bots: bool
    first_name: str
    username: str | None = None
    can_join_groups: bool | None = None
    can_read_all_group_messages: bool | None = None
    supports_inline_queries: bool | None = None


class SetMeResult(BaseModel):
    """Result returned after changing the runtime Telegram bot token."""

    status: str
    message: str
    bot: BotInfo
