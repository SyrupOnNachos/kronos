import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(256), unique=True)
    email = Column(String(256), unique=True)
    password = Column(String)
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_on = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    tokens = relationship("Token", back_populates="user")
