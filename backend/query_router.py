"""
query_router.py

Query/analytics endpoints for Net-Sentinel Social.
- Posts filtered by date range
- Sentiment breakdown over time (covers #19: historical/timestamped queries)
- Top hashtags / trending topics

Follows the same pattern as network_router.py: a standalone APIRouter that
imports shared helpers from main.py and gets wired into the app there with:

    from query_router import router as query_router
    app.include_router(query_router)
"""

from collections import Counter
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
import psycopg2.extras

from main import get_db_connection, load_posts  # reuse backend's DB connection + loader, don't duplicate it
from models import Post

router = APIRouter(prefix="/api/v1", tags=["query"])


def _parse_date(value: str, param_name: str) -> datetime:
    """Accepts 'YYYY-MM-DD' or full ISO timestamps."""
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {param_name} '{value}'. Use YYYY-MM-DD or ISO 8601 (e.g. 2026-09-01T00:00:00)."
        )


# ---------------------------------------------------------------------------
# 1. Posts filtered by date range
# ---------------------------------------------------------------------------
@router.get("/posts/by-date", response_model=list[Post])
def get_posts_by_date(
    start: Optional[str] = Query(None, description="Start date, e.g. 2026-09-01"),
    end: Optional[str] = Query(None, description="End date, e.g. 2026-09-27"),
    platform: Optional[str] = Query(None, description="Optional platform filter"),
):
    """Return posts with timestamp in [start, end], inclusive. Both bounds optional."""
    start_dt = _parse_date(start, "start") if start else None
    end_dt = _parse_date(end, "end") if end else None

    raw = load_posts()

    if start_dt:
        raw = [p for p in raw if p["timestamp"] and p["timestamp"] >= start_dt]
    if end_dt:
        raw = [p for p in raw if p["timestamp"] and p["timestamp"] <= end_dt]
    if platform:
        raw = [p for p in raw if p["platform"] == platform]

    return [Post(**p) for p in raw]


# ---------------------------------------------------------------------------
# 2. Sentiment breakdown over time (folds in #19 - historical/time-windowed queries)
# ---------------------------------------------------------------------------
@router.get("/analytics/sentiment-over-time")
def sentiment_over_time(
    interval: str = Query("day", pattern="^(hour|day)$", description="Bucket size: 'hour' or 'day'"),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
):
    """
    Returns sentiment counts grouped by time bucket, e.g.:
    [
      {"bucket": "2026-09-25", "sentiment": "Supportive", "count": 12},
      {"bucket": "2026-09-25", "sentiment": "Against", "count": 4},
      ...
    ]
    """
    date_trunc_unit = "hour" if interval == "hour" else "day"

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """
        SELECT
            date_trunc(%s, p.timestamp) AS bucket,
            an.sentiment AS sentiment,
            COUNT(*) AS count
        FROM posts p
        JOIN analysis an ON p.post_id = an.post_id
        WHERE an.sentiment IS NOT NULL
    """
    params: list = [date_trunc_unit]

    if start:
        query += " AND p.timestamp >= %s"
        params.append(_parse_date(start, "start"))
    if end:
        query += " AND p.timestamp <= %s"
        params.append(_parse_date(end, "end"))

    query += " GROUP BY bucket, an.sentiment ORDER BY bucket ASC"

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "bucket": r["bucket"].isoformat() if r["bucket"] else None,
            "sentiment": r["sentiment"],
            "count": r["count"],
        }
        for r in rows
    ]


# ---------------------------------------------------------------------------
# 3. Top hashtags / trending topics
# ---------------------------------------------------------------------------
@router.get("/analytics/top-hashtags")
def top_hashtags(
    limit: int = Query(10, ge=1, le=100),
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
):
    """
    Returns the most frequent hashtags across posts in the given window, e.g.:
    [{"hashtag": "#election2026", "count": 37}, ...]
    """
    start_dt = _parse_date(start, "start") if start else None
    end_dt = _parse_date(end, "end") if end else None

    raw = load_posts()

    if start_dt:
        raw = [p for p in raw if p["timestamp"] and p["timestamp"] >= start_dt]
    if end_dt:
        raw = [p for p in raw if p["timestamp"] and p["timestamp"] <= end_dt]

    counter: Counter = Counter()
    for p in raw:
        for tag in (p.get("hashtags") or []):
            counter[tag] += 1

    top = counter.most_common(limit)
    return [{"hashtag": tag, "count": count} for tag, count in top]