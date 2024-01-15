from sqlalchemy import Column, String
from models.base import Base
import uuid

class Tag(Base):
    __tablename__ = "tags"
    # TODO: rename api_payload to action_payload

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tag_alias = Column(String(256), nullable=False)
    description = Column(String)
    api_payload = Column(String, nullable=False)
