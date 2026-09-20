# Net-Sentinel Social — Common Data Schema

## Purpose

This document defines the normalized data format used across Net-Sentinel Social.

Data collected from Telegram, Reddit, YouTube, and public X datasets should be converted into this common format before being passed to storage and analysis modules.

The schema is designed to support:

- Sentiment analysis
- Demographic profiling
- Trend detection
- Network analysis
- Coordinated campaign and suspicious activity detection
- Dashboard visualization
- Secure audit logging

## Normalized Post Schema

```json
{
  "post_id": "string",
  "platform": "telegram|reddit|youtube|x",
  "source_id": "string",
  "author_id": "string",
  "text": "string",
  "timestamp": "ISO-8601 UTC datetime",
  "language": "string",
  "hashtags": [],
  "reply_to": null,

  "engagement": {
    "likes": 0,
    "comments": 0,
    "shares": 0,
    "views": 0
  },

  "author": {
    "display_name": "string",
    "account_created_at": null,
    "followers": null,
    "following": null
  },

  "analysis": {
    "sentiment": null,
    "sentiment_confidence": null,
    "demographics": {},
    "topics": [],
    "trend_score": null,
    "network_features": {}
  },

  "security": {
    "record_hash": null,
    "previous_hash": null,
    "audit_timestamp": null
  }
}
