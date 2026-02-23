"""
Utility functions for datetime operations.
Includes:
- Conversion from ISO 8601 strings to datetime objects
- Formatting datetime objects to a specific timezone.

Author: Kavith Ranchagoda
"""

from datetime import datetime
from zoneinfo import ZoneInfo


def iso_to_datetime(iso_str: str) -> datetime:
    # Convert ISO 8601 string to datetime object, handling 'Z' for UTC
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


def format_datetime(dt: datetime, tz: str = "America/New_York") -> dict[str, int | str]:
    # Convert the datetime to the specified local timezone
    local_dt = dt.astimezone(ZoneInfo(tz))

    # return a dictionary with day, month, year, and time
    return {
        "day": local_dt.day,
        "month": local_dt.month,
        "year": local_dt.year,
        "time": local_dt.strftime("%H:%M"),
    }
