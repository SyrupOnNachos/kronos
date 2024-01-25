import json
import logging

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.v1.routes.dependencies import get_current_user
from api.v1.schema.request.action_script import action_type_to_class
from models import get_db
from models.tag import Tag
from models.user import User

app = FastAPI()

runner_router = APIRouter(prefix="/runner", tags=["runners"])


@runner_router.get("/{tag_alias}")
def run_tag(
    tag_alias: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logging.info(f"Running tag: {tag_alias}")
    tag = (
        db.query(Tag)
        .filter(Tag.tag_alias == tag_alias, Tag.user_id == current_user.id)
        .first()
    )
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found for this user")
    try:
        action_script = json.loads(tag.action_script)

        response = {}

        action_class = None
        for action in action_script["actions"]:
            if action["name"] == action_script["starting_action"]:
                action_class = action_type_to_class[action["type"]]
                action_class = action_class(**action)
                break
        while action_class:
            response[action_class.name] = action_class.process_action(
                tag_alias=tag_alias, data=response
            )
            if action_class.next_action:
                next_action = next(
                    (
                        action
                        for action in action_script["actions"]
                        if action["name"] == action_class.next_action
                    ),
                    None,
                )
                action_class = action_type_to_class[next_action["type"]]
                action_class = action_class(**next_action)
            else:
                break

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Malformed API payload - {e}",
        )

    return response
