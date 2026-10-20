"""Small, explicit helpers for reading validation and data quality."""

from datetime import datetime, timezone


def utc_iso(timestamp: datetime) -> str:
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def freshness_warning(timestamp: datetime, now: datetime | None = None) -> str | None:
    now = now or datetime.now(timezone.utc)
    age_minutes = (now - timestamp.astimezone(timezone.utc)).total_seconds() / 60
    if age_minutes > 120:
        return f"Latest reading is {age_minutes / 60:.1f} hours old; the score may not reflect current conditions."
    if age_minutes < -5:
        return "Latest reading timestamp is in the future; verify the source clock."
    return None
