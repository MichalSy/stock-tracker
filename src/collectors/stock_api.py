"""
Stock Data Collector using Yahoo Finance API
"""
import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class StockCollector:
    """Collects stock market data from Yahoo Finance"""
    
    def __init__(self):
        self.cache = {}
    
    def get_top_movers(self, limit: int = 20) -> pd.DataFrame:
        """
        Get top gaining/losing stocks from Yahoo Finance
        
        Returns DataFrame with columns:
        - symbol
        - name
        - price
        - change
        - change_percent
        - volume
        - avg_volume
        - volume_ratio (current vs avg)
        """
        try:
            # Yahoo Finance screener for top gainers
            # Using pre-defined list of popular stocks as MVP
            tickers = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'AMD', 'INTC',
                'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'HD', 'DIS', 'NFLX', 'PYPL', 'ADBE',
                'CRM', 'CMCSA', 'PFE', 'KO', 'PEP', 'ABT', 'MRK', 'TMO', 'ABBV', 'COST',
                'AVGO', 'MCD', 'NKE', 'DHR', 'CSCO', 'ACN', 'WFC', 'BMY', 'NEE', 'VZ',
                'TXN', 'QCOM', 'LIN', 'HON', 'RTX', 'UPS', 'AMGN', 'PM', 'UNH', 'LOW'
            ]
            
            data = yf.download(tickers, period='2d', group_by='ticker', progress=False)
            
            results = []
            for ticker in tickers:
                try:
                    ticker_data = data[ticker]
                    if len(ticker_data) < 2:
                        continue
                    
                    current = ticker_data.iloc[-1]
                    previous = ticker_data.iloc[-2]
                    
                    change = current['Close'] - previous['Close']
                    change_pct = (change / previous['Close']) * 100
                    
                    # Get volume info
                    volume = current['Volume']
                    
                    results.append({
                        'symbol': ticker,
                        'price': current['Close'],
                        'change': change,
                        'change_percent': change_pct,
                        'volume': volume,
                    })
                except Exception as e:
                    continue
            
            df = pd.DataFrame(results)
            
            # Sort by absolute change percentage (biggest movers)
            df = df.reindex(df['change_percent'].abs().sort_values(ascending=False).index)
            
            return df.head(limit)
            
        except Exception as e:
            print(f"Error fetching stock data: {e}")
            return pd.DataFrame()
    
    def get_most_active(self, limit: int = 20) -> pd.DataFrame:
        """
        Get most actively traded stocks by volume
        """
        df = self.get_top_movers(limit=100)  # Get more to sort by volume
        
        if df.empty:
            return df
        
        # Sort by volume
        df = df.sort_values('volume', ascending=False)
        return df.head(limit)
    
    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get detailed info for a single stock
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', ''),
                'price': info.get('currentPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'pe_ratio': info.get('forwardPE', 0),
                '52week_high': info.get('fiftyTwoWeekHigh', 0),
                '52week_low': info.get('fiftyTwoWeekLow', 0),
            }
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return {}


if __name__ == "__main__":
    # Test
    collector = StockCollector()
    
    print("🔥 TOP MOVERS:")
    movers = collector.get_top_movers(10)
    print(movers[['symbol', 'price', 'change_percent', 'volume']].to_string())
    
    print("\n📊 MOST ACTIVE:")
    active = collector.get_most_active(10)
    print(active[['symbol', 'price', 'change_percent', 'volume']].to_string())
