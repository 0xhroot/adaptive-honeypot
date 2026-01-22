
import json
from datetime import datetime
from honeypot.storage.database import get_connection

def log_event(event: dict):
    event["timestamp"] = datetime.utcnow().isoformat()

    # Print JSON (stdout)
    print(json.dumps(event))

    # Persist to DB
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO events (session_id, event_type, payload, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            event["data"].get("session_id"),
            event["type"],
            json.dumps(event["data"]),
            event["timestamp"],
        ),
    )

    conn.commit()
    conn.close()

