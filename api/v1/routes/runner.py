from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from models.tag import Tag
import requests
import logging
import json

app = FastAPI()

runner_router = APIRouter(prefix="/runner", tags=["runners"])
token = '1186049461479293099'


@runner_router.get("/{tag_alias}")
def run_tag(tag_alias: str, db: Session = Depends(get_db)):
    logging.info(f"Running tag: {tag_alias}")
    tag = db.query(Tag).filter(Tag.tag_alias == tag_alias).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    # Extracting the components of the API request from the payload
    try:
        api_payload = json.loads(tag.api_payload)
        url = api_payload["url"]
        method = api_payload.get("method", "GET")
        #  TODO: make it so headers and body are passed in to the api only if they exist
        headers = api_payload.get("headers", {})
        body = api_payload.get("body", {})
    except KeyError:
        raise HTTPException(status_code=400, detail="Malformed API payload")

    # Making the API request
    response = requests.request(method, url, data=body)
    logging.info(f"Runner tag {tag_alias} - Response: {response.status_code} {response.text}")
    return response.text
