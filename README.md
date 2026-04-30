# 📊 Akira Stocks Dashboard

Read-only Streamlit dashboard for Akira's stock-analysis core.

## Wichtig

Die App holt **keine Marktdaten direkt von Yahoo, CoinGecko oder anderen externen APIs**.
Sie zeigt nur Daten an, die bereits von der Akira-Core-Pipeline in Supabase gespeichert wurden.

Aktuelle Pipeline:

```text
XX:00 Collector          → akira_stocks_price_snapshots
XX:10 Indicator Engine   → akira_stocks_indicator_snapshots
XX:20 Signal Engine      → akira_stocks_signal_events
XX:30 Portfolio Engine   → akira_stocks_portfolio_* Tabellen
```

## Genutzte DB-Tabellen

- `akira_stocks_assets`
- `akira_stocks_price_snapshots`
- `akira_stocks_indicator_snapshots`
- `akira_stocks_signal_events`
- `akira_stocks_portfolios`
- `akira_stocks_portfolio_snapshots`
- `akira_stocks_portfolio_transactions`

## Features

- Übersicht über aktuelle Core-Daten
- Top Movers aus der Datenbank
- Most Active aus der Datenbank
- Neueste Signal-Events
- Demo-Depot Übersicht
- Neueste Portfolio-Transaktionen

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Credentials:

```bash
export SUPABASE_URL="https://...supabase.co"
export SUPABASE_SERVICE_ROLE_KEY="..."
```

Auf Akiras Host kann die App alternativ `~/secrets.json` lesen.

## Start

```bash
streamlit run app.py
```

CLI:

```bash
python src/main.py --type all --limit 20
python src/main.py --type stocks
python src/main.py --type signals
python src/main.py --type portfolios
```

## Architektur

```text
stock-tracker/
├── app.py                     # Streamlit UI
├── src/
│   ├── collectors/
│   │   └── stock_api.py       # Supabase DB reader, no Yahoo calls
│   └── main.py                # DB-only CLI helper
├── requirements.txt
└── README.md
```

## Tests / Checks

```bash
python -m py_compile app.py src/collectors/stock_api.py src/main.py
python src/main.py --type all --limit 5
```
