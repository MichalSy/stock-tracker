#!/usr/bin/env python3
"""
Stock & Crypto Flow Radar - Streamlit Frontend

Run with:
    streamlit run app.py

Access at:
    http://localhost:8501
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.collectors.stock_api import StockCollector
from src.collectors.crypto_api import CryptoCollector


# Page config
st.set_page_config(
    page_title="Flow Radar 📊",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    /* Dark Theme Colors */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        color: #00d4aa;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1d24;
    }
    
    /* Tables */
    .stDataFrame {
        background-color: #1a1d24;
    }
    
    /* Positive change */
    .positive {
        color: #00d4aa;
    }
    
    /* Negative change */
    .negative {
        color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)


def display_stock_tab(collector: StockCollector, limit: int):
    """Display stock analysis"""
    
    # Top Movers
    st.subheader("🔥 Top Movers")
    movers = collector.get_top_movers(limit)
    
    if not movers.empty:
        # Chart
        fig = px.bar(
            movers.head(15),
            x='symbol',
            y='change_percent',
            title='Top Stock Movers (% Change)',
            color='change_percent',
            color_continuous_scale='RdYlGn',
            text='change_percent'
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#fafafa',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Table
        movers_display = movers.copy()
        movers_display['price'] = movers_display['price'].apply(lambda x: f"${x:.2f}")
        movers_display['change_percent'] = movers_display['change_percent'].apply(lambda x: f"{x:+.2f}%")
        movers_display['volume'] = movers_display['volume'].apply(lambda x: f"{x:,.0f}")
        movers_display = movers_display.rename(columns={
            'symbol': 'Symbol',
            'price': 'Price',
            'change_percent': 'Change %',
            'volume': 'Volume'
        })
        
        st.dataframe(
            movers_display,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No stock data available")
    
    st.divider()
    
    # Most Active
    st.subheader("📊 Most Active (Volume)")
    active = collector.get_most_active(limit)
    
    if not active.empty:
        active_display = active.copy()
        active_display['price'] = active_display['price'].apply(lambda x: f"${x:.2f}")
        active_display['change_percent'] = active_display['change_percent'].apply(lambda x: f"{x:+.2f}%")
        active_display['volume'] = active_display['volume'].apply(lambda x: f"{x:,.0f}")
        active_display = active_display.rename(columns={
            'symbol': 'Symbol',
            'price': 'Price',
            'change_percent': 'Change %',
            'volume': 'Volume'
        })
        
        st.dataframe(
            active_display,
            use_container_width=True,
            hide_index=True
        )


def display_crypto_tab(collector: CryptoCollector, limit: int):
    """Display crypto analysis"""
    
    col1, col2 = st.columns(2)
    
    # Top Gainers
    with col1:
        st.subheader("🚀 Top Gainers (24h)")
        gainers = collector.get_top_gainers(limit)
        
        if not gainers.empty:
            # Chart
            fig = px.scatter(
                gainers.head(15),
                x='market_cap',
                y='price_change_percentage_24h',
                size='total_volume',
                hover_name='name',
                color='price_change_percentage_24h',
                color_continuous_scale='Greens',
                title='Market Cap vs 24h Change',
                labels={
                    'market_cap': 'Market Cap ($)',
                    'price_change_percentage_24h': '24h Change (%)'
                }
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#fafafa'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Table
            gainers_display = gainers[['symbol', 'name', 'current_price', 'price_change_percentage_24h', 'total_volume']].head(10)
            gainers_display = gainers_display.copy()
            gainers_display['symbol'] = gainers_display['symbol'].str.upper()
            gainers_display['current_price'] = gainers_display['current_price'].apply(lambda x: f"${x:,.4f}" if x < 1 else f"${x:,.2f}")
            gainers_display['price_change_percentage_24h'] = gainers_display['price_change_percentage_24h'].apply(lambda x: f"{x:+.2f}%")
            gainers_display['total_volume'] = gainers_display['total_volume'].apply(lambda x: f"${x:,.0f}")
            gainers_display = gainers_display.rename(columns={
                'symbol': 'Symbol',
                'name': 'Name',
                'current_price': 'Price',
                'price_change_percentage_24h': '24h %',
                'total_volume': 'Volume ($)'
            })
            
            st.dataframe(gainers_display, use_container_width=True, hide_index=True)
    
    # Top Losers
    with col2:
        st.subheader("📉 Top Losers (24h)")
        losers = collector.get_top_losers(limit)
        
        if not losers.empty:
            # Table
            losers_display = losers[['symbol', 'name', 'current_price', 'price_change_percentage_24h']].head(10)
            losers_display = losers_display.copy()
            losers_display['symbol'] = losers_display['symbol'].str.upper()
            losers_display['current_price'] = losers_display['current_price'].apply(lambda x: f"${x:,.4f}" if x < 1 else f"${x:,.2f}")
            losers_display['price_change_percentage_24h'] = losers_display['price_change_percentage_24h'].apply(lambda x: f"{x:+.2f}%")
            losers_display = losers_display.rename(columns={
                'symbol': 'Symbol',
                'name': 'Name',
                'current_price': 'Price',
                'price_change_percentage_24h': '24h %'
            })
            
            st.dataframe(losers_display, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Trending
    st.subheader("🔥 Trending on CoinGecko")
    trending = collector.get_trending()
    
    if not trending.empty:
        col1, col2, col3 = st.columns(3)
        
        for idx, (_, row) in enumerate(trending.iterrows()):
            with [col1, col2, col3][idx % 3]:
                st.metric(
                    label=f"#{idx+1} {row['symbol'].upper()}",
                    value=row['name'][:15],
                    delta=f"Rank #{row['market_cap_rank']}" if row['market_cap_rank'] else "Unranked"
                )


def main():
    # Sidebar
    st.sidebar.title("📊 Flow Radar")
    st.sidebar.markdown("---")
    
    # Page selection
    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Overview", "📈 Stocks", "🚀 Crypto"],
        label_visibility="collapsed"
    )
    
    # Settings
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Settings")
    limit = st.sidebar.slider("Items to show", 5, 50, 15)
    
    # Auto-refresh
    auto_refresh = st.sidebar.checkbox("Auto-refresh (5 min)", value=False)
    if auto_refresh:
        st.sidebar.info("⏱️ Refreshing every 5 minutes")
        import time
        time.sleep(300)
        st.rerun()
    
    # Main content
    st.title("📊 Stock & Crypto Flow Radar")
    
    # Timestamp
    st.markdown(f"**Last updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")
    
    # Initialize collectors (with caching)
    @st.cache_resource
    def get_stock_collector():
        return StockCollector()
    
    @st.cache_resource
    def get_crypto_collector():
        return CryptoCollector()
    
    stock_collector = get_stock_collector()
    crypto_collector = get_crypto_collector()
    
    # Page content
    if page == "🏠 Overview":
        st.subheader("Welcome! 👋")
        st.markdown("""
        **Flow Radar** helps you detect where money is flowing right now.
        
        - 📈 **Stocks** - Top movers, unusual volume, most active
        - 🚀 **Crypto** - Gainers, losers, trending coins
        - 🐋 **Whale Tracking** (coming soon)
        - 📱 **Mobile-friendly** dashboard
        
        Use the sidebar to navigate!
        """)
        
        st.info("💡 **Tip:** Use auto-refresh to keep data up-to-date!")
        
    elif page == "📈 Stocks":
        with st.spinner("Loading stock data..."):
            display_stock_tab(stock_collector, limit)
    
    elif page == "🚀 Crypto":
        with st.spinner("Loading crypto data..."):
            display_crypto_tab(crypto_collector, limit)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        Made with ❤️ by Aiko & Michal | 
        <a href='https://github.com/MichalSy/stock-tracker' target='_blank'>GitHub</a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
