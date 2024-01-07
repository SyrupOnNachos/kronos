from sqlalchemy import Column, Integer, String
from models.base import Base
import uuid

class Tag(Base):
    __tablename__ = "tags"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tag_id = Column(Integer, nullable=False)
    description = Column(String)
    api_payload = Column(String, nullable=False)
