# NET-SENTINEL SOCIAL — Demo Architecture

## Design principle
Precompute everything, serve statically. Two phases, run once and read forever:

```
Phase A (offline, run once):
  synthetic_data.py → raw posts + interaction graph
        ↓
  analyze.py → sentiment + trends + network + bot flags
        ↓
  hash_chain.py → tamper-evident log of ingestion events
        ↓
  demo_data.json  (everything the dashboard needs, precomputed)

Phase B (demo time):
  dashboard.html/js  ← reads demo_data.json only, no server, no network
```

## Tech stack (pinned to what's actually needed — nothing heavier)
- **Language:** Python 3.11+
- **Synthetic data:** `Faker` for names/handles/timestamps; small hand-written templates for
  post text (Hindi-English code-mixed included, to match the deck's stated differentiator)
- **Sentiment:** `transformers` pipeline with a pretrained multilingual model
  (e.g. `cardiffnlp/twitter-xlm-roberta-base-sentiment`) — real inference, run once, cached
- **Trend detection:** simple time-bucketed keyword/hashtag frequency + spike detection
  (BERTopic is a stretch goal — see TASKS.md; don't block the demo on it)
- **Network analysis:** `NetworkX` — degree/betweenness centrality on a synthetic
  follow/reply/retweet graph
- **Bot detection:** heuristic, no ML: posting-frequency bursts, near-duplicate text
  (simple string similarity), synchronized timestamps across accounts
- **Integrity:** hand-written SHA-256 linked hash-chain (`hashlib`), with a `verify_chain()`
  function that actually checks the chain — same honest pattern as the criminal-network project
- **Storage:** a single SQLite file (optional — JSON is enough for the demo; use SQLite only
  if it's genuinely easier for you, not because the deck says Postgres)
- **Frontend:** plain HTML5/CSS3/Vanilla JS + Chart.js (via CDN) for charts, a small
  force-directed graph (e.g. `vis-network` via CDN) for the influence graph — no build step,
  no npm, one file opens in a browser

## Data schema

### Unified Post object
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

### Analysis output (attached per post, or in a separate keyed table)
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
Note the sentiment label set matches the PS's explicit examples (sarcasm, anxiety, excitement,
supportive, against) rather than a flat positive/negative/neutral scale — a plain 3-way
sentiment model can be adapted to this by mapping model output + simple heuristics (e.g.
question-mark density, negation patterns) onto the richer label set. Don't claim more nuance
than the underlying model actually produces — label the mapping as heuristic-assisted in code
comments.

### Demographic profile (aggregated, anonymized — never per-individual in the UI)
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
Inferred from synthetic bio text, posting language, and behavioral patterns — grouped into
segments, never presented as a claim about a specific named individual.

### Trend entry (adds a lightweight forward-looking signal, not just a frequency count)
```json
{
  "topic": "string",
  "time_window": "ISO8601 bucket",
  "mention_count": 0,
  "rank": 1,
  "momentum": "rising | falling | stable"
}
```
`momentum` is computed by comparing mention_count across the last 2-3 time windows — simple
slope, not a trained forecasting model. This is enough to honestly say "identify, rank, and
signal what's rising" without overclaiming a predictive model that isn't there. BERTopic-based
forecasting (the deck's original stretch goal) can replace this later without changing the
schema.

### Hash-chain entry
```json
{
  "index": 0,
  "timestamp": "ISO8601",
  "post_id": "string",
  "data_hash": "sha256 of the post payload",
  "prev_hash": "sha256 of the previous entry",
  "entry_hash": "sha256 of (index+timestamp+data_hash+prev_hash)"
}
```

## Folder structure
```
net-sentinel-social-demo/
├── CLAUDE.md                  # rules for the coding agent
├── PROJECT_BRIEF.md
├── ARCHITECTURE.md
├── TASKS.md
├── pipeline/
│   ├── synthetic_data.py      # generates posts + interaction graph
│   ├── analyze.py             # sentiment + trends + network + bot detection
│   ├── hash_chain.py          # SHA-256 linked chain + verify_chain()
│   └── build_demo_data.py     # orchestrates the above → demo_data.json
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── app.js                 # reads demo_data.json, renders charts/graph
├── demo_data.json             # generated, not hand-written
└── README.md                  # "run this one command" instructions
```

## What the dashboard must visually communicate
Mirrors the User Flow Diagram: Data Collection → AI Engines → Storage → Unified Dashboard →
Action Required? → Alert/Continue. The dashboard should show, at minimum, one section per
required PS component plus the security layer:
- **(B)** A sentiment-over-time chart using the nuanced label set, not just pos/neg/neutral
- **(C)** A demographics panel (age bracket / region / language breakdown) — aggregated only
- **(D)** A trending-topics list showing rank + momentum (rising/falling/stable)
- **(E)** An influence-network graph (nodes = accounts, sized by centrality) with a simple
  time-slider or before/after view showing how a topic/sentiment moved through the network
- A flagged bot-cluster panel (cybersecurity addition, beyond the PS's core 5)
- A hash-chain integrity badge (green if `verify_chain()` passes)
- A simple "Action Required?" indicator driven by a threshold rule

Data source labels in the UI (e.g. small platform icons/tags on posts) should visibly lead
with X and Telegram, matching the PS's Must-Have priority — even though all data here is
synthetic, don't let Reddit/YouTube visually dominate the story.
