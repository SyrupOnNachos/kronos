import json
from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from api.v1.schema.request.utils import Service
from models import get_db
from models.token import Token
from datetime import datetime, timedelta

app = FastAPI()

token_router = APIRouter(prefix="/tokens", tags=["tokens"])


@token_router.post("/")
def create_token(
    user_id: str,
    service: Service,
    auth_token: Optional[str] = None,
    expires_in_seconds: Optional[int] = None,
    meta_data: Optional[dict] = None,
    db: Session = Depends(get_db),
):
    token = (
        db.query(Token)
        .filter(Token.user_id == user_id, Token.service == service.value)
        .first()
    )
    if token:
        raise HTTPException(
            status_code=400, detail="Token already exists with this user_id and service"
        )
    meta_data_json = json.dumps(meta_data) if meta_data else None

    if expires_in_seconds:
        expires_on = datetime.utcnow() + timedelta(seconds=expires_in_seconds) 

    token = Token(
        user_id=user_id,
        service=service.value,
        auth_token=auth_token,
        expires_on=expires_on,
        meta_data=meta_data_json,
    )

    db.add(token)
    db.commit()
    db.refresh(token)
    return token


@token_router.get("/{token_id}")
def get_token(token_id: str, db: Session = Depends(get_db)):
    token = db.query(Token).filter(Token.id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")
    token.meta_data = json.loads(token.meta_data) if token.meta_data else None
    return token


@token_router.get("/")
def get_tokens(db: Session = Depends(get_db)):
    tokens = db.query(Token).all()
    for token in tokens:
        token.meta_data = json.loads(token.meta_data) if token.meta_data else None
    return tokens


@token_router.patch("/{token_id}")
def update_token(token_id: str, token_data: dict, db: Session = Depends(get_db)):
    token = db.query(Token).filter(Token.id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    token.user_id = token_data.get("user_id", token.user_id)
    token.service = token_data.get("service", token.service)
    token.auth_token = token_data.get("auth_token", token.auth_token)
    expires_in_seconds = token_data.get("expires_in_seconds")
    if expires_in_seconds:
        token.expires_on = datetime.utcnow() + timedelta(seconds=expires_in_seconds) 
    token.meta_data = token_data.get("meta_data", token.meta_data)

    db.commit()
    return token

@token_router.delete("/{token_id}")
def delete_token(token_id: str, db: Session = Depends(get_db)):
    token = db.query(Token).filter(Token.id == token_id).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    db.delete(token)
    db.commit()
    return {"message": "Token deleted successfully"}