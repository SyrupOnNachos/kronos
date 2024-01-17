import json
import logging
import os
from base64 import b64encode
from datetime import datetime, timedelta
from http.client import HTTPException

from requests import request

from api.v1.schema.request.utils import Service
from models import SessionLocal
from models.token import Token

from .actions import Action

# TODO: Need to add functionality to actually allow user to give permissions.
# Likely will be done when frontend is created

def refresh_token(user_id):
    logging.info("Refreshing Spotify access token")

    token = Token.get_token(user_id, Service.spotify)

    expires_on = token.expires_on
    if expires_on < datetime.utcnow():
        client_id = os.getenv("SPOTIFY_CLIENT_ID")
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        token = None
        refresh_token = None

        with SessionLocal() as db:
            token = Token.get_token(user_id, Service.spotify)
            if token:
                meta_data = json.loads(token.meta_data)
                refresh_token = meta_data["refresh_token"]
            else:
                raise HTTPException(status_code=400, detail="No Spotify token found")

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
                token.auth_token = response["access_token"]
                token.expires_on = datetime.utcnow() + timedelta(
                    seconds=response["expires_in"]
                )
                db.add(token)
                db.commit()
                db.refresh(token)
        except Exception as e:
            logging.error(f"Error replacing Spotify auth token token in db: {e}")
            return HTTPException(
                status_code=400, detail=f"Error refreshing Spotify token in db: {e}"
            )

        token = Token.get_token(user_id, Service.spotify)

    auth_token = token.auth_token
    return auth_token


class SpotifyPlayPause(Action):
    """
    Plays or pauses playback on Spotify based on the action payload
    """

    user_id: str
    type: str = "spotify_play_pause"

    def process_action(self, **kwargs):
        auth_token = refresh_token(self.user_id)

        method = "GET"

        url = "https://api.spotify.com/v1/me/player"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}",
        }

        response = request(method, url, headers=headers)
        if response.reason == "No Content":
            return {"status": 204, "message": "No Spotify device is currently playing"}
        response = json.loads(response.text)
        is_playing = response["is_playing"]
        if is_playing:
            method = "PUT"
            url = f"https://api.spotify.com/v1/me/player/pause"
        else:
            method = "PUT"
            url = f"https://api.spotify.com/v1/me/player/play"

        response = request(method, url, headers=headers)
        return response.text
