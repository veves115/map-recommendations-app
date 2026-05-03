from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.database import Base


class FriendInvite(Base):
    __tablename__ = "friend_invites"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, nullable=False, unique=True, index=True)
    code = Column(String(6), nullable=False, unique=True, index=True)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
    used_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    inviter = relationship("User", foreign_keys=[inviter_id], back_populates="sent_invites")
    used_by = relationship("User", foreign_keys=[used_by_id])
