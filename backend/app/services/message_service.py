from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.message import Message
from app.schemas.message import MessageCreate


class MessageService:
    @staticmethod
    def get_conversation(
        db: Session,
        current_user_id: int,
        other_user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> List[Message]:
        """
        Returns all messages exchanged between two users, ordered
        chronologically (oldest first).

        Args:
            db: SQLAlchemy database session
            current_user_id: ID of the requesting user
            other_user_id: ID of the conversation partner

        Returns:
            List of Message ORM instances ordered by timestamp ascending.
        """
        return (
            db.query(Message)
            .filter(
                (
                    (Message.sender_id == current_user_id) &
                    (Message.receiver_id == other_user_id)
                ) | (
                    (Message.sender_id == other_user_id) &
                    (Message.receiver_id == current_user_id)
                )
            )
            .order_by(Message.timestamp.asc())
            .offset(skip).limit(limit)
            .all()
        )

    @staticmethod
    def create_message(
        db: Session,
        sender_id: int,
        message_data: MessageCreate
    ) -> Message:
        """
        Persists a new message from sender_id to the receiver specified
        in message_data.

        Args:
            db: SQLAlchemy database session
            sender_id: ID of the authenticated user sending the message
            message_data: Validated payload with receiver_id and content

        Returns:
            The newly created Message ORM instance.
        """
        new_message = Message(
            sender_id=sender_id,
            receiver_id=message_data.receiver_id,
            content=message_data.content
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message

    @staticmethod
    def get_message_by_id(db: Session, message_id: int) -> Optional[Message]:
        """
        Returns a single message by its primary key, or None if not found.

        Args:
            db: SQLAlchemy database session
            message_id: Primary key of the message

        Returns:
            Message ORM instance or None.
        """
        return db.query(Message).filter(Message.id == message_id).first()

    @staticmethod
    def mark_as_read(db: Session, message: Message) -> Message:
        """
        Marks the given message as read.

        Args:
            db: SQLAlchemy database session
            message: The Message ORM instance to update

        Returns:
            The updated Message ORM instance.
        """
        message.is_read = True
        db.commit()
        db.refresh(message)
        return message
