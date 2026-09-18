# NET-SENTINEL SOCIAL

**AI-Powered Social Media Intelligence Platform**  
Real-time sentiment, trend, demographic, and network analysis with coordinated campaign detection.

---

**Smart India Hackathon 2026**  
Problem Statement ID: **SIH26152**  
Problem Statement Title: **Social Media Analytics**  
Theme: **Blockchain & Cybersecurity**  
PS Category: **Software**  
Organization: **National Technical Research Organisation (NTRO)**  
Team Name: **Net-Sentinel**

---

## About

Net-Sentinel Social is an AI-driven social media intelligence and counter-disinformation framework. It collects data from multiple social media platforms (Telegram, Reddit, YouTube, X), processes it through four parallel AI analysis engines, and presents unified intelligence through an analyst-grade dashboard — all backed by a SHA-256 cryptographic audit trail for tamper-evident data integrity.

The system addresses the growing challenge of fragmented social media analytics tools by combining sentiment analysis, demographic profiling, trend forecasting, network topology mapping, and coordinated campaign detection into a single cohesive platform.

---

## Understanding the Problem

- **Fragmented tools:** Most platforms offer single-purpose sentiment-only or trend-only analysis.
- **No visibility layer:** Bot and coordinated campaign activity can go undetected, making results unreliable.
- **Language gaps:** Bilingual and code-mixed Hindi-English content is poorly handled by existing tools.
- **Stale reporting:** Periodic batch reports miss fast-moving narratives and coordinated attacks.

## Our Solution

An AI-driven analytics intelligence platform that combines:
- **Sentiment + Demographics + Trend + Network Analysis** in a single pipeline
- Continuous ingestion from **Telegram, Reddit, YouTube, and X**
- Four parallel AI analysis engines for real-time processing
- A unified dashboard for cross-platform intelligence
- **Coordinated Campaign Detection** for identifying bot networks and amplified voices
- **SHA-256 cryptographic audit logs** for data integrity and evidence handling

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Timeline Analysis** | Multi-platform data ingestion with temporal event clustering |
| **Sentiment Analysis** | 6-class nuanced taxonomy (Supportive, Against, Anxious, Excited, Sarcastic, Neutral) using Indic BERT / XLM-R |
| **Demographic Profiling** | Aggregated, anonymized audience segmentation by age, region, language, and interests |
| **Trend Detection** | Keyword/hashtag frequency tracking with momentum signals (Rising / Stable / Falling) using BERTopic |
| **Network Analysis** | Graph-based influence mapping with degree and betweenness centrality via NetworkX |
| **Campaign Detection** | Multi-signal correlation engine for identifying coordinated bot clusters |
| **Integrity Verification** | SHA-256 linked hash-chain with interactive tamper simulation |

---

## Unique Selling Points (USPs)

- **Coordinated Campaign Detection** — Multi-signal correlation (text similarity, temporal bursts, hashtag bundles, graph reciprocity) to flag bot networks
- **Trend Forecasting** — Forward-looking momentum signals, not just retrospective frequency counts
- **Hindi-English & Sarcasm Aware AI** — Handles code-mixed bilingual content and detects sarcasm in social posts
- **Tamper-Evident Audit Trail** — Cryptographic SHA-256 chain for evidence-grade data provenance

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Data Collection** | Isolation + PRAW + YouTube API + Kaggle datasets |
| **AI/ML** | Indic BERT / XLM-R + BERTopic + NetworkX / Neo4j |
| **Backend & UI** | FastAPI + PostgreSQL + React |
| **Security** | SHA-256 Hash Chain + Hyperledger Fabric |

### Development & Validation Flow

```
Synthetic Data → Pipeline Testing → Live Data Integration
       ↓                ↓                    ↓
  Indic BERT       BERTopic           NetworkX / Neo4j
       ↓                ↓                    ↓
  Backend & UI    Pipeline Testing     Live Data Testing
       ↓                ↓                    ↓
             Security & Integrity Layer
```

---

## Project Structure

