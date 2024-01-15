import logging
from requests import request
from pydantic import BaseModel
from typing import Optional, List, Union


class Action(BaseModel):
    name: str # Name of the action block
    next_action: Optional[str] = None # Name of the next action that should be run

class DiscordMessage(Action):
    message: str
    webhook_id: int
    webhook_token: str
    username: str
    type: Optional[str] = 'disc_message'

    def process_action(self, tag_alias: str):
        logging.info(f"Sending discord api call")
        response = request("POST", f"https://discordapp.com/api/webhooks/{self.webhook_id}/{self.webhook_token}", json={"content": self.message, "username": self.username})
        logging.info(f"Runner tag {tag_alias} - Response: {response.status_code} {response.text}")
        return response.status_code

    
class WeatherCheck(Action):
    location: str
    forecast_url: str
    type: Optional[str] = 'weather_check'
        

action_type_to_class = {
    "disc_message": DiscordMessage,
    "weather_check": WeatherCheck
}

class ActionScript(BaseModel):
    actions: List[Union[DiscordMessage, WeatherCheck]]
    starting_action: str # Name of the action that starts the sequence
