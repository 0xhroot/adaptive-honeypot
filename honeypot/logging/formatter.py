
from datetime import datetime

def _json_safe(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value


def format_event(event_type: str, payload: dict) -> dict:
    safe_payload = {
        key: _json_safe(value)
        for key, value in payload.items()
    }

    return {
        "type": event_type,
        "data": safe_payload
    }

