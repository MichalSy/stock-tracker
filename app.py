#!/usr/bin/env python3
"""
Akira Stocks Dashboard - Streamlit Frontend

Important: this app is read-only and only displays data from Akira's Supabase
v2 core tables. It does not call Yahoo Finance or other market APIs directly.

Run with:
    streamlit run app.py
"""
from __future__ import annotations

from datetime import datetime
import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.collectors.stock_api import StockCollector


st.set_page_config(
    page_title="Akira Stocks 📊",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .stApp { background-color: #0e1117; color: #fafafa; }
    [data-testid="stMetricValue"] { font-size: 1.5rem; color: #00d4aa; }
    [data-testid="stSidebar"] { background-color: #1a1d24; }
    .positive { color: #00d4aa; }
    .negative { color: #ff4b4b; }
</style>
""",
    unsafe_allow_html=True,
)


def money(value, currency="$") -> str:
    try:
        if pd.isna(value):
            return "—"
        return f"{currency}{float(value):,.2f}"
    except Exception:
        return "—"


def pct(value) -> str:
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):+.2f}%"
    except Exception:
        return "—"


def number(value) -> str:
    try:
        if pd.isna(value):
            return "—"
        return f"{float(value):,.0f}"
    except Exception:
        return "—"


def display_stock_table(df: pd.DataFrame, title: str, limit: int) -> None:
    st.subheader(title)
    if df.empty:
        st.warning("Keine Daten in der Datenbank gefunden.")
        return

    display_cols = [
        "symbol", "name", "price", "change_percent", "volume", "relative_volume",
        "signal", "score", "confidence", "rsi_14", "volume_spike_level", "currency", "captured_at",
    ]
    display_cols = [c for c in display_cols if c in df.columns]
    out = df[display_cols].head(limit).copy()
    rename = {
        "symbol": "Symbol", "name": "Name", "price": "Preis", "change_percent": "Änderung",
        "volume": "Volumen", "relative_volume": "Rel. Vol.", "signal": "Signal", "score": "Score",
        "confidence": "Confidence", "rsi_14": "RSI", "volume_spike_level": "Volumen-Level",
        "currency": "Währung", "captured_at": "Datenzeit",
    }
    if "Preis" not in out.columns and "price" in out.columns:
        pass
    if "price" in out.columns:
        out["price"] = out["price"].apply(lambda x: money(x, "$"))
    if "change_percent" in out.columns:
        out["change_percent"] = out["change_percent"].apply(pct)
    if "volume" in out.columns:
        out["volume"] = out["volume"].apply(number)
    for col in ["relative_volume", "score", "confidence", "rsi_14"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").round(2)
    out = out.rename(columns=rename)
    st.dataframe(out, use_container_width=True, hide_index=True)


def display_stocks_tab(collector: StockCollector, limit: int) -> None:
    movers = collector.get_top_movers(limit)
    if not movers.empty:
        fig = px.bar(
            movers.head(15),
            x="symbol",
            y="change_percent",
            title="Top Movers aus DB (% Änderung)",
            color="change_percent",
            color_continuous_scale="RdYlGn",
            text="change_percent",
        )
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#fafafa")
        st.plotly_chart(fig, use_container_width=True)

    display_stock_table(movers, "🔥 Top Movers", limit)
    st.divider()
    display_stock_table(collector.get_most_active(limit), "📊 Most Active", limit)


def display_signals_tab(collector: StockCollector, limit: int) -> None:
    st.subheader("⚡ Neueste Signal-Events")
    signals = collector.get_latest_signals(limit)
    if signals.empty:
        st.warning("Keine Signal-Events gefunden.")
        return

    cols = [
        "created_at", "symbol", "event_type", "severity", "old_signal", "new_signal",
        "old_score", "new_score", "score_delta", "price", "reason",
        "current_price_change_1h", "current_volume_spike_level", "current_rsi_14",
    ]
    cols = [c for c in cols if c in signals.columns]
    out = signals[cols].copy()
    if "price" in out.columns:
        out["price"] = out["price"].apply(lambda x: money(x, "$"))
    for col in ["old_score", "new_score", "score_delta", "current_price_change_1h", "current_rsi_14"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").round(2)
    st.dataframe(out, use_container_width=True, hide_index=True)


def display_portfolios_tab(collector: StockCollector, limit: int) -> None:
    st.subheader("💼 Demo-Depots")
    snapshots = collector.get_portfolio_snapshots()
    if snapshots.empty:
        st.warning("Keine Portfolio-Snapshots gefunden.")
    else:
        cols = [
            "name", "strategy_key", "cash", "positions_value", "total_value", "realized_pnl",
            "unrealized_pnl", "total_return_pct", "num_positions", "num_transactions", "created_at",
        ]
        cols = [c for c in cols if c in snapshots.columns]
        out = snapshots[cols].copy()
        for col in ["cash", "positions_value", "total_value", "realized_pnl", "unrealized_pnl"]:
            if col in out.columns:
                out[col] = out[col].apply(lambda x: money(x, "€"))
        if "total_return_pct" in out.columns:
            out["total_return_pct"] = out["total_return_pct"].apply(pct)
        st.dataframe(out, use_container_width=True, hide_index=True)

        latest = snapshots.sort_values("created_at", ascending=False).head(5)
        cols = st.columns(min(5, len(latest)))
        for idx, (_, row) in enumerate(latest.iterrows()):
            with cols[idx % len(cols)]:
                st.metric(
                    label=row.get("name", row.get("strategy_key", "Depot")),
                    value=money(row.get("total_value"), "€"),
                    delta=pct(row.get("total_return_pct")),
                )

    st.divider()
    st.subheader("🧾 Neueste Transaktionen")
    tx = collector.get_recent_transactions(limit)
    if tx.empty:
        st.warning("Keine Transaktionen gefunden.")
        return
    cols = ["created_at", "name", "transaction_type", "yahoo_symbol", "quantity", "price", "net_amount", "fee", "currency", "reason"]
    cols = [c for c in cols if c in tx.columns]
    out = tx[cols].copy()
    for col in ["quantity", "price", "net_amount", "fee"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce").round(4)
    st.dataframe(out, use_container_width=True, hide_index=True)


def display_overview(collector: StockCollector) -> None:
    stocks = collector.get_stock_table()
    signals = collector.get_latest_signals(10)
    portfolios = collector.get_portfolio_snapshots()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Aktien im Core", len(stocks) if not stocks.empty else 0)
    col2.metric("Kandidaten", int(stocks.get("is_candidate", pd.Series(dtype=bool)).fillna(False).sum()) if not stocks.empty else 0)
    col3.metric("Neue Events", len(signals) if not signals.empty else 0)
    col4.metric("Aktive Depots", len(portfolios) if not portfolios.empty else 0)

    st.info("Datenquelle: Supabase v2 Core Tabellen (`akira_stocks_*`). Kein Yahoo-Zugriff in der App.")

    if not stocks.empty and "captured_at" in stocks.columns:
        st.markdown(f"**Neuester Preis-Snapshot:** `{stocks['captured_at'].max()}`")

    st.divider()
    display_stock_table(collector.get_top_movers(10), "🔥 Schneller Überblick: Top Movers", 10)


def main() -> None:
    st.sidebar.title("📊 Akira Stocks")
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Overview", "📈 Stocks", "⚡ Signale", "💼 Depots"],
        label_visibility="collapsed",
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Settings")
    limit = st.sidebar.slider("Items to show", 5, 100, 20)

    auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=False)
    if auto_refresh:
        st.sidebar.info("⏱️ Refreshing every 5 minutes")
        import time

        time.sleep(300)
        st.rerun()

    st.title("📊 Akira Stocks Dashboard")
    st.markdown(f"**App-Zeit:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")

    @st.cache_resource(ttl=300)
    def get_stock_collector():
        return StockCollector()

    collector = get_stock_collector()

    with st.spinner("Lade Daten aus Supabase..."):
        if page == "🏠 Overview":
            display_overview(collector)
        elif page == "📈 Stocks":
            display_stocks_tab(collector, limit)
        elif page == "⚡ Signale":
            display_signals_tab(collector, limit)
        elif page == "💼 Depots":
            display_portfolios_tab(collector, limit)

    st.markdown("---")
    st.markdown(
        """
    <div style='text-align: center; color: #666;'>
        Akira Stocks v2 · read-only DB dashboard · built with Michal
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
