from fastapi import FastAPI, Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from models import get_db
from models.tag import Tag
import requests
import logging

app = FastAPI()

runner_router = APIRouter(prefix="/runner", tags=["runners"])
token = '1186049461479293099'


@runner_router.post("/{tag_id}")
def run_tag(tag_id: int, db: Session = Depends(get_db)):
    logging.info(f"Running tag: {tag_id}")
    print(f"Running tag: {tag_id}")
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    api_payload = tag.api_payload
    # Extracting the components of the API request from the payload
    try:
        api_payload = tag.api_payload
        url = api_payload["url"]
        method = api_payload.get("method", "GET")
        #  TODO: make it so headers and body are passed in to the api only if they exist
        headers = api_payload.get("headers", {})
        body = api_payload.get("body", {})
    except KeyError:
        raise HTTPException(status_code=400, detail="Malformed API payload")

    # Making the API request
    response = requests.request(method, url)
    print(f"response: {response}")
    print(f"response text: {response.text}")
    return response.text
