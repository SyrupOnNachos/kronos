from typing import List, Union

from pydantic import BaseModel

from .discord import DiscordMessage
from .utils import TimeCalculate


class ActionScript(BaseModel):
    actions: List[Union[DiscordMessage, TimeCalculate]]
    starting_action: str  # Name of the action that starts the sequence


action_type_to_class = {"disc_message": DiscordMessage, "time_calculate": TimeCalculate}
