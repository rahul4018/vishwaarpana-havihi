from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# CONVERSATION SCHEMAS
# ============================================================


class CreateConversationRequest(BaseModel):
    """
    Request schema for creating a new chat conversation.
    """

    title: str | None = Field(
        default=None,
        max_length=255,
    )


class ChatConversationResponse(BaseModel):
    """
    Response schema for a chat conversation.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    user_id: UUID
    title: str | None
    conversation_status: str
    created_at: datetime
    updated_at: datetime


# ============================================================
# MESSAGE SCHEMAS
# ============================================================


class SendMessageRequest(BaseModel):
    """
    Request schema for sending a message to the chatbot.
    """

    message: str = Field(
        min_length=1,
        max_length=5000,
    )


class ChatMessageResponse(BaseModel):
    """
    Response schema for an individual chat message.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    model_name: str | None
    created_at: datetime


# ============================================================
# AI CHAT RESPONSE
# ============================================================


class ChatAskResponse(BaseModel):
    """
    Response returned after the chatbot processes
    a user's message.
    """

    conversation_id: UUID
    user_message: ChatMessageResponse
    assistant_message: ChatMessageResponse