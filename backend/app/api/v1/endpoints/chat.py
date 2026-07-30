from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies.auth import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.schemas import (
    ChatAskResponse,
    ChatConversationResponse,
    ChatMessageResponse,
    CreateConversationRequest,
    SendMessageRequest,
)
from app.services import (
    AIChatService,
    ChatContextService,
    ChatService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"],
)


# ============================================================
# CONVERSATION ENDPOINTS
# ============================================================


@router.post(
    "/conversations",
    response_model=ChatConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create chat conversation",
)
def create_conversation(
    request: CreateConversationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new chatbot conversation for the
    currently authenticated user.
    """

    service = ChatService(db)

    conversation = service.create_conversation(
        user_id=current_user.id,
        title=request.title,
    )

    return conversation


@router.get(
    "/conversations",
    response_model=list[ChatConversationResponse],
    summary="Get my chat conversations",
)
def get_my_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all chatbot conversations belonging
    to the currently authenticated user.
    """

    service = ChatService(db)

    return service.get_user_conversations(
        user_id=current_user.id,
    )


@router.get(
    "/conversations/{conversation_id}",
    response_model=ChatConversationResponse,
    summary="Get chat conversation",
)
def get_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific conversation belonging
    to the authenticated user.
    """

    service = ChatService(db)

    try:
        return service.get_user_conversation(
            conversation_id=conversation_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.delete(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete chat conversation",
)
def delete_conversation(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a conversation belonging to the
    authenticated user.

    Associated messages are deleted through
    the database cascade.
    """

    service = ChatService(db)

    try:
        service.delete_conversation(
            conversation_id=conversation_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# ============================================================
# MESSAGE ENDPOINTS
# ============================================================


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[ChatMessageResponse],
    summary="Get conversation messages",
)
def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all messages from a conversation
    belonging to the authenticated user.
    """

    service = ChatService(db)

    try:
        return service.get_messages(
            conversation_id=conversation_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# ============================================================
# CHATBOT ENDPOINT
# ============================================================


@router.post(
    "/conversations/{conversation_id}/ask",
    response_model=ChatAskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send message to chatbot",
)
def ask_chatbot(
    conversation_id: UUID,
    request: SendMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Send a message to the Vishwaarpana Havihi chatbot.

    Flow:

    1. Verify conversation ownership.
    2. Load previous conversation history.
    3. Store the user's message.
    4. Fetch structural database context (temples, priests, poojas).
    5. Generate the AI response using context and history.
    6. Store the assistant response.
    7. Return both stored messages.
    """

    chat_service = ChatService(db)
    ai_service = AIChatService()
    context_service = ChatContextService(db)

    try:
        # Verify ownership
        chat_service.get_user_conversation(
            conversation_id=conversation_id,
            user_id=current_user.id,
        )

        # Get previous history
        conversation_history = (
            chat_service.get_conversation_history(
                conversation_id=conversation_id,
                user_id=current_user.id,
            )
        )

        # Save user message
        user_message = chat_service.create_message(
            conversation_id=conversation_id,
            user_id=current_user.id,
            role="USER",
            content=request.message,
        )

        # Retrieve full database context
        database_context = (
            context_service.get_database_context()
        )

        # Generate AI response with database context injection
        ai_response = ai_service.generate_response(
            database_context=database_context,
            conversation_history=conversation_history,
            user_message=request.message,
        )

        # Save assistant message
        assistant_message = chat_service.create_message(
            conversation_id=conversation_id,
            user_id=current_user.id,
            role="ASSISTANT",
            content=ai_response["content"],
            model_name=ai_response["model_name"],
        )

        return ChatAskResponse(
            conversation_id=conversation_id,
            user_message=user_message,
            assistant_message=assistant_message,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service unavailable: {exc}",
        ) from exc


# ============================================================
# INDIVIDUAL MESSAGE OPERATIONS
# ============================================================


@router.delete(
    "/messages/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete chat message",
)
def delete_message(
    message_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete an individual chat message belonging
    to one of the authenticated user's conversations.
    """

    service = ChatService(db)

    try:
        service.delete_message(
            message_id=message_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc