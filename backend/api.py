from fastapi import FastAPI
import psycopg2
import psycopg2.extras

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "netsentinel"
DB_USER = "postgres"
DB_PASSWORD = "postgres112"

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

@app.get("/latest-results")
def latest_results():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT engine_name, post_id, result, created_at
        FROM engine_results
        ORDER BY created_at DESC
        LIMIT 10
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"latest": rows}