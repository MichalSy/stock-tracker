"""
Crypto Data Collector using CoinGecko API (free, no API key needed)
"""
import requests
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime


class CryptoCollector:
    """Collects cryptocurrency data from CoinGecko API"""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_top_gainers(self, limit: int = 20) -> pd.DataFrame:
        """
        Get top gaining cryptocurrencies (24h)
        
        Returns DataFrame with:
        - id, symbol, name
        - current_price
        - price_change_24h, price_change_percentage_24h
        - total_volume, market_cap
        """
        try:
            # Get top 100 by market cap, then sort by price change
            url = f"{self.BASE_URL}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 100,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h,7d'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            df = pd.DataFrame(data)
            
            # Sort by 24h price change (descending)
            df = df.sort_values('price_change_percentage_24h', ascending=False)
            
            return df.head(limit)
            
        except Exception as e:
            print(f"Error fetching crypto data: {e}")
            return pd.DataFrame()
    
    def get_top_losers(self, limit: int = 20) -> pd.DataFrame:
        """Get top losing cryptocurrencies (24h)"""
        try:
            df = self.get_top_gainers(limit=100)
            if df.empty:
                return df
            
            # Sort ascending (most negative first)
            df = df.sort_values('price_change_percentage_24h', ascending=True)
            return df.head(limit)
            
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()
    
    def get_trending(self) -> pd.DataFrame:
        """
        Get trending coins on CoinGecko (community interest)
        """
        try:
            url = f"{self.BASE_URL}/search/trending"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            coins = []
            for item in data.get('coins', []):
                coin = item['item']
                coins.append({
                    'id': coin.get('id'),
                    'symbol': coin.get('symbol'),
                    'name': coin.get('name'),
                    'market_cap_rank': coin.get('market_cap_rank'),
                    'score': coin.get('score'),  # Trending score
                })
            
            return pd.DataFrame(coins)
            
        except Exception as e:
            print(f"Error fetching trending: {e}")
            return pd.DataFrame()
    
    def get_most_active(self, limit: int = 20) -> pd.DataFrame:
        """Get most active by trading volume"""
        try:
            url = f"{self.BASE_URL}/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'volume_desc',
                'per_page': limit,
                'page': 1,
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Error: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    # Test
    collector = CryptoCollector()
    
    print("🚀 TOP GAINERS (24h):")
    gainers = collector.get_top_gainers(10)
    if not gainers.empty:
        print(gainers[['symbol', 'name', 'current_price', 'price_change_percentage_24h', 'total_volume']].to_string())
    
    print("\n📉 TOP LOSERS (24h):")
    losers = collector.get_top_losers(10)
    if not losers.empty:
        print(losers[['symbol', 'name', 'current_price', 'price_change_percentage_24h']].to_string())
    
    print("\n🔥 TRENDING:")
    trending = collector.get_trending()
    if not trending.empty:
        print(trending.to_string())
