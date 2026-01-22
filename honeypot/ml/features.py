"""
Feature extraction from raw events.
"""

def extract_features(events):
    return []
import json
from datetime import datetime
from honeypot.storage.database import get_connection

def extract_features_for_session(session_id: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT event_type, payload, timestamp FROM events WHERE session_id = ?",
        (session_id,),
    )

    rows = cur.fetchall()
    conn.close()

    auth_attempts = 0
    commands = []
    timestamps = []

    for r in rows:
        timestamps.append(datetime.fromisoformat(r["timestamp"]))

        if r["event_type"] == "auth_attempt":
            auth_attempts += 1

        if r["event_type"] == "command":
            payload = json.loads(r["payload"])
            cmd = payload.get("command", "")
            if cmd:
                commands.append(cmd)

    duration = (
        (max(timestamps) - min(timestamps)).total_seconds()
        if len(timestamps) > 1
        else 1
    )

    return {
        "auth_attempts": auth_attempts,
        "command_count": len(commands),
        "unique_commands": len(set(commands)),
        "avg_command_length": (
            sum(len(c) for c in commands) / len(commands)
            if commands else 0
        ),
        "session_duration": duration,
        "command_rate": len(commands) / duration if duration > 0 else 0,
    }
def persist_features(session_id: str, features: dict):
    conn = get_connection()
    cur = conn.cursor()

    for name, value in features.items():
        cur.execute(
            """
            INSERT INTO features (session_id, feature_name, feature_value)
            VALUES (?, ?, ?)
            """,
            (session_id, name, float(value)),
        )

    conn.commit()
    conn.close()

