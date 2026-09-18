# NET-SENTINEL SOCIAL

**AI-Driven Social Media Intelligence, Counter-Disinformation & Cryptographic Audit Framework**  
*Smart India Hackathon (SIH 2026) — Problem Statement SIH26152*  
*Theme: Blockchain & Cybersecurity | Organization: National Technical Research Organisation (NTRO)*  
*Demo Prototype Version: 5.0 (Offline Proof-of-Concept)*

---

## 🛡️ Executive Summary

**NET-SENTINEL SOCIAL** is an analyst-oriented social media intelligence operations suite engineered for high-reliability, zero-infrastructure demonstration. It transforms multi-platform social streams into actionable intelligence across five mission-critical analytical pillars, fortified by a cryptographic **SHA-256 tamper-evident linked audit trail**.

```
  SYNTHETIC SOCIAL FEEDS (X & Telegram Prioritized)
                         ↓
             DATA NORMALIZATION ENGINE
                         ↓
  ┌──────────────┬──────────────┬──────────────┐
  ↓              ↓              ↓              ↓
SENTIMENT      TRENDS     DEMOGRAPHICS      NETWORK
(6 Classes)   (Momentum)   (Anonymized)   (Centrality)
  └──────────────┴──────────────┴──────────────┘
                         ↓
            COORDINATION DETECTION ENGINE
                         ↓
                UNIFIED DASHBOARD
                         ↓
             ACTION REQUIRED? (Alert)
                         ↓
           CAMPAIGN INVESTIGATION (CAM-0017)
                         ↓
         CRYPTOGRAPHIC INTEGRITY VERIFICATION
                         ↓
            INTELLIGENCE DOSSIER EXPORT
```

---

## ⚡ Quick Start (Ready in 10 Seconds)

The entire project runs **100% offline with zero external databases, zero paid APIs, and zero npm/bundler dependencies**.

### Step 1: Install Minimal Python Dependency
```bash
pip install -r requirements.txt
```
*(Only requires `networkx>=3.0`)*

### Step 2: Generate Precomputed Intelligence Dataset
```bash
python pipeline/build_demo_data.py
```
*Runs synthetic generation, runs all 5 analysis engines, constructs the SHA-256 linked hash-chain, validates integrity, and emits `demo_data.json` and `dashboard/data.js`.*

### Step 3: Launch the Command Center
Simply **double-click** `dashboard/index.html` to open it in your browser!  
*(Direct `file:///` viewing is fully supported via pre-bundled local data and offline libraries).*

Alternatively, start a local HTTP server:
```bash
python -m http.server 8000
```
Then navigate to: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)

---

## 🎯 Verification Against Official PS Requirements (Components A–E)

| PS Component | Requirement | Implementation in NET-SENTINEL SOCIAL |
|---|---|---|
| **(A) Data Ingestion** | Multi-platform ingestion with X & Telegram prioritized | 220 synthetic posts: **X (61.8%)** and **Telegram (25.5%)** form 87.3% of volume; Reddit (7.7%) & YouTube (5.0%) as secondary. Includes English, Hindi, and Hinglish code-mixed posts. |
| **(B) Sentiment Analysis** | Nuanced emotion labels (not just positive/negative) | 6-class taxonomy: `Supportive`, `Against`, `Anxious`, `Excited`, `Sarcastic`, `Neutral` with confidence scores and temporal distribution. |
| **(C) Demographic Profiling** | Aggregate audience signals | Anonymized age brackets (`13-17`, `18-24`, `25-34`, `35-44`, `45+`), top geographic regions (Delhi NCR, Karnataka, etc.), languages, and interest segments. *Strictly anonymized.* |
| **(D) Trend Detection** | Forward-looking rising topics | Frequency tracking across time windows (T1 → T2 → T3) with mathematical momentum calculation: `↑ Rising`, `→ Stable`, `↓ Falling`. `#CyberSurakshaBill` surges to `↑ Rising`. |
| **(E) Link Analysis** | Network topology and time-sliced diffusion | NetworkX degree and betweenness centrality. Interactive canvas with **Baseline (Before)** vs **Campaign Injected (After)** toggle showing bot cluster insertion. |
| **Cybersecurity Layer** | Coordinated Bot Campaign Detection | Multi-signal correlation engine flagging Campaign **CAM-0017** with 75%+ confidence based on text similarity (94%), temporal burst sync (91%), hashtag bundles (88%), and graph reciprocity (84%). |
| **Integrity Layer** | Tamper-evident ledger & provenance | Cryptographic SHA-256 linked chain (`entry_hash = SHA256(index + timestamp + data_hash + prev_hash)`). Includes an **Interactive Tamper Simulation Lab** that proves instantaneous mathematical tamper detection. |
| **Decision & Reporting** | Actionable intelligence & evidence handling | High-visibility **"Action Required?"** decision banner, slide-over **Campaign Investigation Drawer**, and one-click **Printable Intelligence Dossier Export**. |

