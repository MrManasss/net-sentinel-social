import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException

from models import Post

app = FastAPI(
    title="Net-Sentinel Social API",
    description="Backend API for the Net-Sentinel Social platform (SIH26152)",
    version="0.1.0",
)

DATA_FILE = Path(__file__).parent.parent / "data" / "sample_social_media.json"


def load_posts() -> list[dict]:
    if not DATA_FILE.exists():
        raise HTTPException(status_code=500, detail=f"Data file not found: {DATA_FILE}")
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def root():
    return {"status": "ok", "service": "net-sentinel-social-api"}


@app.get("/api/v1/posts", response_model=list[Post])
def get_posts(platform: Optional[str] = None, scenario: Optional[str] = None):
    raw = load_posts()

    if platform:
        raw = [p for p in raw if p.get("platform") == platform]
    if scenario:
        raw = [p for p in raw if p.get("scenario") == scenario]

    for p in raw:
        p.pop("scenario", None)

    return [Post(**p) for p in raw]


@app.get("/api/v1/posts/{post_id}", response_model=Post)
def get_post(post_id: str):
    raw = load_posts()

    match = next((p for p in raw if p.get("post_id") == post_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Post not found")

    match.pop("scenario", None)
    return Post(**match)


# Added for issues #13, #15 (network analysis + demographics).
# Import happens down here, not at the top of the file, so that network_router's
# `from backend import load_posts` finds load_posts already defined - putting
# this import earlier causes a circular-import crash.
from network_router import router as network_router
app.include_router(network_router)
