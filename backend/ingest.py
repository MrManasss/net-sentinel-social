import json
import psycopg2

# --- Database connection settings ---
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "netsentinel"
DB_USER = "postgres"
DB_PASSWORD = "postgres112"

# --- Load the sample data ---
with open("data/sample_social_media.json", "r", encoding="utf-8") as f:
    records = json.load(f)

conn = psycopg2.connect(
    host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
    user=DB_USER, password=DB_PASSWORD
)
cur = conn.cursor()

inserted = 0

for rec in records:
    rec.pop("scenario", None)  # test-only field, strip before insert

    author = rec.get("author", {}) or {}
    engagement = rec.get("engagement", {}) or {}

    cur.execute("""
        INSERT INTO authors (author_id, display_name, platform, account_created_at, followers, following)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (author_id) DO NOTHING
    """, (
        rec.get("author_id"),
        author.get("display_name"),
        rec.get("platform"),
        author.get("account_created_at"),
        author.get("followers"),
        author.get("following"),
    ))

    cur.execute("""
        INSERT INTO posts (post_id, platform, source_id, author_id, text, timestamp,
                            language, hashtags, reply_to, likes, comments, shares, views)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (post_id) DO NOTHING
    """, (
        rec.get("post_id"),
        rec.get("platform"),
        rec.get("source_id"),
        rec.get("author_id"),
        rec.get("text"),
        rec.get("timestamp"),
        rec.get("language"),
        rec.get("hashtags", []),
        rec.get("reply_to"),
        engagement.get("likes", 0),
        engagement.get("comments", 0),
        engagement.get("shares", 0),
        engagement.get("views", 0),
    ))

    inserted += 1

conn.commit()
cur.close()
conn.close()

print(f"Done. Inserted/processed {inserted} posts.")