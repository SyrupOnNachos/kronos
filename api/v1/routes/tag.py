import json
from http.client import HTTPException
from typing import Optional

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from api.v1.schema.request.action_script import ActionScript
from models import get_db
from models.tag import Tag

app = FastAPI()

tag_router = APIRouter(prefix="/tags", tags=["tags"])


@tag_router.post("/")
def create_tag(
    tag_alias: str,
    action_script: ActionScript,
    description: Optional[str] = None,
    db: Session = Depends(get_db),
):
    tag = db.query(Tag).filter(Tag.tag_alias == tag_alias).first()
    if tag:
        raise HTTPException(status_code=400, detail="Tag alias already exists")
    action_script_json = action_script.json()
    tag = Tag(
        tag_alias=tag_alias, action_script=action_script_json, description=description
    )

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
    tag_action_script = tag_data.get("action_script")
    if tag_action_script:
        tag.action_script = json.dumps(tag_action_script)

    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


@tag_router.get("/")
def get_tags(tag_alias: Optional[str] = None, db: Session = Depends(get_db)):
    if tag_alias:
        search_pattern = f"%{tag_alias}%"
        tags = db.query(Tag).filter(Tag.tag_alias.ilike(search_pattern)).all()
    else:
        tags = db.query(Tag).all()
    for tag in tags:
        tag.action_script = json.loads(tag.action_script) if tag.action_script else None
    return tags


# TODO: move the health check to a higher url and check for snowflake connection
@tag_router.get("/health_check")
def health_check():
    return {200: "Boogie Oogie in my Woogie"}
