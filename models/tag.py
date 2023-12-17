from sqlalchemy import Column, Integer, String, JSON
from models.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, index=True, nullable=False)
    description = Column(String, index=True)
    api_payload = Column(JSON, nullable=False)
