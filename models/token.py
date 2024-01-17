import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String

from api.v1.schema.request.utils import Service
from models import SessionLocal
from models.base import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(256), nullable=False)
    # TODO: service should be a restricted sql type
    service = Column(String(256), nullable=False)
    auth_token = Column(String(256))
    created_on = Column(DateTime, default=datetime.utcnow)
    expires_on = Column(DateTime)
    meta_data = Column(String)

    @classmethod
    def get_token(cls, user_id: str, service: Service):
        token = None
        with SessionLocal() as db:
            token = (
                db.query(cls)
                .filter(cls.user_id == user_id, cls.service == service.value)
                .first()
            )

        return token
