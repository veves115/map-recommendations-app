from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/{user_id}", response_model=list[MessageResponse],status_code=status.HTTP_200_OK)
def get_conversation(
    user_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Return the full message history between the authenticated user and user_id,
    ordered chronologically (oldest message first).

    - **user_id**: ID of the conversation partner
    """ 
    return MessageService.get_conversation(
        db,
        current_user_id=current_user.id,
        other_user_id=user_id,
        skip=skip,
        limit=limit
    )


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send a message to another user.

    - **receiver_id**: ID of the recipient
    - **content**: Text content of the message

    Returns 400 if the user tries to send a message to themselves.
    """
    if message_data.receiver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes enviarte un mensaje a ti mismo"
        )

    return MessageService.create_message(db, sender_id=current_user.id, message_data=message_data)


@router.patch("/{message_id}/read", response_model=MessageResponse)
def mark_message_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mark a message as read.

    Only the intended receiver of the message can mark it as read.
    Returns 404 if the message does not exist and 403 if the current
    user is not the receiver.
    """
    message = MessageService.get_message_by_id(db, message_id)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensaje no encontrado"
        )

    if message.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para marcar este mensaje como leído"
        )

    return MessageService.mark_as_read(db, message)
