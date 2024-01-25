import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String

from models.base import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tag_alias = Column(String(256), nullable=False)
    description = Column(String)
    action_script = Column(String, nullable=False)
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow)
    user_id = Column(String(36), ForeignKey("users.id"))