```
net-sentinel-social/
├── README.md                   # Project documentation
├── ARCHITECTURE.md             # System architecture and data schemas
├── requirements.txt            # Python dependencies
├── demo_data.json              # Precomputed intelligence dataset
├── pipeline/
│   ├── __init__.py
│   ├── synthetic_data.py       # Multi-platform post generator (X, Telegram, Reddit, YouTube)
│   ├── analyze.py              # AI analysis engines (sentiment, trends, demographics, network, bot detection)
│   ├── hash_chain.py           # SHA-256 linked chain with verification
│   └── build_demo_data.py      # Orchestrator script for generating demo_data.json
└── dashboard/
    ├── index.html              # Analyst operations dashboard
    ├── style.css               # Dashboard styling
    ├── app.js                  # Dashboard logic and cryptographic verifier
    ├── data.js                 # Precomputed data bundle
    ├── demo_data.json          # Local data copy
    └── libs/
        ├── chart.umd.min.js    # Chart.js (bundled for offline use)
        └── vis-network.min.js  # vis-network (bundled for offline use)
```

---

## Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Step 1: Clone the repository
```bash
git clone https://github.com/MrManasss/net-sentinel-social.git
cd net-sentinel-social
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Generate the intelligence dataset
```bash
python pipeline/build_demo_data.py
```
This runs the full pipeline — synthetic data generation, all five analysis engines, SHA-256 hash chain construction, and outputs `demo_data.json` along with `dashboard/data.js`.

### Step 4: Launch the dashboard
Simply open `dashboard/index.html` in your browser.

Or start a local server:
```bash
python -m http.server 8000
```
Then visit: [http://localhost:8000/dashboard/](http://localhost:8000/dashboard/)

---

## Dashboard Walkthrough

1. **Data Ingestion Overview** — See multi-platform data from X (61.8%), Telegram (25.5%), Reddit (7.7%), and YouTube (5.0%)
2. **Sentiment Analysis** — Six nuanced emotion classes with temporal distribution charts
3. **Demographic Profiling** — Aggregated age brackets, geographic regions, language distribution (strictly anonymized)
4. **Trend Detection** — Keyword/hashtag tracking with momentum indicators (Rising ↑, Stable →, Falling ↓)
5. **Network Topology** — Interactive force-directed graph with Baseline vs Campaign Injected toggle
6. **Campaign Investigation** — Multi-signal detection breakdown (Text: 94%, Temporal: 91%, Hashtag: 88%, Reciprocity: 84%)
7. **Cryptographic Integrity** — SHA-256 chain validation with interactive tamper simulation lab
8. **Intelligence Dossier** — One-click export of printable intelligence report

---

## Feasibility

- **Available Data Sources:** Telegram, Reddit, and YouTube provide accessible sources through their public APIs
- **Existing AI Models:** Indic BERT, BERTopic, and network-analysis methods are readily available, reducing the need to build models from scratch
- **Modular Architecture:** Individual data sources and analysis modules can be added or replaced without redesigning the entire system
- **Low-Cost Prototype:** Open-source tools and free-tier data sources allow the core system to be developed and demonstrated at low cost

---

## Research References

- Pacheco et al., **ICWSM 2021** — *Coordinated link-sharing and information cascades*
- **ACM Web Conf. 2022** — *Blogosphere: A cross-platform campaign analysis*
- Aggarwal et al., **arXiv:2010.00118** — *Hindi-English code-mixed sentiment detection*
- Groeneveld, **arXiv:2301.06751** — *Topic modelling for trend detection*
- **IEEE**, *Opinion Leaders in Social Networks* — *Community detection methods*
- Ku, Bhagwat & Mazov, **SentimentCall (Kaggle)** — *Large-scale Twitter sentiment dataset*

---

## Impact

### Target Audience
| Audience | Benefit |
|----------|---------|
| **Analysts & Investigators** | Faster campaign identification via multi-signal correlation |
| **Content Creators** | Identify audience engagement patterns beyond amplified voices |
| **Viewers / Public** | Clearer picture of public sentiment beyond manipulated narratives |

### Benefits
- **Security:** Early detection of bot-driven and coordinated disinformation campaigns
- **Social:** A clearer picture of public sentiment beyond amplified voices
- **Economic:** Reduces duplicated and time-consuming manual OSINT work

---

## License

This project was developed as part of the Smart India Hackathon 2026 (Problem Statement SIH26152).

---

## Team

**Team Net-Sentinel**  
Smart India Hackathon 2026
