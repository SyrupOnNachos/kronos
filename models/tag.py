from sqlalchemy import Column, Integer, String
from models.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    tag_id = Column(Integer, index=True)
    action = Column(String, index=True)
