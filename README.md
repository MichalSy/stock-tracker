# 🚀 Stock & Crypto Flow Radar

**MVP zur Erkennung von "Hot Money" - Wo fließt gerade Kapital hin?**

![Status](https://img.shields.io/badge/Status-Phase%201%20MVP-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📱 Screenshots (Streamlit Dashboard)

**Dark Theme Trading Dashboard** - Mobile responsive!

```
┌──────────────────────────────────────┐
│  📊 Flow Radar                        │
├──────────────────────────────────────┤
│  🔥 TOP MOVERS                        │
│  ├─ NVDA  +5.2%   Vol: 50M           │
│  ├─ TSLA  -3.1%   Vol: 45M           │
│  └─ AMD   +2.8%   Vol: 30M           │
├──────────────────────────────────────┤
│  🚀 TOP CRYPTO GAINERS (24h)          │
│  ├─ PEPE  +25%   Vol: $500M          │
│  └─ SOL   +12%   Vol: $2B            │
└──────────────────────────────────────┘
```

---

## 🎯 Projekt-Ziel

Ein Tool, das erkennt welche Aktien und Kryptowährungen **gerade massives Kaufinteresse** haben durch:
- Ungewöhnlich hohes Volumen
- Starke Preisbewegungen
- Whale-Aktivität (Krypto)
- Social Sentiment (optional)

**Use Case:** Early Detection von Trends um "auf den Zug aufzuspringen" bevor es mainstream wird.

---

## 📊 MVP Features (Phase 1)

### Aktien (US Market)
- **Top Movers** - Aktien mit stärkster Preisänderung
- **Unusual Volume** - Volumen vs. 30-Tage-Durchschnitt
- **Most Active** - Meistgehandelte Aktien
- **Sector Heatmap** - Welche Sektoren sind hot?

### Krypto
- **Top Gainers/Losers** (24h, 7d)
- **Highest Volume** - Exchange-übergreifend
- **Whale Alerts** - Große Transaktionen (>$100k)
- **Trending** auf CoinGecko/CMC

### Scoring-System
```python
# Beispiel Heat Score
heat_score = (
    volume_change * 0.4 +      # Ungewöhnliches Volumen
    price_momentum * 0.3 +     # Preisbewegung
    social_buzz * 0.2 +        # Reddit/Twitter (optional)
    whale_activity * 0.1       # Nur Krypto
)
```

---

## 🏗️ Architektur

```
stock-tracker/
├── src/
│   ├── collectors/          # Data Fetcher
│   │   ├── stock_api.py     # Yahoo Finance, Finnhub
│   │   ├── crypto_api.py    # Binance, CoinGecko
│   │   └── whale_api.py     # Whale Alert
│   ├── analyzers/           # Scoring & Analysis
│   │   ├── volume_analyzer.py
│   │   ├── momentum_scorer.py
│   │   └── heat_mapper.py
│   ├── models/              # Data Models
│   │   ├── stock.py
│   │   └── crypto.py
│   └── utils/               # Helper Functions
│       ├── cache.py
│       └── formatters.py
├── notebooks/               # Jupyter Notebooks für Exploration
├── data/                    # Cached Data (gitignored)
├── tests/                   # Unit Tests
├── requirements.txt         # Python Dependencies
└── README.md
```

---

## 🔧 Tech Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| **Language** | Python 3.11+ | Pandas, Data Science Ecosystem |
| **Stock Data** | yfinance, Finnhub (free tier) | Kostenlos, zuverlässig |
| **Crypto Data** | ccxt, CoinGecko API | Exchange-übergreifend |
| **Whale Tracking** | whale-alert.io API | On-chain Analytics |
| **Analysis** | pandas, numpy | Standard für Data |
| **Visualization** | plotly, matplotlib | Interaktive Charts |
| **Caching** | SQLite (local) | Kein externer DB nötig für MVP |
| **Frontend (MVP)** | Streamlit | Schnelles Data Dashboard, Mobile-ready |
| **Frontend (Future)** | React + TypeScript | Custom UI, Native Mobile Feel |

---

## 📅 Roadmap

### Phase 1: MVP (Aktuell)
- [x] Projekt-Setup & Repo
- [x] Stock Data Collector (yfinance)
- [x] Crypto Data Collector (CoinGecko)
- [x] CLI Output (Top 10 Listen)
- [x] Jupyter Notebook für Exploration
- [x] **Streamlit Frontend** (Mobile-ready Dashboard)
- [ ] Deploy auf eigener Domain

### Phase 2: Enhanced Analysis
- [ ] Whale Alert Integration
- [ ] Social Sentiment (Reddit API)
- [ ] Historical Backtesting
- [ ] Heat Score Algorithm optimieren
- [ ] **React Frontend Planung** (TypeScript Migration)

### Phase 3: React Migration & Automation
- [ ] **React + TypeScript Frontend** (Full Custom UI)
- [ ] Native Mobile Optimization
- [ ] Cronjob Scheduler
- [ ] Push Notifications (Telegram/Signal)
- [ ] Alert Thresholds konfigurierbar
- [ ] Database für Historical Data

### Phase 4: Advanced
- [ ] Multi-Asset Correlation Analysis
- [ ] Machine Learning Signals
- [ ] Options Flow Data
- [ ] Backtesting Framework
- [ ] Mobile App (React Native optional)

---

## 🚀 Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Option 1: Streamlit Frontend (Empfohlen)
streamlit run app.py
# → Öffne http://localhost:8501

# Option 2: CLI
python src/main.py --type stocks --limit 20
python src/main.py --type crypto --limit 20

# Option 3: Jupyter für Exploration
jupyter notebook notebooks/
```

---

## 📦 Data Sources (Free Tiers)

| Source | Data | Limit |
|--------|------|-------|
| **Yahoo Finance** | Stocks, Volume, Price | Unlimited (rate-limited) |
| **Finnhub** | Unusual Volume, News | 60 calls/min |
| **CoinGecko** | Crypto Prices, Trending | 10-50 calls/min |
| **Binance API** | Order Book, Volume | 1200 requests/min |
| **Whale Alert** | Large Transactions | Free tier: 10 calls/day |

---

## 🎯 Success Metrics

- **Accuracy:** Heat Score korreliert mit späteren Preisbewegungen
- **Speed:** Trends werden früher erkannt als Mainstream News
- **Coverage:** Min. 80% der relevanten US Stocks & Top 100 Crypto

---

## 📝 Notes

- **Keine Finanzberatung!** Nur Datenanalyse & Signale.
- MVP ist **manuell triggbar** (kein Auto-Refresh)
- Push-Notifications kommen in Phase 3

---

## 🎨 Frontend Evolution (Plan)

### Phase 1: Streamlit (Aktuell)
- ✅ Schnelles MVP Dashboard
- ✅ Mobile-responsive
- ✅ Dark Theme
- ✅ Plotly Charts
- ⚠️ Limitierte Customization

### Phase 3: React + TypeScript (Geplant)
Warum migrieren?
- 🎨 Volle Design-Kontrolle
- 📱 Native Mobile App Feel
- ⚡ Bessere Performance
- 🔧 Komplexere Features möglich

**Tech Stack (Phase 3):**
```
Frontend: React 18 + TypeScript + Vite
Charts: Recharts / TradingView Lightweight
State: Zustand / Jotai
Styling: Tailwind CSS
Mobile: PWA (Progressive Web App)
Backend: FastAPI (Python) - bereits vorhandene Collectors nutzen
```

**Migration Path:**
1. FastAPI Backend erstellen (endpoints für stocks/crypto)
2. React Frontend bauen (API consumed)
3. Streamlit deprecated
4. Deploy React app

---

## 👥 Contributors

- Michal (@MichalSy)
- Aiko ✨

---

**Status:** 🟡 In Development - Phase 1 Setup
