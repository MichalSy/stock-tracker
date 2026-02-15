# 🚀 Stock & Crypto Flow Radar

**MVP zur Erkennung von "Hot Money" - Wo fließt gerade Kapital hin?**

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

---

## 📅 Roadmap

### Phase 1: MVP (Aktuell)
- [x] Projekt-Setup & Repo
- [ ] Stock Data Collector (yfinance)
- [ ] Crypto Data Collector (ccxt)
- [ ] Basic Heat Score Algorithm
- [ ] CLI Output (Top 10 Listen)
- [ ] Jupyter Notebook für Exploration

### Phase 2: Enhanced Analysis
- [ ] Whale Alert Integration
- [ ] Social Sentiment (Reddit API)
- [ ] Historical Backtesting
- [ ] Web Dashboard (Streamlit)

### Phase 3: Automation
- [ ] Cronjob Scheduler
- [ ] Push Notifications (Telegram/Signal)
- [ ] Alert Thresholds konfigurierbar
- [ ] Database für Historical Data

### Phase 4: Advanced
- [ ] Multi-Asset Correlation Analysis
- [ ] Machine Learning Signals
- [ ] Options Flow Data
- [ ] Backtesting Framework

---

## 🚀 Quick Start

```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run Analysis
python src/main.py --type stocks --limit 20
python src/main.py --type crypto --limit 20

# Start Jupyter für Exploration
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

## 👥 Contributors

- Michal (@MichalSy)
- Aiko ✨

---

**Status:** 🟡 In Development - Phase 1 Setup
