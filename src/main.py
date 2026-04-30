#!/usr/bin/env python3
"""Akira Stocks DB CLI.

Read-only helper for the same Supabase v2 core tables used by the Streamlit app.
No direct Yahoo/CoinGecko/API market calls happen here.
"""
from __future__ import annotations

import argparse
from datetime import datetime

import math

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from collectors.stock_api import StockCollector

console = Console()


def value_float(value, default: float = 0.0) -> float:
    try:
        result = float(value)
        if math.isnan(result) or math.isinf(result):
            return default
        return result
    except Exception:
        return default


def display_stocks(limit: int = 20) -> None:
    collector = StockCollector()
    console.print(Panel.fit("🔥 TOP STOCK MOVERS FROM DB", style="bold yellow"))
    movers = collector.get_top_movers(limit)
    if movers.empty:
        console.print("[red]No stock data available in DB[/red]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Symbol", style="cyan")
    table.add_column("Price", justify="right")
    table.add_column("Change %", justify="right")
    table.add_column("Volume", justify="right")
    table.add_column("Signal")
    table.add_column("Score", justify="right")

    for _, row in movers.iterrows():
        change = value_float(row.get("change_percent"))
        change_color = "green" if change > 0 else "red"
        table.add_row(
            str(row.get("symbol") or row.get("yahoo_symbol")),
            f"${value_float(row.get('price')):.2f}",
            f"[{change_color}]{change:+.2f}%[/{change_color}]",
            f"{value_float(row.get('volume')):,.0f}",
            str(row.get("signal") or "—"),
            f"{value_float(row.get('score')):.1f}",
        )
    console.print(table)


def display_portfolios(limit: int = 20) -> None:
    collector = StockCollector()
    console.print(Panel.fit("💼 DEMO PORTFOLIOS FROM DB", style="bold green"))
    portfolios = collector.get_portfolio_snapshots(limit)
    if portfolios.empty:
        console.print("[red]No portfolio snapshots available in DB[/red]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Depot")
    table.add_column("Total", justify="right")
    table.add_column("Cash", justify="right")
    table.add_column("Positions", justify="right")
    table.add_column("Return", justify="right")
    table.add_column("Open", justify="right")

    for _, row in portfolios.iterrows():
        table.add_row(
            str(row.get("name") or row.get("strategy_key")),
            f"€{value_float(row.get('total_value')):,.2f}",
            f"€{value_float(row.get('cash')):,.2f}",
            f"€{value_float(row.get('positions_value')):,.2f}",
            f"{value_float(row.get('total_return_pct')):+.2f}%",
            str(int(row.get("num_positions") or 0)),
        )
    console.print(table)


def display_signals(limit: int = 20) -> None:
    collector = StockCollector()
    console.print(Panel.fit("⚡ LATEST SIGNAL EVENTS FROM DB", style="bold magenta"))
    signals = collector.get_latest_signals(limit)
    if signals.empty:
        console.print("[red]No signals available in DB[/red]")
        return

    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Time")
    table.add_column("Symbol", style="cyan")
    table.add_column("Event")
    table.add_column("Signal")
    table.add_column("Score", justify="right")
    table.add_column("Reason")

    for _, row in signals.iterrows():
        table.add_row(
            str(row.get("created_at"))[:19],
            str(row.get("symbol") or row.get("yahoo_symbol")),
            str(row.get("event_type") or "—"),
            str(row.get("new_signal") or "—"),
            f"{value_float(row.get('new_score')):.1f}",
            str(row.get("reason") or "")[:80],
        )
    console.print(table)


def main() -> None:
    parser = argparse.ArgumentParser(description="Akira Stocks DB dashboard CLI")
    parser.add_argument("--type", choices=["stocks", "signals", "portfolios", "all"], default="all")
    parser.add_argument("--limit", type=int, default=15)
    args = parser.parse_args()

    console.print(f"[bold cyan]📊 AKIRA STOCKS DB - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold cyan]\n")
    if args.type in ["stocks", "all"]:
        display_stocks(args.limit)
        console.print()
    if args.type in ["signals", "all"]:
        display_signals(args.limit)
        console.print()
    if args.type in ["portfolios", "all"]:
        display_portfolios(args.limit)


if __name__ == "__main__":
    main()
