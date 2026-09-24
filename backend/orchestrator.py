import time
import json
import psycopg2

# --- DB connection ---
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

def save_to_db(engine_name, post_id, result):
    """Saves one engine's result + auto-timestamp into engine_results."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO engine_results (engine_name, post_id, result)
        VALUES (%s, %s, %s)
    """, (engine_name, post_id, json.dumps(result)))
    conn.commit()
    cur.close()
    conn.close()
    print(f"[{engine_name}] saved result for post {post_id} at {time.strftime('%H:%M:%S')}")

# --- Placeholder engines (Hitesh will replace these with real AI later) ---
def sentiment_engine(post_id):
    time.sleep(1)  # simulates work being done
    return {"sentiment": "neutral", "confidence": 0.5}

def trend_engine(post_id):
    time.sleep(1)
    return {"topic": "placeholder", "momentum": "stable"}

def bot_detection_engine(post_id):
    time.sleep(1)
    return {"is_bot_cluster": False, "confidence": 0.0}

# --- The "traffic controller": runs ONE engine at a time, in order ---
def run_pipeline_once(post_id):
    engines = [
        ("sentiment", sentiment_engine),
        ("trend", trend_engine),
        ("bot_detection", bot_detection_engine),
    ]
    for name, engine_func in engines:
        result = engine_func(post_id)   # run this engine fully
        save_to_db(name, post_id, result)  # save before starting the next one
        # because this loop is a plain "for" loop (not parallel),
        # engine N+1 can never start until engine N finishes here.

if __name__ == "__main__":
    run_pipeline_once("test_post_001")
    print("Pipeline run complete — check engine_results table.")