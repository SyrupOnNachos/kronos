import json
import logging
from base64 import b64encode
from datetime import datetime, timedelta
from os import getenv

from fastapi import HTTPException
from requests import request
from starlette import status

from api.v1.schema.request.utils import Service
from models import SessionLocal
from models.connection import Connection


def generate_spotify_credentials(code: str):
    grant_type = "authorization_code"
    redirect_uri = getenv("SPOTIFY_REDIRECT_URI")
    client_id = getenv("SPOTIFY_CLIENT_ID")
    client_secret = getenv("SPOTIFY_CLIENT_SECRET")
    method = "POST"
    url = "https://accounts.spotify.com/api/token"
    payload = f"grant_type={grant_type}&code={code}&redirect_uri={redirect_uri}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
    }
    response = request(method, url, headers=headers, data=payload)
    response_json = json.loads(response.text)
    return response.status_code, response_json


def refresh_spotify_credentials(user_id):
    logging.info("Refreshing Spotify access connection")

    connection = Connection.get_connection(user_id, Service.spotify)

    expires_on = connection.expires_on
    if expires_on < datetime.utcnow():
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        connection = None
        refresh_token = None

        with SessionLocal() as db:
            connection = Connection.get_connection(user_id, Service.spotify)
            if connection:
                meta_data = json.loads(connection.meta_data)
                refresh_token = meta_data["refresh_token"]
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No Spotify connection found",
                )

        grant_type = "refresh_token"

        method = "POST"
        url = "https://accounts.spotify.com/api/token"

        payload = f"grant_type={grant_type}&refresh_token={refresh_token}"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64encode(f'{client_id}:{client_secret}'.encode()).decode()}",
        }

        response = request(method, url, headers=headers, data=payload)
        response = json.loads(response.text)

        try:
            with SessionLocal() as db:
                connection.auth_token = response["access_token"]
                connection.expires_on = datetime.utcnow() + timedelta(
                    seconds=response["expires_in"]
                )
                db.add(connection)
                db.commit()
                db.refresh(connection)
        except Exception as e:
            logging.error(f"Error replacing Spotify auth token in db: {e}")
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error refreshing Spotify connection in db: {e}",
            )

        connection = Connection.get_connection(user_id, Service.spotify)

    auth_token = connection.auth_token
    return auth_token
