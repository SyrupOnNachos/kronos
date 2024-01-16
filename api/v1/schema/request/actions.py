from typing import Optional

from pydantic import BaseModel


class Action(BaseModel):
    name: str  # Name of the action block
    next_action: Optional[str] = None  # Name of the next action that should be run
