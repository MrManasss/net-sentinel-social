# Net-Sentinel Social — Common Data Schema

## Purpose

This document defines the common data format used across Net-Sentinel Social modules.

All data ingestion sources should be normalized into this format before being passed to other modules.

## Post Schema

```json
{
  "post_id": "string",
  "platform": "string",
  "author_id": "string",
  "text": "string",
  "timestamp": "ISO-8601 UTC datetime",
  "language": "string",
  "hashtags": [],
  "reply_to": null
}
