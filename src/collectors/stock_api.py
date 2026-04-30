"""
Stock data reader for the Akira Stocks v2 database.

The Streamlit app must not call Yahoo Finance directly. Market data is collected by
Akira's hourly core pipeline and stored in Supabase. This module only reads the
latest database snapshots and portfolio ledger tables.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict

import pandas as pd
import requests


class StockCollector:
    """Reads stock, signal and demo-portfolio data from Supabase."""

    def __init__(self):
        self.supabase_url, self.service_key = self._load_credentials()
        self.session = requests.Session()
        self.headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _load_credentials() -> tuple[str, str]:
        url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        if url and key:
            return url.rstrip("/"), key

        secrets_path = Path.home() / "secrets.json"
        if secrets_path.exists():
            with secrets_path.open("r", encoding="utf-8") as f:
                secrets = json.load(f)
            for nugget in secrets.get("nuggets", []):
                if nugget.get("name") == "supabase":
                    values = {c["key"]: c["value"] for c in nugget.get("config", [])}
                    return values["NEXT_PUBLIC_SUPABASE_URL"].rstrip("/"), values["SUPABASE_SERVICE_ROLE_KEY"]

        raise RuntimeError("Supabase credentials not found. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.")

    def _select(self, table: str, params: dict[str, Any]) -> pd.DataFrame:
        response = self.session.get(
            f"{self.supabase_url}/rest/v1/{table}",
            headers=self.headers,
            params=params,
            timeout=30,
        )
        if response.status_code != 200:
            raise RuntimeError(f"Supabase read failed for {table}: {response.status_code} {response.text}")
        return pd.DataFrame(response.json())

    @staticmethod
    def _latest_by_symbol(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or "yahoo_symbol" not in df.columns:
            return df
        return df.drop_duplicates(subset=["yahoo_symbol"], keep="first").reset_index(drop=True)

    def get_latest_prices(self, limit: int = 1000) -> pd.DataFrame:
        """Latest price snapshot per Yahoo symbol from `akira_stocks_price_snapshots`."""
        df = self._select(
            "akira_stocks_price_snapshots",
            {
                "select": "symbol,yahoo_symbol,name,price,previous_close,change_abs,change_pct,volume,avg_volume,relative_volume,market_cap,pe_ratio,fifty_two_week_position,currency,exchange,market_state,captured_at",
                "order": "captured_at.desc",
                "limit": limit,
            },
        )
        df = self._latest_by_symbol(df)
        if df.empty:
            return df
        return df.rename(columns={"change_pct": "change_percent", "change_abs": "change"})

    def get_latest_indicators(self, limit: int = 1000) -> pd.DataFrame:
        """Latest indicator snapshot per Yahoo symbol from `akira_stocks_indicator_snapshots`."""
        df = self._select(
            "akira_stocks_indicator_snapshots",
            {
                "select": "symbol,yahoo_symbol,price,rsi_14,sma_20,sma_50,sma_200,price_change_1h,price_change_today,volume_spike_level,is_candidate,candidate_reasons,vwap,vwap_distance_pct,atr_14,data_quality,score,signal,confidence,captured_at",
                "order": "captured_at.desc",
                "limit": limit,
            },
        )
        return self._latest_by_symbol(df)

    def get_stock_universe(self, limit: int = 1000) -> pd.DataFrame:
        return self._select(
            "akira_stocks_assets",
            {
                "select": "symbol,yahoo_symbol,name,exchange,currency,country,instrument_type,revolut_status,is_active,updated_at",
                "is_active": "eq.true",
                "order": "yahoo_symbol.asc",
                "limit": limit,
            },
        )

    def get_stock_table(self, limit: int = 1000) -> pd.DataFrame:
        """Combined latest prices + indicators from the v2 core tables."""
        prices = self.get_latest_prices(limit)
        indicators = self.get_latest_indicators(limit)
        if prices.empty:
            return prices
        if indicators.empty:
            return prices

        indicator_cols = [
            "yahoo_symbol", "rsi_14", "sma_20", "sma_50", "sma_200", "price_change_1h",
            "price_change_today", "volume_spike_level", "is_candidate", "vwap_distance_pct",
            "atr_14", "data_quality", "score", "signal", "confidence",
        ]
        indicator_cols = [c for c in indicator_cols if c in indicators.columns]
        return prices.merge(indicators[indicator_cols], on="yahoo_symbol", how="left")

    def get_top_movers(self, limit: int = 20) -> pd.DataFrame:
        df = self.get_stock_table()
        if df.empty or "change_percent" not in df.columns:
            return pd.DataFrame()
        df = df.copy()
        df["change_percent"] = pd.to_numeric(df["change_percent"], errors="coerce")
        df = df.dropna(subset=["change_percent"])
        df = df.reindex(df["change_percent"].abs().sort_values(ascending=False).index)
        return df.head(limit)

    def get_most_active(self, limit: int = 20) -> pd.DataFrame:
        df = self.get_stock_table()
        if df.empty or "volume" not in df.columns:
            return pd.DataFrame()
        df = df.copy()
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce")
        return df.sort_values("volume", ascending=False).head(limit)

    def get_latest_signals(self, limit: int = 50) -> pd.DataFrame:
        return self._select(
            "akira_stocks_signal_events",
            {
                "select": "symbol,yahoo_symbol,event_type,old_signal,new_signal,old_score,new_score,score_delta,price,reason,severity,current_price_change_1h,current_volume_spike_level,current_vwap_distance_pct,current_rsi_14,current_confidence,created_at",
                "order": "created_at.desc",
                "limit": limit,
            },
        )

    def get_portfolio_snapshots(self, limit: int = 20) -> pd.DataFrame:
        snapshots = self._select(
            "akira_stocks_portfolio_snapshots",
            {
                "select": "portfolio_id,cash,positions_value,total_value,realized_pnl,unrealized_pnl,total_return_pct,num_positions,num_transactions,metadata,created_at",
                "order": "created_at.desc",
                "limit": 200,
            },
        )
        if snapshots.empty:
            return snapshots
        snapshots = snapshots.drop_duplicates(subset=["portfolio_id"], keep="first")
        portfolios = self._select(
            "akira_stocks_portfolios",
            {
                "select": "id,name,strategy_key,base_currency,is_active",
                "is_active": "eq.true",
                "limit": 100,
            },
        )
        if not portfolios.empty:
            snapshots = snapshots.merge(portfolios, left_on="portfolio_id", right_on="id", how="left")
        return snapshots.head(limit)

    def get_recent_transactions(self, limit: int = 50) -> pd.DataFrame:
        tx = self._select(
            "akira_stocks_portfolio_transactions",
            {
                "select": "portfolio_id,transaction_type,symbol,yahoo_symbol,quantity,price,gross_amount,fee,net_amount,currency,reason,created_at",
                "order": "created_at.desc",
                "limit": limit,
            },
        )
        if tx.empty:
            return tx
        portfolios = self._select(
            "akira_stocks_portfolios",
            {"select": "id,name,strategy_key", "limit": 100},
        )
        if not portfolios.empty:
            tx = tx.merge(portfolios, left_on="portfolio_id", right_on="id", how="left")
        return tx

    def get_stock_info(self, symbol: str) -> Dict:
        df = self.get_stock_table()
        if df.empty:
            return {}
        matches = df[(df["symbol"] == symbol) | (df["yahoo_symbol"] == symbol)]
        if matches.empty:
            return {}
        return matches.iloc[0].to_dict()


if __name__ == "__main__":
    collector = StockCollector()
    print("🔥 TOP MOVERS FROM DB:")
    print(collector.get_top_movers(10)[["symbol", "price", "change_percent", "volume", "signal", "score"]].to_string())
    print("\n📊 PORTFOLIOS FROM DB:")
    print(collector.get_portfolio_snapshots().to_string())
