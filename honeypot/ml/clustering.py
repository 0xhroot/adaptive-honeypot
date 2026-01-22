"""
Clustering logic.
"""

def cluster(features):
    return []
import numpy as np
from sklearn.cluster import DBSCAN
from honeypot.storage.database import get_connection

def load_feature_matrix():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT session_id, feature_name, feature_value
        FROM features
    """)

    rows = cur.fetchall()
    conn.close()

    sessions = {}
    for r in rows:
        sessions.setdefault(r["session_id"], {})[r["feature_name"]] = r["feature_value"]

    session_ids = []
    vectors = []

    for sid, feats in sessions.items():
        vector = [
            feats.get("auth_attempts", 0),
            feats.get("command_count", 0),
            feats.get("unique_commands", 0),
            feats.get("avg_command_length", 0),
            feats.get("session_duration", 0),
            feats.get("command_rate", 0),
        ]
        session_ids.append(sid)
        vectors.append(vector)

    return session_ids, np.array(vectors)

def cluster_sessions():
    session_ids, X = load_feature_matrix()
    if len(X) < 2:
        return {}

    model = DBSCAN(eps=2.5, min_samples=2)
    labels = model.fit_predict(X)

    return dict(zip(session_ids, labels))

