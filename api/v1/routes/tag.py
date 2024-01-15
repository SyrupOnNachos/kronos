from http.client import HTTPException
from api.v1.schema.request.discord_message import ActionScript
from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from models import get_db
from models.tag import Tag
from typing import Optional
import logging
import json

app = FastAPI()

tag_router = APIRouter(prefix="/tags", tags=["tags"])

@tag_router.post("/")
def create_tag(tag_alias: str, api_payload: ActionScript, description: Optional[str] = None, db: Session = Depends(get_db)):
    # TODO: add unique name validation
    tag = db.query(Tag).filter(Tag.tag_alias == tag_alias).first()
    if tag:
        raise HTTPException(status_code=400, detail="Tag alias already exists")
    api_payload_json = api_payload.json()
    tag = Tag(tag_alias=tag_alias, api_payload=api_payload_json, description=description)

    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@tag_router.patch("/{tag_id}")
def update_tag(tag_id: str, tag_data: dict, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.tag_alias = tag_data.get("tag_alias", tag.tag_alias)
    tag.description = tag_data.get("description", tag.description)
    tag_api_payload = tag_data.get("api_payload")
    if tag_api_payload:
        tag.api_payload = json.dumps(tag_api_payload)

    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

@tag_router.get("/")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    for tag in tags:
        tag.api_payload = json.loads(tag.api_payload) if tag.api_payload else None
    return tags

@tag_router.get("/health_check")
def health_check():
    return {200: "Boogie Oogie in my Woogie"}
