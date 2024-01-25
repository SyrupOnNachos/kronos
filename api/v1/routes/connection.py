import json
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from api.v1.routes.dependencies import get_current_user
from api.v1.schema.request.utils import Service
from models import get_db
from models.connection import Connection
from models.user import User
from utils.connection import generate_spotify_credentials

app = FastAPI()

connection_router = APIRouter(prefix="/connections", tags=["connections"])


@connection_router.post("/")
def create_connection(
    service: Service,
    auth_token: Optional[str] = None,
    expires_in_seconds: Optional[int] = None,
    meta_data: Optional[dict] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    connection = (
        db.query(Connection)
        .filter(
            Connection.user_id == current_user.id, Connection.service == service.value
        )
        .first()
    )
    if connection:
        raise HTTPException(
            status_code=400,
            detail="Connection already exists with this user_id and service",
        )
    meta_data_json = json.dumps(meta_data) if meta_data else None

    if expires_in_seconds:
        expires_on = datetime.utcnow() + timedelta(seconds=expires_in_seconds)

    connection = Connection(
        user_id=current_user.id,
        service=service.value,
        auth_token=auth_token,
        expires_on=expires_on,
        meta_data=meta_data_json,
    )

    db.add(connection)
    db.commit()
    db.refresh(connection)
    return {
        "Success": "Connection created successfully. You may close this window at any time"
    }


@connection_router.get("/{connection_id}")
def get_connection(
    connection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    connection = (
        db.query(Connection)
        .filter(Connection.id == connection_id, Connection.user_id == current_user.id)
        .first()
    )
    if not connection:
        raise HTTPException(
            status_code=404, detail="Connection not found for this user"
        )
    connection.meta_data = (
        json.loads(connection.meta_data) if connection.meta_data else None
    )
    return connection


@connection_router.get("/")
def get_connections(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    connections = (
        db.query(Connection).filter(Connection.user_id == current_user.id).all()
    )
    for connection in connections:
        connection.meta_data = (
            json.loads(connection.meta_data) if connection.meta_data else None
        )
    return connections


@connection_router.patch("/{connection_id}")
def update_connection(
    connection_id: str,
    connection_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    connection = (
        db.query(Connection)
        .filter(Connection.id == connection_id, Connection.user_id == current_user.id)
        .first()
    )
    if not connection:
        raise HTTPException(
            status_code=404, detail="Connection not found for this user"
        )

    connection.user_id = connection_data.get("user_id", connection.user_id)
    connection.service = connection_data.get("service", connection.service)
    connection.auth_connection = connection_data.get(
        "auth_connection", connection.auth_connection
    )
    expires_in_seconds = connection_data.get("expires_in_seconds")
    if expires_in_seconds:
        connection.expires_on = datetime.utcnow() + timedelta(
            seconds=expires_in_seconds
        )
    connection.meta_data = connection_data.get("meta_data", connection.meta_data)

    db.commit()
    return connection


@connection_router.delete("/{connection_id}")
def delete_connection(
    connection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    connection = (
        db.query(Connection)
        .filter(Connection.id == connection_id, Connection.user_id == current_user.id)
        .first()
    )
    if not connection:
        raise HTTPException(
            status_code=404, detail="Connection not found for this user"
        )

    db.delete(connection)
    db.commit()
    return {"message": "Connection deleted successfully"}


@connection_router.get("/spotify_callback")
def callback(
    code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status_code, response = generate_spotify_credentials(code)

    if status_code != 200:
        raise HTTPException(status_code=status_code, detail=response)

    connection = create_connection(
        service=Service.spotify.value,
        auth_connection=response.get("access_token"),
        expires_in_seconds=response.get("expires_in"),
        db=db,
        current_user=current_user,
        meta_data=response,
    )
    return connection
