import enum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime, Enum, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class FriendshipStatus(str, enum.Enum):
    pending = "pending"
    accepted = "accepted"


class Friendship(Base):
    __tablename__ = "friendships"
    __table_args__ = (
        UniqueConstraint("requester_id", "addressee_id", name="uq_friendship_pair"),
    )

    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    addressee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(
        Enum(FriendshipStatus, name="friendship_status"),
        nullable=False,
        default=FriendshipStatus.pending,
    )
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    responded_at = Column(DateTime, nullable=True)

    requester = relationship("User", foreign_keys=[requester_id], back_populates="sent_friendships")
    addressee = relationship("User", foreign_keys=[addressee_id], back_populates="received_friendships")
 