from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.chat_conversation import ChatConversation
from app.db.models.chat_message import ChatMessage


class ChatRepository:
    """
    Repository for chatbot conversations and messages.
    """

    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CONVERSATION OPERATIONS
    # ============================================================

    def create_conversation(
        self,
        user_id: UUID,
        title: str | None = None,
    ) -> ChatConversation:
        """
        Create a new chatbot conversation.
        """

        conversation = ChatConversation(
            user_id=user_id,
            title=title,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_conversation_by_id(
        self,
        conversation_id: UUID,
    ) -> ChatConversation | None:
        """
        Get a conversation by ID.
        """

        statement = select(
            ChatConversation
        ).where(
            ChatConversation.id == conversation_id
        )

        return self.db.scalar(statement)

    def get_user_conversation_by_id(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> ChatConversation | None:
        """
        Get a conversation only if it belongs to the specified user.
        """

        statement = select(
            ChatConversation
        ).where(
            ChatConversation.id == conversation_id,
            ChatConversation.user_id == user_id,
        )

        return self.db.scalar(statement)

    def get_conversations_by_user_id(
        self,
        user_id: UUID,
    ) -> list[ChatConversation]:
        """
        Get all conversations belonging to a user.
        """

        statement = (
            select(ChatConversation)
            .where(
                ChatConversation.user_id == user_id
            )
            .order_by(
                ChatConversation.updated_at.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update_conversation(
        self,
        conversation: ChatConversation,
        **updates,
    ) -> ChatConversation:
        """
        Update conversation fields.
        """

        for field, value in updates.items():
            if hasattr(conversation, field):
                setattr(
                    conversation,
                    field,
                    value,
                )

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def delete_conversation(
        self,
        conversation: ChatConversation,
    ) -> None:
        """
        Delete a conversation.

        Associated messages are deleted automatically
        through database cascade.
        """

        self.db.delete(conversation)
        self.db.commit()

    # ============================================================
    # MESSAGE OPERATIONS
    # ============================================================

    def create_message(
        self,
        conversation_id: UUID,
        role: str,
        content: str,
        model_name: str | None = None,
    ) -> ChatMessage:
        """
        Store a new message in a conversation.
        """

        message = ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
            model_name=model_name,
        )

        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_message_by_id(
        self,
        message_id: UUID,
    ) -> ChatMessage | None:
        """
        Get a chat message by ID.
        """

        statement = select(
            ChatMessage
        ).where(
            ChatMessage.id == message_id
        )

        return self.db.scalar(statement)

    def get_messages_by_conversation_id(
        self,
        conversation_id: UUID,
    ) -> list[ChatMessage]:
        """
        Get all messages in a conversation
        ordered from oldest to newest.
        """

        statement = (
            select(ChatMessage)
            .where(
                ChatMessage.conversation_id
                == conversation_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def delete_message(
        self,
        message: ChatMessage,
    ) -> None:
        """
        Delete an individual chat message.
        """

        self.db.delete(message)
        self.db.commit()