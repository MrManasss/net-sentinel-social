from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Engagement(BaseModel):
    likes: Optional[int] = None
    comments: Optional[int] = None
    shares: Optional[int] = None
    views: Optional[int] = None


class Author(BaseModel):
    display_name: str
    account_created_at: Optional[datetime] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    karma: Optional[int] = None


class Analysis(BaseModel):
    sentiment: Optional[str] = None
    sentiment_confidence: Optional[float] = None
    demographics: dict = Field(default_factory=dict)
    topics: list[str] = Field(default_factory=list)
    trend_score: Optional[float] = None
    network_features: dict = Field(default_factory=dict)


class Security(BaseModel):
    record_hash: Optional[str] = None
    previous_hash: Optional[str] = None
    audit_timestamp: Optional[datetime] = None


class Post(BaseModel):
    post_id: str
    platform: str
    source_id: str
    author_id: str
    text: str
    timestamp: datetime
    language: str
    hashtags: list[str] = Field(default_factory=list)
    reply_to: Optional[str] = None
    engagement: Engagement
    author: Author
    analysis: Analysis
    security: Security
