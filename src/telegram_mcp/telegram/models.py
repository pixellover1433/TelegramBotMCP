"""Sanitized Telegram response models exposed through MCP tools."""

from __future__ import annotations

from pydantic import BaseModel


class BotInfo(BaseModel):
    """Basic Telegram bot identity information."""

    id: int
    is_bot: bool
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


class ChatInfo(BaseModel):
    """Basic Telegram chat information."""

    id: int
    type: str
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    description: str | None = None
    invite_link: str | None = None


class DeleteMessagesResult(BaseModel):
    """Result returned after deleting Telegram messages."""

    chat_id: int | str
    requested_message_ids: list[int]
    deleted_message_ids: list[int]
    failed_message_ids: list[int]
    deleted_count: int
    failed_count: int
    note: str


class DeleteForumTopicResult(BaseModel):
    """Result returned after deleting a Telegram forum topic."""

    chat_id: int | str
    message_thread_id: int
    deleted: bool
    note: str


class MessageHistoryItem(BaseModel):
    """A sanitized Telegram message history item."""

    message_id: int
    chat_id: int | str
    date: str | None = None
    from_user_id: int | None = None
    from_username: str | None = None
    text: str | None = None
    caption: str | None = None
    content_type: str | None = None


class MessageHistoryResult(BaseModel):
    """Result returned when reading message history for a chat."""

    chat_id: int | str
    messages: list[MessageHistoryItem]
    count: int
    limit: int
    note: str
