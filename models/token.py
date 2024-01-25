import uuid
from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class Token(Base):
    # Tokens handle login sessions for users.

    __tablename__ = "tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_on = Column(
        DateTime(timezone=True), default=lambda: datetime.utcnow() + timedelta(days=1)
    )
    user_id = Column(String(36), ForeignKey("users.id"))

    user = relationship("User", back_populates="tokens")
