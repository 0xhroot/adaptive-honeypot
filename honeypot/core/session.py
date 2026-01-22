from dataclasses import dataclass
from datetime import datetime
from honeypot.storage.database import get_connection

@dataclass
class Session:
    session_id: str
    ip: str
    port: int
    start_time: datetime

    def save(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT OR IGNORE INTO sessions
            (session_id, ip, port, start_time)
            VALUES (?, ?, ?, ?)
            """,
            (
                self.session_id,
                self.ip,
                self.port,
                self.start_time.isoformat(),
            ),
        )

        conn.commit()
        conn.close()
