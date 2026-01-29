from datetime import datetime
from zoneinfo import ZoneInfo


def iso_to_datetime(iso_str: str) -> datetime:
    """Convert ISO 8601 string to datetime object."""
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


def format_datetime(dt: datetime, tz: str = "America/New_York") -> dict[str, int | str]:
    local_dt = dt.astimezone(ZoneInfo(tz))
    return {
        "day": local_dt.day,
        "month": local_dt.month,
        "year": local_dt.year,
        "time": local_dt.strftime("%H:%M"),
    }
