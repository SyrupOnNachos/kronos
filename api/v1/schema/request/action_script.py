from typing import List, Union

from pydantic import BaseModel, Field

from api.v1.schema.request.spotify import SpotifyPlayPause

from .discord import DiscordMessage
from .utils import TimeCalculate

example_action = [
    {
        "name": "string",
        "next_action": "string",
        "depends_on": "string",
        "type": "string",
    }
]


class ActionScript(BaseModel):
    actions: List[Union[DiscordMessage, TimeCalculate, SpotifyPlayPause]] = Field(
        ..., example=example_action
    )
    starting_action: str  # Name of the action that starts the sequence


action_type_to_class = {
    "disc_message": DiscordMessage,
    "time_calculate": TimeCalculate,
    "spotify_play_pause": SpotifyPlayPause,
}
