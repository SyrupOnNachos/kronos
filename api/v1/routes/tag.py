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
def create_tag(tag_alias: str, api_payload: dict, description: Optional[str] = None, db: Session = Depends(get_db)):
    # TODO: add unique name validation
    api_payload_json = json.dumps(api_payload)
    db_tag = Tag(tag_alias=tag_alias, api_payload=api_payload_json, description=description)

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@tag_router.get("/")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    for tag in tags:
        tag.api_payload = json.loads(tag.api_payload) if tag.api_payload else None
    return tags

@tag_router.get("/health_check")
def health_check():
    return {200: "Boogie Oogie in my Woogie"}
