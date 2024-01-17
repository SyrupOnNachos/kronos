from typing import Optional

from pydantic import BaseModel


class Action(BaseModel):
    name: str  # Name of the action block
    next_action: Optional[str] = None  # Name of the next action that should be run
    depends_on: Optional[str] = None  # This should be a previous action finder function

    def get_data(self, **kwargs):
        if self.depends_on:
            return kwargs["data"][f"{self.depends_on}"]
        else:
            return None
