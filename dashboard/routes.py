from flask import jsonify, render_template
import json
from honeypot.storage.database import get_connection

def register_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/events")
    def events():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT event_type, payload, timestamp
            FROM events
            ORDER BY id DESC
            LIMIT 50
        """)

        rows = cur.fetchall()
        conn.close()

        data = [
            {
                "type": r["event_type"],
                "payload": json.loads(r["payload"]),
                "timestamp": r["timestamp"],
            }
            for r in rows
        ]

        return jsonify(data)

    @app.route("/api/sessions")
    def sessions():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT session_id, ip, start_time
            FROM sessions
            ORDER BY start_time DESC
        """)

        rows = cur.fetchall()
        conn.close()

        return jsonify([dict(r) for r in rows])

    @app.route("/api/profiles")
    def profiles():
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT session_id, profile
            FROM profiles
        """)

        rows = cur.fetchall()
        conn.close()

        return jsonify([dict(r) for r in rows])

