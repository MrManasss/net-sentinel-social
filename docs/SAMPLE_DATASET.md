# Sample Social Media Dataset

## Overview

This file documents `data/sample_social_media.json` — a synthetic dataset of 30 records used to test the Net-Sentinel Social pipeline. All records follow the normalized schema defined in `docs/DATA_SCHEMA.md`.

Records span 4 platforms: Reddit, X, Telegram, and YouTube. All timestamps are ISO-8601 UTC. All `analysis` and `security` fields are null — they are populated by the pipeline, not pre-filled.

---

## Scenarios

| Scenario | Records | Purpose |
|----------|---------|---------|
| SCEN-A | 5 | Organic baseline — multi-platform, clean sentiment |
| SCEN-B | 4 | Hindi-English variety — negative, mixed, ambiguous |
| SCEN-C | 8 | Coordinated bot cluster — 89s burst, X + Telegram |
| SCEN-D | 4 | Emerging trend — #GridFailure spike over 3 hours |
| SCEN-E | 5 | Reply chain — 3 levels deep, branching, repeated author |
| SCEN-F | 4 | Sarcasm and ambiguous sentiment |

The `scenario` field is a test annotation. The ingestion layer must strip it before inserting into PostgreSQL and before hashing.

---

## Platform-Specific Engagement Rules

| Platform | likes | comments | shares | views | followers | following | karma |
|----------|-------|----------|--------|-------|-----------|-----------|-------|
| Reddit | ✅ | ✅ | 0 | 0 | null | null | ✅ |
| X | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | null |
| Telegram | 0 | 0 | ✅ | ✅ | null | null | null |
| YouTube (comment) | ✅ | 0 | 0 | 0 | null | null | null |

---

## Reply Graph (SCEN-E)

post_0022 (data_corrector) is the root.
It is replied to by post_0023 (telecom_insider).
post_0023 is replied to by post_0024 (data_corrector) — same author reappears.
post_0024 has two replies: post_0025 (passerby_viewer) and post_0026 (solar_homeowner_jhk).

---

## Bot Cluster (SCEN-C)

8 posts between 14:00:00 and 14:01:29 UTC — an 89 second burst across X and Telegram. All accounts created in 2025-2026 with under 100 followers and near-identical text.
