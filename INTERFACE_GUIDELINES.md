# NET-SENTINEL SOCIAL — Interface Guidelines

These guidelines govern `dashboard/index.html` and everything under `dashboard/`. They exist
so the interface actually demonstrates the 5 required PS components (see PROJECT_BRIEF.md),
not just whatever looked good to build. Read PROJECT_BRIEF.md and ARCHITECTURE.md first.

## 1. Structure follows the User Flow Diagram, literally
The pitch deck's User Flow Diagram is not just a pitch artifact — it's the actual information
architecture. The dashboard should read top to bottom as:

```
[ Header: platform name, hash-chain integrity badge ]
        ↓
[ Data Collection strip: which sources fed this data, X/Telegram visually first ]
        ↓
[ 4 analysis sections, one per PS component: Sentiment | Demographics | Trends | Network ]
        ↓
[ Security & Provenance panel: hash-chain status, audit log excerpt ]
        ↓
[ Action Required? indicator: clear Yes/No state, matching the flowchart's decision diamond ]
```

Don't reorganize this into a generic "analytics dashboard grid" — the judge is comparing what
they see against the diagrams you already showed them. Structural continuity matters.

## 2. One section per required component — never merge or drop one
Five sections are non-negotiable, each clearly labeled with what it is:
1. **Sentiment** — nuanced labels (supportive/against/anxious/excited/sarcastic/neutral),
   shown as a stacked area or line chart over the synthetic timeline
2. **Demographics** — aggregate breakdown only (age bracket / region / language), bar or donut
   charts, never a list of "individuals" — label this clearly as **aggregated, anonymized**
3. **Trends** — ranked list with a momentum indicator (↑ rising / → stable / ↓ falling), not
   just a word cloud
4. **Network** — the influence graph, with a way to see change over time (even a simple
   "before" / "after" toggle between two time windows is enough — doesn't need to be animated)
5. **Bot/Coordination flags** — a distinct panel, visually separated from the 4 above, since
   it's a cybersecurity capability beyond the PS's core ask, not a core analytics feature

If time runs out, cut polish before cutting a section. A rough demographics panel beats no
demographics panel — that's the one component that's easy to accidentally skip.

## 3. Data source honesty
Every chart/panel that implies live data must carry a small, unmissable label:
**"Synthetic demo data — not live"**. Put it once in the header, not buried in a footnote.
Platform tags on individual posts (small icons or text badges) should visually favor X and
Telegram over Reddit/YouTube, per the PS's Must-Have/Appreciable split — don't let the visual
hierarchy imply Reddit/YouTube are equally central.

## 4. Visual style
- **Layout**: single page, section-per-scroll or a simple tab/anchor nav — no multi-page
  routing, no build step (per ARCHITECTURE.md)
- **Color**: reuse the palette already established in the pitch deck's diagrams — blue for
  data/system elements, green for security/integrity, orange/amber for alerts — so the demo
  visually matches the pitch rather than introducing a new unrelated palette
- **Typography**: system font stack, no custom font loading (one less thing to break offline)
- **Density**: prioritize legibility on a projector — a judge six feet from a screen should be
  able to read section headers and chart labels without leaning in
- **Motion**: minimal. A hover tooltip is fine; auto-playing animations are not — they're one
  more thing that can look broken if the browser stutters mid-demo

## 5. The "Action Required?" indicator
This is the payoff moment from the User Flow Diagram — make it visually obvious, not a small
badge. Large, clearly colored (e.g. green "Continue Monitoring" vs. red/amber "Alert &
Notify"), with one line explaining *why* (e.g. "Coordinated posting spike detected in cluster
#3"). This is what ties all 5 analysis sections back to a concrete decision, which is the
actual point of the system per the PS's framing ("actionable audience insights").

## 6. Accessibility & resilience baseline (lightweight, not exhaustive)
- Every chart has a text-equivalent summary line nearby (e.g. "Sentiment: 62% supportive, up
  from 48% in the previous window") — protects against a chart library rendering glitch mid-demo
  and helps anyone who can't read the chart at a glance
- Color is never the only signal (pair color with an icon or label — e.g. rising/falling
  arrows, not just red/green)
- The page must degrade gracefully if `demo_data.json` is missing or malformed: show a clear
  "run `build_demo_data.py` first" message, never a blank white screen or raw console error

## 7. Definition of done for the interface
- All 5 required-component sections are present and populated from real computed values in
  `demo_data.json` — no hardcoded placeholder numbers left in by the time this is "done"
  (check against CLAUDE.md's honesty rules)
- The "synthetic data" label is visible without scrolling
- Opens correctly via `file://` or the documented local-server command, on a fresh checkout,
  with no console errors
- Someone who has only seen the pitch deck's diagrams should recognize the dashboard as "the
  same system" within a few seconds of looking at it
