from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from models.tag import Tag
import requests
import logging
import json
from api.v1.schema.request.discord_message import action_type_to_class

app = FastAPI()

runner_router = APIRouter(prefix="/runner", tags=["runners"])


@runner_router.get("/{tag_alias}")
def run_tag(tag_alias: str, db: Session = Depends(get_db)):
    logging.info(f"Running tag: {tag_alias}")
    tag = db.query(Tag).filter(Tag.tag_alias == tag_alias).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    # Extracting the components of the API request from the payload
    try:
        api_payload = json.loads(tag.api_payload)

        response = {}

        action_class = None
        for action in api_payload["actions"]:
            if action["name"] == api_payload["starting_action"]:
                action_class = action_type_to_class[action["type"]]
                action_class = action_class(**action)
                break
        while action_class:
            response[action_class.name] = action_class.process_action(tag_alias)
            if action_class.next_action:
                next_action = next(
                    (
                        action
                        for action in api_payload["actions"]
                        if action["name"] == action_class.next_action
                    ),
                    None,
                )
                action_class = action_type_to_class[next_action["type"]]
                action_class = action_class(**next_action)
            else:
                break

    except KeyError:
        raise HTTPException(status_code=400, detail="Malformed API payload")

    # Making the API request
 
    return response
