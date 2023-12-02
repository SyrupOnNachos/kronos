from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session
from models import get_db
from models.tag import Tag

app = FastAPI()

tag_router = APIRouter(prefix="/tags", tags=["tags"])

@tag_router.post("/")
def create_tag(tag_id: int, action: str, db: Session = Depends(get_db)):
    db_tag = Tag(tag_id=tag_id, action=action)
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
    return {200: "We boogie woogie"}