from honeypot.storage.database import get_connection

# -------------------------
# Behavior classification
# -------------------------

def classify_profile(features: dict) -> str:
    if features["auth_attempts"] > 5 and features["command_count"] == 0:
        return "bruteforce_bot"

    if features["command_rate"] > 3:
        return "automated_scanner"

    if features["unique_commands"] > 5:
        return "human_interactive"

    return "unknown"


# -------------------------
# Persistence
# -------------------------

def save_profile(session_id: str, profile: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            session_id TEXT PRIMARY KEY,
            profile TEXT
        )
    """)

    cur.execute("""
        INSERT OR REPLACE INTO profiles (session_id, profile)
        VALUES (?, ?)
    """, (session_id, profile))

    conn.commit()
    conn.close()


def load_profile(session_id: str) -> str:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT profile FROM profiles WHERE session_id = ?",
        (session_id,),
    )

    row = cur.fetchone()
    conn.close()

    return row["profile"] if row else "unknown"
