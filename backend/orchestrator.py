import json
import psycopg2

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "netsentinel"
DB_USER = "postgres"
DB_PASSWORD = "postgres112"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

def get_all_post_ids():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT post_id FROM posts")
    ids = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return ids

def save_analysis(post_id, sentiment=None, sentiment_confidence=None, trend_score=None, is_bot_cluster=None):
    """Upserts into the analysis table so results actually show up through /api/v1/posts."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO analysis (post_id, sentiment, sentiment_confidence, trend_score, network_features)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (post_id) DO UPDATE SET
            sentiment = EXCLUDED.sentiment,
            sentiment_confidence = EXCLUDED.sentiment_confidence,
            trend_score = EXCLUDED.trend_score,
            network_features = EXCLUDED.network_features
    """, (
        post_id, sentiment, sentiment_confidence, trend_score,
        json.dumps({"is_bot_cluster": is_bot_cluster})
    ))
    conn.commit()
    cur.close()
    conn.close()

# --- Placeholder engines (Hitesh will replace these with real AI) ---
def sentiment_engine(post_id):
    return {"sentiment": "neutral", "confidence": 0.5}

def trend_engine(post_id):
    return {"trend_score": 0.0}

def bot_detection_engine(post_id):
    return {"is_bot_cluster": False}

def run_pipeline_once(post_id):
    sentiment_result = sentiment_engine(post_id)
    trend_result = trend_engine(post_id)
    bot_result = bot_detection_engine(post_id)

    save_analysis(
        post_id,
        sentiment=sentiment_result["sentiment"],
        sentiment_confidence=sentiment_result["confidence"],
        trend_score=trend_result["trend_score"],
        is_bot_cluster=bot_result["is_bot_cluster"],
    )
    print(f"Analyzed post {post_id}")

def run_pipeline_all():
    post_ids = get_all_post_ids()
    for pid in post_ids:
        run_pipeline_once(pid)
    print(f"Pipeline run complete — {len(post_ids)} posts analyzed.")

if __name__ == "__main__":
    run_pipeline_all()