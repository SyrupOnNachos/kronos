
import logging
from string import Template
from typing import Optional

from .actions import Action
from requests import request


class DiscordMessage(Action):
    message: str
    webhook_id: int
    webhook_token: str
    username: str
    depends_on: Optional[str] = None  # This should be a previous action finder function
    type: Optional[str] = "disc_message"

    def process_action(self, **kwargs):
        logging.info(f"Sending discord api call")
        tag_alias = kwargs["tag_alias"]
        message = self.message

        if self.depends_on:
            data = kwargs["data"][f"{self.depends_on}"]
            message = Template(message)
            message = message.substitute(data)

        response = request(
            "POST",
            f"https://discordapp.com/api/webhooks/{self.webhook_id}/{self.webhook_token}",
            json={"content": message, "username": self.username},
        )
        logging.info(
            f"Runner tag {tag_alias} - Response: {response.status_code} {response.text}"
        )
        return response.status_code
