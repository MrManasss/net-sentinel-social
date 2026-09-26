import json
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
import psycopg2
import psycopg2.extras

from models import Post

app = FastAPI(
    title="Net-Sentinel Social API",
    description="Backend API for the Net-Sentinel Social platform (SIH26152)",
    version="0.1.0",
)

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "netsentinel"
DB_USER = "postgres"
DB_PASSWORD = "postgres112"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )

def load_posts() -> list[dict]:
    """Load posts from PostgreSQL, joined into the nested shape Post expects."""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT
            p.post_id, p.platform, p.source_id, p.author_id, p.text, p.timestamp,
            p.language, p.hashtags, p.reply_to,
            p.likes, p.comments, p.shares, p.views,
            a.display_name, a.account_created_at, a.followers, a.following,
            an.sentiment, an.sentiment_confidence, an.demographics, an.topics,
            an.trend_score, an.network_features,
            s.record_hash, s.previous_hash, s.audit_timestamp
        FROM posts p
        LEFT JOIN authors a ON p.author_id = a.author_id
        LEFT JOIN analysis an ON p.post_id = an.post_id
        LEFT JOIN security_log s ON p.post_id = s.post_id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    posts = []
    for r in rows:
        posts.append({
            "post_id": r["post_id"],
            "platform": r["platform"],
            "source_id": r["source_id"],
            "author_id": r["author_id"],
            "text": r["text"],
            "timestamp": r["timestamp"],
            "language": r["language"],
            "hashtags": r["hashtags"] or [],
            "reply_to": r["reply_to"],
            "engagement": {
                "likes": r["likes"],
                "comments": r["comments"],
                "shares": r["shares"],
                "views": r["views"],
            },
            "author": {
                "display_name": r["display_name"],
                "account_created_at": r["account_created_at"],
                "followers": r["followers"],
                "following": r["following"],
                "karma": None,
            },
            "analysis": {
                "sentiment": r["sentiment"],
                "sentiment_confidence": r["sentiment_confidence"],
                "demographics": r["demographics"] or {},
                "topics": r["topics"] or [],
                "trend_score": r["trend_score"],
                "network_features": r["network_features"] or {},
            },
            "security": {
                "record_hash": r["record_hash"],
                "previous_hash": r["previous_hash"],
                "audit_timestamp": r["audit_timestamp"],
            },
        })
    return posts

@app.get("/")
def root():
    return {"status": "ok", "service": "net-sentinel-social-api"}

@app.get("/api/v1/posts", response_model=list[Post])
def get_posts(platform: Optional[str] = None):
    raw = load_posts()
    if platform:
        raw = [p for p in raw if p["platform"] == platform]
    return [Post(**p) for p in raw]

@app.get("/api/v1/posts/{post_id}", response_model=Post)
def get_post(post_id: str):
    raw = load_posts()
    match = next((p for p in raw if p["post_id"] == post_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Post not found")
    return Post(**match)

