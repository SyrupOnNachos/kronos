import calendar
from datetime import datetime, timedelta
from typing import Optional

from .actions import Action


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
