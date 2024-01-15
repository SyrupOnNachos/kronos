import calendar
import logging
from datetime import datetime, timedelta
from string import Template
from typing import List, Optional, Union

from pydantic import BaseModel
from requests import request


class Action(BaseModel):
    name: str  # Name of the action block
    next_action: Optional[str] = None  # Name of the next action that should be run


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


class TimeCalculate(Action):
    type: Optional[str] = "time_calculate"
    day_of_week: str
    hour: int
    minute: int

    def process_action(self, **kwargs):
        # Get the current datetime
        now = datetime.now()

        # Convert the input day to a weekday number (0 is Monday, 6 is Sunday)
        target_day = list(calendar.day_name).index(self.day_of_week.title())

        # Calculate how many days to add (0 means today, 7 means the same day next week)
        days_to_add = (target_day - now.weekday() + 7) % 7
        if days_to_add == 0 and (self.hour, self.minute) <= (now.hour, now.minute):
            days_to_add = (
                7  # If it's today but the time has passed, calculate for the next week
            )

        # Calculate the target datetime
        target_datetime = now.replace(
            hour=self.hour, minute=self.minute, second=0, microsecond=0
        ) + timedelta(days=days_to_add)

        # Calculate the difference
        difference = target_datetime - now
        if difference.total_seconds() < 0:
            difference += timedelta(days=7)  # Adjust if we've gone into the past

        # Convert the difference to days, hours, and minutes
        days = difference.days
        hours, remainder = divmod(difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        return {"days": days, "hours": hours, "minutes": minutes, "seconds": seconds}


action_type_to_class = {"disc_message": DiscordMessage, "time_calculate": TimeCalculate}


class ActionScript(BaseModel):
    actions: List[Union[DiscordMessage, TimeCalculate]]
    starting_action: str  # Name of the action that starts the sequence
