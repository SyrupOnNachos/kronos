import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String

from api.v1.schema.request.utils import Service
from models import SessionLocal
from models.base import Base


class Connection(Base):
    # This used to be the Token model. Connections are for other services.
    __tablename__ = "connections"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # TODO: service should be a restricted sql type
    service = Column(String(256), nullable=False)
    auth_token = Column(String(256))
    created_on = Column(DateTime(timezone=True), default=datetime.utcnow)
    expires_on = Column(DateTime(timezone=True))
    meta_data = Column(String)
    user_id = Column(String(36), ForeignKey("users.id"))

    @classmethod
    def get_connection(cls, user_id: str, service: Service):
        connection = None
        with SessionLocal() as db:
            connection = (
                db.query(cls)
                .filter(cls.user_id == user_id, cls.service == service.value)
                .first()
            )

        return connection
