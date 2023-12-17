from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from models import get_db
from models.tag import Tag
from schemas.tag import CreateTagSchema
from typing import Optional
import logging

app = FastAPI()

tag_router = APIRouter(prefix="/tags", tags=["tags"])

@tag_router.post("/")
def create_tag(tag_id: int, api_payload: dict, description: Optional[str] = None, db: Session = Depends(get_db)):
    logging.info(f"Input params: tag_id={tag_id}, api_payload={api_payload}, description={description}")
    print(f"Input params: tag_id={tag_id}, api_payload={api_payload}, description={description}")
    db_tag = Tag(tag_id=tag_id, api_payload=api_payload, description=description)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@tag_router.get("/")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return tags

@tag_router.get("/health_check")
def health_check():
    return {200: "Boogie Oogie in my Woogie"}
