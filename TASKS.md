# Build plan — NET-SENTINEL SOCIAL demo

Work through phases in order. Each phase has a "done when" check — don't move on until it
passes. This list is intentionally lean given a tight time budget; stretch goals are marked.

## Phase 0 — Scaffold
- Create the folder structure from ARCHITECTURE.md
- Set up a virtualenv, `requirements.txt` with only what's needed for Phase 1–2
- **Done when:** `python -m venv .venv && pip install -r requirements.txt` works clean

## Phase 1 — Synthetic data generator
- `synthetic_data.py`: generate ~150–300 synthetic posts, **weighted toward X and Telegram**
  as the primary platforms (per the official PS's Must-Have priority), with Reddit/YouTube as
  a smaller share — some in Hindi-English code-mixed text, with realistic timestamps clustered
  around 2–3 "events" (so trend/sentiment spikes are visible)
- Include varied author bio text and posting patterns so demographic inference (Phase 2) has
  real signal to work with — not just random noise
- Also generate a synthetic interaction graph (who replies to / retweets whom) — this feeds
  both network analysis and bot detection
- Include at least one deliberately obvious "coordinated bot cluster" (near-identical text,
  synchronized timestamps) so the bot-detection feature has something real to catch
- **Done when:** running the script produces valid `Post` objects matching the schema, saved
  to a raw JSON file, with the planted bot cluster visibly present in the data, and X/Telegram
  visibly the majority platforms

## Phase 2 — Analysis engines (one sub-phase per required PS component)
- **(B) Sentiment**: load a pretrained multilingual sentiment model, run inference, then map
  output onto the nuanced label set from ARCHITECTURE.md (supportive/against/anxious/
  excited/sarcastic/neutral) using the model's raw output plus simple heuristics; cache scores
- **(C) Demographics**: infer aggregate segments from synthetic bio text and posting patterns
  per the schema in ARCHITECTURE.md — this is a required component, don't skip it
- **(D) Trends**: bucket posts by time window, rank top keywords/hashtags per bucket, compute
  a simple rising/falling/stable momentum signal across windows
- **(E) Network**: run NetworkX centrality measures on the interaction graph; capture at least
  two time-window snapshots so the dashboard can show change over time, not just an end state
- Bot detection: implement the heuristic rules from ARCHITECTURE.md; confirm it actually
  flags the planted cluster from Phase 1
- **Done when:** each analysis function runs standalone on the Phase 1 output and produces
  output matching its schema in ARCHITECTURE.md; the planted bot cluster is correctly flagged;
  all 5 PS components have real, non-empty output

## Phase 3 — Hash-chain integrity layer
- `hash_chain.py`: build the linked-hash-chain over ingestion events, implement
  `verify_chain()`
- Write the tamper test described in CLAUDE.md (mutate one entry, confirm verify fails)
- **Done when:** the tamper test passes and is easy to re-run

## Phase 4 — Assemble demo_data.json
- `build_demo_data.py`: orchestrate Phases 1–3 into one script, output the final
  `demo_data.json` the dashboard will read
- **Done when:** one command, no arguments, produces a complete, schema-valid
  `demo_data.json` with no errors

## Phase 5 — Dashboard
- Static HTML/CSS/JS reading `demo_data.json`
- Follow `INTERFACE_GUIDELINES.md` exactly — section order, the 5 required-component panels,
  data-source honesty labeling, and the "Action Required?" indicator are all specified there
- **Done when:** opening the dashboard (via `file://` or the documented local server command)
  shows real data from `demo_data.json` in every one of the 5 required sections plus the
  bot-flag and security panels, no console errors, and it passes the definition-of-done
  checklist at the end of INTERFACE_GUIDELINES.md

## Phase 6 — Polish & README
- Write `README.md`: one clear command (or two, if a local server is genuinely required) to
  regenerate data and view the dashboard
- Pass over every UI label and code comment against the honesty rules in CLAUDE.md
- **Done when:** someone who has never seen the project can clone it and get the dashboard
  running by only reading the README

## Stretch goals (only after Phase 6 is solid)
- Swap keyword-frequency trend detection for real BERTopic
- Add a toggle to pull a small amount of real, live Reddit data (PRAW, public read-only,
  no auth needed for public subreddits) as an optional "this can use real data too" moment
- SQLite instead of flat JSON for the assembled dataset
