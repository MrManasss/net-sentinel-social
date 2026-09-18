# Build rules — NET-SENTINEL SOCIAL demo

Read `PROJECT_BRIEF.md` and `ARCHITECTURE.md` first. This file governs *how* to build, not
*what* to build.

## Non-negotiable honesty rules
This project got burned once already by a pitch deck that overclaimed (blockchain framed as
a real distributed ledger when the code was actually a hash-chain). Do not repeat that here.

1. **Never write code, comments, UI text, or docs that claim something is live/real when it's
   precomputed/synthetic/simulated.** If the dashboard shows "Telegram" as a data source,
   label it clearly as synthetic demo data, not a live feed.
2. **Never silently stub something and describe it as done.** If a feature is a heuristic
   standing in for a planned ML model (e.g. bot detection), say so in a code comment and in
   any user-facing text.
3. **No blockchain claims.** The integrity layer is a SHA-256 hash-chain. Call it that
   everywhere — code, comments, UI, README. If Hyperledger Fabric anchoring is mentioned
   anywhere, it must be clearly marked "planned / roadmap," never implemented as a stub that
   *looks* real.
4. **Numbers must be real or explicitly labeled.** Any stat shown in the dashboard must come
   from actual computation on the generated data — no hardcoded impressive-looking numbers.

## Build order (follow TASKS.md phases in order)
Do not start the dashboard before the data pipeline produces valid `demo_data.json`. Do not
add BERTopic, Neo4j, Postgres, or any other stretch-goal dependency until the core phases in
TASKS.md are done and tested.

## Code conventions
- Python: standard library + the specific packages named in ARCHITECTURE.md. Don't add new
  heavy dependencies without a clear reason — every new dependency is more that can break
  before the demo.
- One script, one job. `synthetic_data.py` generates data and does nothing else. `analyze.py`
  analyzes and does nothing else.
- Every pipeline script should be runnable standalone for debugging, and also callable from
  `build_demo_data.py`.
- Frontend: no build step. No npm, no bundler. CDN script tags only, per ARCHITECTURE.md.
- Write a docstring at the top of every file stating what it does and what it does NOT do
  (e.g. "does not call any external API").

## Testing expectations (lightweight — this is a demo, not production)
- `hash_chain.py` needs a real test that tampering with one entry breaks `verify_chain()`.
- `build_demo_data.py` should fail loudly (not silently produce partial output) if any stage
  errors.
- Manually verify `dashboard/index.html` opens directly via `file://` with no server running,
  OR document clearly if a local server is required (e.g. due to browser CORS on local JSON)
  and provide the exact one-line command to start it.

## Definition of done (per phase)
A phase is done when:
1. It runs standalone without errors on a clean checkout.
2. Its output matches the schema in ARCHITECTURE.md.
3. Nothing in its output or UI text overclaims per the honesty rules above.
4. It's been actually run at least once by the agent, not just written.

## When in doubt
Prefer the smaller, more reliable version of a feature over the more impressive but fragile
one. A judge sees a hash-chain badge that works. A judge does not see the Hyperledger Fabric
cluster that would have taken three extra days to stand up.
