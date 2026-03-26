# K-SIP — Kenya Strategic Intelligence Platform

> A portfolio-grade business intelligence platform built to demonstrate strategic analytics, competitive intelligence, and AI-powered decision support for East African fintech leadership roles.

---

## Overview

K-SIP is a multi-module Streamlit application that simulates the intelligence system a Business Intelligence Manager would build at a PAYG solar/fintech company operating in Kenya. It was developed as a flagship portfolio project targeting senior BI and strategy roles in EA fintech.

The platform covers all four pillars of strategic BI:

| Module | Pillar | What it does |
|---|---|---|
| Early Warning System | Strategic intelligence | EA fintech risk index, macro signals, regulatory event tracker |
| Competitive War Room | Competitive intelligence | Competitor profiles, scenario war-gaming, whitespace map |
| Customer Intelligence | Customer & commercial strategy | Segment economics, LTV/CAC modeler, churn model, pricing sensitivity |
| Diagnostics Board | Performance management | KPI variance diagnosis, leading indicators, action recommendations |

---

## Live Demo

> Deploy to Streamlit Cloud in one click — see deployment section below.

---

## Screenshots

_Add screenshots of each module after first run_

---

## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit |
| Data & modelling | Python, Pandas, NumPy, scikit-learn |
| Visualisation | Plotly |
| AI synthesis | Ollama + Mistral (local) — falls back to rich demo mode |
| Data | Synthetic PAYG portfolio + macro signals + competitor data |

---

## Project Structure
```
k-sip/
├── app.py                          # Home — platform overview + AI strategic brief
├── pages/
│   ├── 1_Early_Warning.py          # Module 1 — EA fintech risk index + regulatory tracker
│   ├── 2_War_Room.py               # Module 2 — competitor profiles + scenario war-game
│   ├── 3_Customer_Intelligence.py  # Module 3 — PAYG economics + churn + pricing
│   └── 4_Diagnostics_Board.py      # Module 4 — KPI diagnostics + action recommendations
├── utils/
│   ├── data_generator.py           # Synthetic PAYG portfolio, macro signals, competitor data
│   └── ai_synthesis.py             # Ollama/Mistral AI calls with demo fallback
├── assets/
├── requirements.txt
├── .env.example
└── README.md
```

---

## Quickstart

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/k-sip.git
cd k-sip
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```

The platform runs fully in demo mode without any API keys. To enable live AI briefs, install [Ollama](https://ollama.com) and run:
```bash
ollama pull mistral
```

### 5. Run the platform
```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## AI Features

K-SIP uses a local Ollama + Mistral setup for all AI synthesis. No cloud API keys required.

| Feature | Location | What it generates |
|---|---|---|
| Strategic brief | Homepage | Weekly executive intelligence summary across all four modules |
| Competitor narrative | War Room → Scenario tab | How a named competitor would respond to a selected scenario |
| KPI diagnosis | Diagnostics Board | Root cause + recommended action for any metric below target |

**Demo mode:** If Ollama is not running, all AI features fall back to rich pre-built content so the platform remains fully functional for demos and presentations.

---

## Data

All data is synthetically generated and does not represent any real company or individual. The synthetic datasets are calibrated to reflect realistic Kenya PAYG solar/fintech market dynamics:

- **PAYG customer portfolio** — 1,200 customers across 15 counties, 5 product tiers, 4 income segments
- **Macro signals** — 24 months of CBK rate, KES/USD, inflation, mobile money volume, credit growth
- **Competitor profiles** — 5 EA PAYG/fintech players with strategic intent and vulnerability mapping
- **Regulatory events** — 8 CBK/EPRA/KRA events with strategic implication analysis

---

## Module Detail

### Module 1 — Early Warning System

Tracks the EA Fintech Risk Index (0–100 composite of KES depreciation, inflation, CBK rate, credit growth slowdown) against alert thresholds. Includes a regulatory event tracker with strategic implication notes for each CBK/EPRA/KRA development.

**Key outputs:** Risk index trend, signal decomposition, regulatory event feed with strategic implications

### Module 2 — Competitive War Room

Profiles five EA PAYG and fintech competitors by customer base, pricing, churn, and strategic intent. The scenario war-game engine lets you select any macro/regulatory scenario and generate an AI narrative of how a named competitor would respond and what pre-emptive action M-KOPA should take. The whitespace map identifies counties with low PAYG penetration and large addressable markets.

**Key outputs:** Competitor scatter plot, war-game AI narratives, whitespace opportunity table

### Module 3 — Customer Intelligence Engine

Segments 1,200 synthetic PAYG customers by income band and analyses unit economics per segment. The LTV/CAC modeler lets you adjust price, CAC, and payment rate assumptions and see the impact on the LTV curve in real time. A Gradient Boosting churn model identifies high-risk accounts with a probability score. Pricing sensitivity analysis models revenue impact of price changes per segment using demand elasticity assumptions calibrated to Kenya.

**Key outputs:** Segment net economics, LTV/CAC modeler, churn intervention list, pricing sensitivity curves

### Module 4 — Strategic Performance Diagnostics Board

Goes beyond reporting numbers — every KPI has an actual vs target comparison with a visual bar, and underperforming KPIs have a one-click AI diagnosis that identifies root cause and recommends a specific action with owner and timeline. Leading indicator trends (mobile money volume, credit growth) provide forward-looking context.

**Key outputs:** KPI diagnostic bars, AI variance explanations, leading indicator trends, recommended action table

---

## Deployment (Streamlit Cloud)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select `k-sip` repo, branch `main`, main file `app.py`
5. Deploy

> Note: AI features will run in demo mode on Streamlit Cloud since Ollama requires a local runtime. All four modules and all charts are fully functional without Ollama.

---

## Roadmap

- [ ] Live CBK data feed via public API
- [ ] NSE market data integration (extends `NSETrendTracker`)
- [ ] PDF export of weekly strategic brief
- [ ] Multi-user role-based views (analyst vs executive)
- [ ] Integration with `afrikana-analytics` toolkit for reusable pipeline components

---

## Author

**Peterson Muriuki**
Data Analyst · Business Analyst · AI Engineer · Financial Engineer

- Email: pitmuriuki@gmail.com
- LinkedIn: [linkedin.com/in/peterson-muriuki](https://linkedin.com/in/peterson-muriuki)
- GitHub: [github.com/Peterson-Muriuki](https://github.com/Peterson-Muriuki)
- MSc Financial Engineering — WorldQuant University (ongoing)

---

## Related Projects

| Repo | Relation |
|---|---|
| `competitor-intelligence-agent` | Powers the war room competitor data pipeline |
| `macro_quant_dashboard` | Source of the macro signal architecture used in Module 1 |
| `KenyaCreditAI` / `msme-credit-scoring` | Credit risk logic adapted for Module 3 churn model |
| `afrikana-analytics` | Reusable analytics toolkit that K-SIP modules will consume |
| `NSETrendTracker` | NSE data layer planned for roadmap integration |

---

## License

MIT License — free to use, fork, and build on with attribution.

---

_Built to demonstrate what strategic BI looks like when it goes beyond dashboards — proactive intelligence, competitive foresight, and AI-generated recommendations._"# k-sip" 
