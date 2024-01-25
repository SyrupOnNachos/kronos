import json

from requests import request

from utils.connection import generate_spotify_credentials

from .actions import Action


class SpotifyPlayPause(Action):
    """
    Plays or pauses playback on Spotify based on the action payload
    """

    user_id: str
    type: str = "spotify_play_pause"

    def process_action(self, **kwargs):
        auth_connection = generate_spotify_credentials(self.user_id)

        method = "GET"

        url = "https://api.spotify.com/v1/me/player"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_connection}",
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
