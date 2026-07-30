from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.chat_conversation import ChatConversation
from app.db.models.chat_message import ChatMessage
from app.repositories import ChatRepository


class ChatService:
    """
    Service layer for chatbot conversations and messages.

    Handles conversation ownership, conversation management,
    and message persistence.

    AI response generation will be handled separately by an
    AI provider/service layer.
    """

    def __init__(self, db: Session):
        self.db = db
        self.repository = ChatRepository(db)

    # ============================================================
    # CONVERSATION OPERATIONS
    # ============================================================

    def create_conversation(
        self,
        user_id: UUID,
        title: str | None = None,
    ) -> ChatConversation:
        """
        Create a new chatbot conversation for a user.
        """

        return self.repository.create_conversation(
            user_id=user_id,
            title=title,
        )

    def get_conversation(
        self,
        conversation_id: UUID,
    ) -> ChatConversation:
        """
        Get a conversation by ID.

        Raises ValueError if the conversation does not exist.
        """

        conversation = (
            self.repository.get_conversation_by_id(
                conversation_id
            )
        )

        if conversation is None:
            raise ValueError(
                "Chat conversation not found."
            )

        return conversation

    def get_user_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> ChatConversation:
        """
        Get a conversation belonging to a specific user.

        This prevents users from accessing conversations
        belonging to other users.
        """

        conversation = (
            self.repository.get_user_conversation_by_id(
                conversation_id=conversation_id,
                user_id=user_id,
            )
        )

        if conversation is None:
            raise ValueError(
                "Chat conversation not found or access denied."
            )

        return conversation

    def get_user_conversations(
        self,
        user_id: UUID,
    ) -> list[ChatConversation]:
        """
        Get all chatbot conversations belonging to a user.
        """

        return (
            self.repository.get_conversations_by_user_id(
                user_id
            )
        )

    def update_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
        title: str | None = None,
        conversation_status: str | None = None,
    ) -> ChatConversation:
        """
        Update a user's chatbot conversation.
        """

        conversation = self.get_user_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        updates = {}

        if title is not None:
            updates["title"] = title

        if conversation_status is not None:
            updates[
                "conversation_status"
            ] = conversation_status.upper()

        if not updates:
            return conversation

        return self.repository.update_conversation(
            conversation,
            **updates,
        )

    def delete_conversation(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Delete a conversation belonging to a user.

        Associated chat messages will be removed through
        database cascade.
        """

        conversation = self.get_user_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        self.repository.delete_conversation(
            conversation
        )

    # ============================================================
    # MESSAGE OPERATIONS
    # ============================================================

    def create_message(
        self,
        conversation_id: UUID,
        user_id: UUID,
        role: str,
        content: str,
        model_name: str | None = None,
    ) -> ChatMessage:
        """
        Create and store a message in a user's conversation.
        """

        self.get_user_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        normalized_role = role.upper()

        allowed_roles = {
            "USER",
            "ASSISTANT",
            "SYSTEM",
        }

        if normalized_role not in allowed_roles:
            raise ValueError(
                "Invalid message role. "
                "Allowed roles are USER, ASSISTANT, and SYSTEM."
            )

        cleaned_content = content.strip()

        if not cleaned_content:
            raise ValueError(
                "Message content cannot be empty."
            )

        message = self.repository.create_message(
            conversation_id=conversation_id,
            role=normalized_role,
            content=cleaned_content,
            model_name=model_name,
        )

        # Touch the conversation so updated_at reflects
        # recent activity.
        conversation = self.get_user_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        self.repository.update_conversation(
            conversation
        )

        return message

    def get_messages(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> list[ChatMessage]:
        """
        Get all messages from a user's conversation.
        """

        self.get_user_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        return (
            self.repository.get_messages_by_conversation_id(
                conversation_id
            )
        )

    def get_message(
        self,
        message_id: UUID,
        user_id: UUID,
    ) -> ChatMessage:
        """
        Get an individual message while verifying
        conversation ownership.
        """

        message = self.repository.get_message_by_id(
            message_id
        )

        if message is None:
            raise ValueError(
                "Chat message not found."
            )

        self.get_user_conversation(
            conversation_id=message.conversation_id,
            user_id=user_id,
        )

        return message

    def delete_message(
        self,
        message_id: UUID,
        user_id: UUID,
    ) -> None:
        """
        Delete an individual message after verifying
        conversation ownership.
        """

        message = self.get_message(
            message_id=message_id,
            user_id=user_id,
        )

        self.repository.delete_message(
            message
        )

    # ============================================================
    # CHAT CONTEXT
    # ============================================================

    def get_conversation_history(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ) -> list[dict[str, str]]:
        """
        Return conversation history in a format suitable
        for sending to an AI/LLM provider.
        """

        messages = self.get_messages(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        history = []

        for message in messages:
            history.append(
                {
                    "role": message.role.lower(),
                    "content": message.content,
                }
            )

        return history