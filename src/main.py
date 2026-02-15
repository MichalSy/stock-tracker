#!/usr/bin/env python3
"""
Stock & Crypto Flow Radar - Main Entry Point

Usage:
    python src/main.py --type stocks --limit 20
    python src/main.py --type crypto --limit 20
    python src/main.py --type all
"""
import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from collectors.stock_api import StockCollector
from collectors.crypto_api import CryptoCollector


console = Console()


def display_stocks(limit: int = 20):
    """Display stock market analysis"""
    collector = StockCollector()
    
    # Top Movers
    console.print(Panel.fit("🔥 TOP STOCK MOVERS", style="bold yellow"))
    movers = collector.get_top_movers(limit)
    
    if not movers.empty:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Symbol", style="cyan")
        table.add_column("Price", justify="right")
        table.add_column("Change %", justify="right")
        table.add_column("Volume", justify="right")
        
        for _, row in movers.iterrows():
            change_color = "green" if row['change_percent'] > 0 else "red"
            table.add_row(
                row['symbol'],
                f"${row['price']:.2f}",
                f"[{change_color}]{row['change_percent']:+.2f}%[/{change_color}]",
                f"{row['volume']:,.0f}"
            )
        
        console.print(table)
    else:
        console.print("[red]No data available[/red]")
    
    # Most Active
    console.print(f"\n[bold]📊 MOST ACTIVE (Volume)[/bold]")
    active = collector.get_most_active(limit)
    
    if not active.empty:
        table2 = Table(show_header=True, header_style="bold cyan")
        table2.add_column("Symbol", style="cyan")
        table2.add_column("Price", justify="right")
        table2.add_column("Volume", justify="right")
        table2.add_column("Change %", justify="right")
        
        for _, row in active.iterrows():
            change_color = "green" if row['change_percent'] > 0 else "red"
            table2.add_row(
                row['symbol'],
                f"${row['price']:.2f}",
                f"{row['volume']:,.0f}",
                f"[{change_color}]{row['change_percent']:+.2f}%[/{change_color}]"
            )
        
        console.print(table2)


def display_crypto(limit: int = 20):
    """Display crypto market analysis"""
    collector = CryptoCollector()
    
    # Top Gainers
    console.print(Panel.fit("🚀 TOP CRYPTO GAINERS (24h)", style="bold green"))
    gainers = collector.get_top_gainers(limit)
    
    if not gainers.empty:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("#", justify="right")
        table.add_column("Symbol", style="cyan")
        table.add_column("Name")
        table.add_column("Price", justify="right")
        table.add_column("24h Change", justify="right")
        table.add_column("Volume ($)", justify="right")
        
        for idx, (_, row) in enumerate(gainers.iterrows(), 1):
            change = row['price_change_percentage_24h']
            change_color = "green" if change > 0 else "red"
            table.add_row(
                str(idx),
                row['symbol'].upper(),
                row['name'][:20],
                f"${row['current_price']:,.4f}" if row['current_price'] < 1 else f"${row['current_price']:,.2f}",
                f"[{change_color}]{change:+.2f}%[/{change_color}]",
                f"${row['total_volume']:,.0f}"
            )
        
        console.print(table)
    
    # Trending
    console.print(f"\n[bold]🔥 TRENDING ON COINGECKO[/bold]")
    trending = collector.get_trending()
    
    if not trending.empty:
        t_table = Table(show_header=True, header_style="bold cyan")
        t_table.add_column("#", justify="right")
        t_table.add_column("Symbol", style="cyan")
        t_table.add_column("Name")
        t_table.add_column("Market Cap Rank", justify="right")
        
        for idx, (_, row) in enumerate(trending.iterrows(), 1):
            t_table.add_row(
                str(idx),
                row['symbol'].upper(),
                row['name'][:20],
                f"#{row['market_cap_rank']}" if row['market_cap_rank'] else "N/A"
            )
        
        console.print(t_table)


def main():
    parser = argparse.ArgumentParser(description='Stock & Crypto Flow Radar')
    parser.add_argument('--type', choices=['stocks', 'crypto', 'all'], default='all',
                       help='What to analyze')
    parser.add_argument('--limit', type=int, default=15,
                       help='Number of items to show')
    
    args = parser.parse_args()
    
    console.print(f"[bold cyan]📊 FLOW RADAR - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/bold cyan]\n")
    
    if args.type in ['stocks', 'all']:
        display_stocks(args.limit)
        console.print()
    
    if args.type in ['crypto', 'all']:
        display_crypto(args.limit)
    
    console.print(f"\n[dim]💡 Tip: Use --type stocks/crypto for specific markets[/dim]")


if __name__ == "__main__":
    main()