---

## ⏱️ 5-Minute Evaluator Demonstration Script

Follow this sequence during the live presentation for maximum impact:

1. **Minute 1 — Access & Situational Awareness**
   - Show the **Visual Login Screen**: Select the *Social Media Analyst* role and click **"Access Command Dashboard as Analyst"**.
   - Point out the **Data Honesty Badge** in the header (*"Synthetic demo data — not live"*).
   - Review the **Multi-Platform Stream**: Emphasize that X and Telegram represent 87.3% of ingested posts, strictly adhering to the PS priority.

2. **Minute 2 — Nuanced Sentiment & Demographic Profiling**
   - Scroll to **Panel B (Sentiment)**: Show the 6 nuanced classes (`Supportive`, `Anxious`, `Sarcastic`, etc.) and the timeline chart showing anxiety rising in T2 and supportive sentiment surging in T3.
   - Scroll to **Panel C (Demographics)**: Point to the aggregate age and regional distribution, highlighting the prominent privacy disclaimer.

3. **Minute 3 — Emerging Trends & Network Topology**
   - Scroll to **Panel D (Trends)**: Show `#CyberSurakshaBill` leading in the **↑ RISING** momentum state with positive velocity.
   - Scroll to **Panel E (Network)**: Click between **"Baseline (Before)"** and **"Campaign Injected (After)"**. Show how the organic network transforms as the dense, red cluster of 18 bot accounts injects itself into the discourse.

4. **Minute 4 — Decision Diamond & Forensic Campaign Investigation**
   - Highlight the **"Action Required?" Alert Banner**: Show the high-severity decision and the multi-signal breakdown meters.
   - Click **`[ 🔍 Investigate Campaign CAM-0017 ]`**:
     - Inspect the **4 Detection Indicators** (Text: 94%, Temporal: 91%, Hashtag: 88%, Reciprocity: 84%).
     - Review the **Synchronized Evidence Posts** (near-duplicate messages posted in tight ~24s intervals).
     - Inspect the **Identified Accounts** ledger (18 batch-created bot accounts).

5. **Minute 5 — Cryptographic Tamper Test & Report Generation**
   - Scroll to **Panel F-10 (Cryptographic Evidence Integrity)**:
     - Notice the green badge: `✓ SHA-256 CHAIN VALID (220 BLOCKS)`.
     - Click **`[ ⚠ Simulate Data Tampering in Block #5 ]`**:
     - **Watch the system react dynamically**: The badge flips to flashing red `⚠ TAMPER DETECTED: BLOCK #5`, a critical security alert appears, and Block #5 is highlighted in red with cryptographic mismatch details!
     - Click **`[ ↺ Restore Chain Integrity ]`**: Show the chain immediately return to green `✓ VALID`.
   - Click **`[ 📄 Export Intelligence Dossier ]`** in the top navigation bar:
     - Show the printable intelligence report dossier ready for law enforcement / command review.

---

## 📁 Repository Directory Structure

```
net-sentinel-social-demo/
├── requirements.txt            # Minimal Python dependencies (networkx)
├── README.md                   # System documentation & evaluation guide
├── demo_data.json              # Precomputed consolidated intelligence dataset
├── pipeline/
│   ├── __init__.py
│   ├── synthetic_data.py       # Multi-platform post & graph generator (T1, T2, T3)
│   ├── analyze.py              # 5 AI intelligence analysis engines + bot detector
│   ├── hash_chain.py           # SHA-256 linked chain & automated tamper unit tests
│   └── build_demo_data.py      # Master orchestrator producing demo_data.json & data.js
└── dashboard/
    ├── index.html              # Single-page analyst operations console
    ├── style.css               # SOC dark-mode intelligence theme
    ├── app.js                  # Dynamic dashboard logic & cryptographic verifier
    ├── data.js                 # Zero-CORS precomputed data bundle for file:/// support
    ├── demo_data.json          # Local JSON copy
    └── libs/
        ├── chart.umd.min.js    # Chart.js (Bundled for 100% offline execution)
        └── vis-network.min.js  # vis-network (Bundled for 100% offline execution)
```

---

## 🔒 Non-Negotiable Data Honesty & Ethics

In strict compliance with project guidelines and academic honesty:
- **Synthetic Data Only:** All handles, accounts, posts, and interaction edges are synthetic constructs for SIH26152 demonstration. No live citizen data is ingested.
- **SHA-256 Hash Chain vs Blockchain:** The demo integrity layer is an authentic Python/JS SHA-256 linked hash chain. Enterprise blockchain anchoring (Hyperledger Fabric) is accurately represented as roadmap architecture.
- **Probabilistic Assessment:** The system surfaces *potential coordinated activity* with confidence scores; it does not claim definitive criminal intent or individual culpability.
