# NET-SENTINEL SOCIAL — Demo Project Brief

## What this is
A demo build of NET-SENTINEL SOCIAL, the Social Media Analytics track of Team Net-Sentinel's
SIH 2026 submission (Problem Statement SIH26152, Theme: Blockchain & Cybersecurity).

This brief covers **the demo only** — a scaled-down, reliable proof-of-concept, not the full
production system described in the pitch deck. Where the two differ, this document wins.

## Why the demo is scoped differently from the pitch deck
The pitch deck describes the full target system (live multi-platform ingestion, Neo4j graph
DB, Hyperledger Fabric anchoring). Building that in a short window is not realistic, and a
live judged demo that depends on external APIs, a running graph database, or on-the-spot model
inference is a demo that can fail in front of judges. So:

- **No live API calls during the demo.** All data is synthetic, generated once ahead of time.
- **No external services to run.** No Postgres, no Neo4j, no blockchain network. SQLite +
  NetworkX + a from-scratch hash-chain cover the same ideas with zero infra risk.
- **No live model inference during the demo.** Sentiment/topic/network analysis runs once,
  offline, and the results are cached to JSON. The dashboard only ever reads cached data.

This is an intentional, honest simplification — not a shortcut we hide. The brief and every
doc below say explicitly what's real vs. simulated vs. roadmap, and the demo UI should too.

## Goal
Show, end-to-end, that the pipeline in the diagrams actually works:
`synthetic posts → unified schema → 4 analysis engines → hash-chained storage → dashboard → alert logic`

## In scope for the demo
This list now follows the **official SIH26152 problem brief's 5 required components (A–E)**,
not just the pitch deck — see "Cross-check against the official PS" below for why this changed.

- **(A) Data collection**: synthetic posts standing in for X and Telegram (the two Must-Have
  sources per the PS), plus Reddit/YouTube as secondary sources — priority matches the PS, not
  the deck's original emphasis
- Unified `Post` schema (see ARCHITECTURE.md)
- **(B) Sentiment**: **nuanced** emotion labels (not just positive/negative/neutral) — sarcasm,
  anxiety, excitement, supportive, against — run offline via a pretrained model, cached
- **(C) Demographic profiling**: infer aggregate, anonymized audience signals (language,
  likely region, rough age bracket, interest area) from bio text and posting patterns in the
  synthetic data — **this was missing from the first draft of this brief; it's a required
  component per the official PS, not optional**
- **(D) Trend detection**: identify, rank, and give a lightweight forward-looking signal on
  rising topics (not just retrospective frequency spikes) — see ARCHITECTURE.md for how this
  stays achievable without full forecasting infrastructure
- **(E) Link analysis & network topology**: NetworkX centrality over a synthetic interaction
  graph, PLUS a simple time-sliced view showing how a flagged topic/sentiment moved through
  the network over 2–3 time windows (not just a static end-state graph)
- Bot-campaign detection: heuristic rules (burst timing, near-duplicate text, synchronized
  posting) — a cybersecurity-relevant addition beyond the PS's core 5, matching the theme
- SHA-256 hash-chained audit log with a working `verify_chain()`
- Static dashboard (HTML/CSS/JS) reading precomputed JSON — no backend server required to demo
- Simple alert logic: threshold-based "Action Required?" flag, matching the User Flow Diagram

## Cross-check against the official PS (do this before building, not after)
Before treating the pitch deck as ground truth, we checked it against NTRO's actual SIH26152
problem brief. Two real mismatches were found and are now corrected above:
1. **Demographics (component C) was absent from the deck's build plan entirely**, despite
   being one of five required components and appearing in the team's own Use Case Diagram.
2. **Data source priority was inverted.** The PS marks X and Telegram as "Must-Have" and
   Reddit/YouTube as merely "Appreciable Additions." The deck leaned on Reddit/YouTube as core
   collectors while demoting X to a static offline dataset. For the demo (synthetic-only) this
   is fine functionally, but the synthetic data and UI must still visibly prioritize X and
   Telegram as the primary sources, not Reddit/YouTube, or the demo won't read as solving the
   actual brief.

## Explicitly out of scope for the demo (roadmap only — say so on the demo itself)
- Live Telegram/Reddit/YouTube/X ingestion
- Neo4j / any running graph database
- Hyperledger Fabric anchoring
- Production auth, RBAC, multi-user access
- Model fine-tuning or training of any kind

## Success criteria
1. `python generate_and_analyze.py` runs start to finish with no internet and no API keys,
   producing a single `demo_data.json`.
2. Opening `dashboard.html` in a browser shows: sentiment over time, trending topics, an
   influence-network graph, flagged bot clusters, and a hash-chain integrity indicator.
3. Every claim visible in the UI is true of the code behind it — nothing implies Neo4j,
   Fabric, or live data unless it's clearly labeled "planned."
4. A person unfamiliar with the code can run it and understand it inside 5 minutes.

## Constraints
- Minimal time budget — prioritize "fully working, honestly scoped" over "feature-complete."
- No paid APIs, no GPU assumed.
- Should run on a normal laptop with Python 3.11+ and no additional installed services.
