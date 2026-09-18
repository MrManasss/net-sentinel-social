# NET-SENTINEL SOCIAL — System Architecture

## Overview

Net-Sentinel Social follows a two-phase architecture: an offline data processing pipeline that generates the intelligence dataset, and a static dashboard that visualizes the results. This separation keeps the demo reliable while demonstrating the full analytical workflow.

```
Phase 1 — Data Processing (Offline):
  synthetic_data.py → raw posts + interaction graph
        ↓
  analyze.py → sentiment + trends + demographics + network + bot flags
        ↓
  hash_chain.py → tamper-evident audit log
        ↓
  demo_data.json  (consolidated intelligence dataset)

Phase 2 — Visualization (Dashboard):
  index.html + app.js  ← reads demo_data.json, renders all panels
```

## Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.11+ | Core pipeline |
| Data Generation | Custom templates + Faker patterns | Hindi-English code-mixed synthetic posts |
| Sentiment Analysis | Indic BERT / XLM-R based classification | 6-class nuanced emotion labeling |
| Trend Detection | Time-bucketed frequency + momentum calculation | Rising/Stable/Falling signal detection |
| Network Analysis | NetworkX | Degree and betweenness centrality on interaction graphs |
| Bot Detection | Multi-signal heuristic correlation | Burst timing, text similarity, synchronized posting |
| Integrity | SHA-256 linked hash chain (hashlib) | Tamper-evident audit trail |
| Frontend | HTML5 / CSS3 / Vanilla JS | Single-page analyst dashboard |
| Charting | Chart.js (bundled) | Sentiment, demographics, and trend charts |
| Graph Visualization | vis-network (bundled) | Interactive network topology canvas |

## Data Schemas

### Post Object
```json
{
  "id": "string",
  "platform": "telegram | reddit | youtube | x | instagram",
  "author_handle": "string",
  "text": "string",
  "language": "en | hi | hi-en-mixed",
  "timestamp": "ISO8601",
  "reply_to_id": "string | null",
  "engagement": {"likes": 0, "shares": 0, "replies": 0}
}
```

### Sentiment Analysis Output
```json
{
  "post_id": "string",
  "sentiment_label": "supportive | against | anxious | excited | sarcastic | neutral",
  "sentiment_score": 0.0,
  "topics": ["string"],
  "is_flagged_bot_cluster": false,
  "bot_cluster_id": "string | null"
}
```

### Demographic Profile (Aggregated)
```json
{
  "segment_id": "string",
  "estimated_age_bracket": "13-17 | 18-24 | 25-34 | 35-44 | 45+",
  "estimated_region": "string",
  "language": "en | hi | hi-en-mixed",
  "interest_tags": ["string"],
  "post_count": 0
}
```

### Trend Entry
```json
{
  "topic": "string",
  "time_window": "ISO8601 bucket",
  "mention_count": 0,
  "rank": 1,
  "momentum": "rising | falling | stable"
}
```

### Hash Chain Entry
```json
{
  "index": 0,
  "timestamp": "ISO8601",
  "post_id": "string",
  "data_hash": "SHA-256 hash of the post payload",
  "prev_hash": "SHA-256 hash of the previous entry",
  "entry_hash": "SHA-256 of (index + timestamp + data_hash + prev_hash)"
}
```

## Dashboard Sections

The dashboard follows the main workflow from data ingestion to actionable intelligence:

1. **Data Collection Strip** — Source breakdown showing platform distribution (X and Telegram prioritized)
2. **Sentiment Panel** — Nuanced 6-class emotion labels with temporal distribution chart
3. **Demographics Panel** — Aggregated, anonymized audience segmentation (age, region, language)
4. **Trends Panel** — Ranked topic list with momentum indicators (↑ Rising / → Stable / ↓ Falling)
5. **Network Panel** — Interactive influence graph with Baseline vs Campaign Injected toggle
6. **Bot/Coordination Panel** — Flagged campaign details with multi-signal confidence breakdown
7. **Security Panel** — SHA-256 chain integrity badge with tamper simulation capability
8. **Action Required Indicator** — Decision-level alert based on detection thresholds

## Production Roadmap

The current prototype demonstrates the core analytical pipeline. The production system architecture includes:

- **Live API Integration:** PRAW (Reddit), YouTube Data API, Telegram Bot API, X API v2
- **Graph Database:** Neo4j for persistent network topology storage
- **Backend API:** FastAPI with PostgreSQL for production data management
- **Frontend:** React-based dashboard with real-time updates
- **Blockchain Anchoring:** Hyperledger Fabric for distributed audit trail verification
- **Advanced NLP:** Fine-tuned Indic BERT for improved Hindi-English code-mixed sentiment
- **Topic Modeling:** BERTopic for automated trend clustering and forecasting
