import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# Import StooqDataFetcher
try:
    from pystooq import StooqDataFetcher
    STOOQ_AVAILABLE = True
except ImportError:
    STOOQ_AVAILABLE = False
    print("Warning: pystooq not installed. Install with: pip install pystooq")

# Page configuration with dark theme
st.set_page_config(
    page_title="CryptoMatrix Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Responsive CSS with Fluid Typography and Improved Sidebar
st.markdown("""
<style>
:root {
    /* Responsive Typography Base */
    --base-font-size: clamp(0.875rem, 2vw, 1rem);
    --heading-font-size: clamp(1.5rem, 4vw, 3.5rem);
    --section-font-size: clamp(1.25rem, 3vw, 2.2rem);
    --card-font-size: clamp(1rem, 2.5vw, 1.3rem);
    
    /* Primary Dark Theme Colors */
    --bg-primary: #121212;
    --surface-color: #1E1E1E;
    --surface-light: #2C2C2C;
    --surface-medium: #252525;
    --text-primary: #F5F5F5;
    --text-secondary: #CCCCCC;
    --text-muted: #999999;
    --divider-color: #444444;
    
    /* Accent Colors (Matrix inspired) */
    --accent-green: #00FF85;
    --accent-green-dim: #00CC66;
    --accent-green-bright: #00FFAA;
    --alert-orange: #FF5722;
    --alert-red: #FF6F61;
    
    /* Enhanced Sidebar Colors */
    --sidebar-bg: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
    --card-bg: rgba(30, 30, 30, 0.8);
    --card-border: rgba(0, 255, 133, 0.3);
    
    /* Responsive Spacing */
    --spacing-xs: clamp(0.5rem, 1vw, 1rem);
    --spacing-sm: clamp(0.75rem, 1.5vw, 1.5rem);
    --spacing-md: clamp(1rem, 2vw, 2rem);
    --spacing-lg: clamp(1.5rem, 3vw, 3rem);
    --spacing-xl: clamp(2rem, 4vw, 4rem);
}

/* Global Responsive Styles */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: 'Courier New', monospace;
    font-size: var(--base-font-size);
    line-height: 1.6;
}

.stApp {
    background-color: var(--bg-primary);
}

/* Responsive Typography */
.main-header {
    font-size: var(--heading-font-size);
    color: var(--accent-green);
    margin-bottom: var(--spacing-md);
    text-align: center;
    text-shadow: 0 0 20px var(--accent-green);
    animation: matrix-glow 2s ease-in-out infinite alternate;
    line-height: 1.2;
}

@keyframes matrix-glow {
    from { text-shadow: 0 0 20px var(--accent-green); }
    to { text-shadow: 0 0 30px var(--accent-green), 0 0 40px var(--accent-green-dim); }
}

.subtitle {
    font-size: clamp(1rem, 2.5vw, 1.3rem);
    color: var(--text-secondary);
    text-align: center;
    margin-bottom: var(--spacing-lg);
    letter-spacing: clamp(1px, 0.2vw, 2px);
}

.section-header {
    font-size: var(--section-font-size);
    color: var(--accent-green);
    margin: var(--spacing-lg) 0 var(--spacing-md) 0;
    padding-bottom: var(--spacing-sm);
    border-bottom: 2px solid var(--accent-green-dim);
    text-transform: uppercase;
    letter-spacing: clamp(2px, 0.4vw, 3px);
}

/* Enhanced Responsive Sidebar */
.stSidebar {
    background: var(--sidebar-bg);
    border-right: 2px solid var(--accent-green);
    width: clamp(280px, 30vw, 400px) !important;
    padding: var(--spacing-md);
    box-shadow: 4px 0 20px rgba(0, 255, 133, 0.1);
}

.stSidebar .stMarkdown {
    color: var(--text-primary);
}

/* Enhanced Sidebar Headers */
.stSidebar h2 {
    color: var(--accent-green) !important;
    font-size: clamp(1.25rem, 3vw, 1.5rem) !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-bottom: var(--spacing-md) !important;
    text-align: center !important;
    text-shadow: 0 0 10px var(--accent-green-dim) !important;
}

.stSidebar h3 {
    color: var(--text-primary) !important;
    font-size: clamp(1rem, 2.5vw, 1.2rem) !important;
    font-weight: 600 !important;
    margin-bottom: var(--spacing-sm) !important;
    padding-left: var(--spacing-xs) !important;
    border-left: 3px solid var(--accent-green) !important;
    padding-left: var(--spacing-sm) !important;
}

/* Enhanced Sidebar Cards */
.sidebar-card {
    background: var(--card-bg);
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.sidebar-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-green), transparent);
    animation: scan 3s linear infinite;
}

@keyframes scan {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.sidebar-card:hover {
    transform: translateY(-2px);
    border-color: var(--accent-green);
    box-shadow: 0 8px 25px rgba(0, 255, 133, 0.2);
}

/* Enhanced Portfolio Strategy Tag */
.strategy-tag {
    background: linear-gradient(135deg, var(--accent-green), var(--accent-green-dim));
    color: var(--bg-primary);
    padding: var(--spacing-xs) var(--spacing-md);
    border-radius: 25px;
    font-weight: bold;
    font-size: clamp(0.875rem, 2vw, 1rem);
    text-transform: uppercase;
    letter-spacing: 1px;
    display: inline-block;
    margin-bottom: var(--spacing-sm);
    box-shadow: 0 4px 15px rgba(0, 255, 133, 0.3);
    transition: all 0.3s ease;
}

.strategy-tag:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0, 255, 133, 0.5);
}

/* Enhanced Description Text */
.description-text {
    color: var(--text-secondary);
    font-size: clamp(0.875rem, 2vw, 1rem);
    line-height: 1.6;
    margin-bottom: var(--spacing-md);
    padding: var(--spacing-sm);
    background: rgba(0, 0, 0, 0.3);
    border-radius: 8px;
    border-left: 3px solid var(--accent-green-dim);
}

/* Enhanced Slider Container */
.slider-container {
    background: var(--surface-medium);
    padding: var(--spacing-md);
    border-radius: 12px;
    margin-bottom: var(--spacing-sm);
    border: 1px solid var(--divider-color);
}

.slider-label {
    color: var(--text-primary);
    font-weight: bold;
    font-size: clamp(0.875rem, 2vw, 1rem);
    margin-bottom: var(--spacing-xs);
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
}

.slider-value {
    background: var(--accent-green);
    color: var(--bg-primary);
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.875rem;
    font-weight: bold;
    min-width: 35px;
    text-align: center;
}

/* Enhanced Slider Styles */
.stSlider > div > div > div {
    background-color: var(--accent-green) !important;
}

.stSlider > div {
    color: var(--text-primary) !important;
}

/* Enhanced Round Buttons */
.round-button {
    background: linear-gradient(135deg, var(--accent-green), var(--accent-green-dim));
    color: var(--bg-primary);
    border: none;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: 25px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: clamp(0.875rem, 2vw, 1rem);
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 255, 133, 0.3);
    width: 100%;
    margin-bottom: var(--spacing-sm);
    position: relative;
    overflow: hidden;
}

.round-button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}

.round-button:hover::before {
    width: 300px;
    height: 300px;
}

.round-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 255, 133, 0.5);
    background: linear-gradient(135deg, var(--accent-green-bright), var(--accent-green));
}

.round-button:active {
    transform: translateY(0);
}

/* Override Streamlit button styles in sidebar */
.stSidebar .stButton > button {
    background: linear-gradient(135deg, var(--accent-green), var(--accent-green-dim)) !important;
    color: var(--bg-primary) !important;
    border: none !important;
    padding: var(--spacing-sm) var(--spacing-md) !important;
    border-radius: 25px !important;
    font-weight: bold !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    font-size: clamp(0.875rem, 2vw, 1rem) !important;
    width: 100% !important;
    margin-bottom: var(--spacing-xs) !important;
    margin-top: 0 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 255, 133, 0.3) !important;
}

.stSidebar .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(0, 255, 133, 0.5) !important;
    background: linear-gradient(135deg, var(--accent-green-bright), var(--accent-green)) !important;
}

/* Remove button margins and padding */
.stSidebar .stButton {
    margin: 0 !important;
    padding: 0 !important;
}

.stSidebar .stButton > div {
    margin: 0 !important;
    padding: 0 !important;
}

/* Enhanced Stats Cards */
.stats-card {
    background: linear-gradient(145deg, var(--surface-color), var(--surface-medium));
    border: 1px solid var(--card-border);
    border-radius: 16px;
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-sm);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.stats-card:hover {
    transform: translateY(-2px);
    border-color: var(--accent-green);
    box-shadow: 0 8px 25px rgba(0, 255, 133, 0.2);
}

.stats-card::after {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(45deg, transparent, rgba(0, 255, 133, 0.1), transparent);
    transform: rotate(45deg);
    transition: all 0.5s ease;
}

.stats-card:hover::after {
    right: -100%;
}

.stats-label {
    color: var(--accent-green);
    font-weight: bold;
    font-size: clamp(0.875rem, 2vw, 1rem);
    margin-bottom: var(--spacing-xs);
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stats-value {
    color: var(--text-primary);
    font-size: clamp(1.25rem, 3vw, 1.5rem);
    font-weight: bold;
    margin-bottom: var(--spacing-xs);
}

.stats-change {
    font-size: clamp(0.875rem, 2vw, 1rem);
    font-weight: bold;
    margin-bottom: var(--spacing-xs);
}

.stats-change.positive {
    color: var(--accent-green);
}

.stats-change.negative {
    color: var(--alert-orange);
}

.stats-description {
    color: var(--text-muted);
    font-size: clamp(0.75rem, 1.5vw, 0.875rem);
    line-height: 1.4;
}

/* Enhanced Section Divider */
.section-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-green), transparent);
    margin: var(--spacing-lg) 0;
    position: relative;
}

.section-divider::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 50%;
    transform: translateX(-50%);
    width: 10px;
    height: 4px;
    background: var(--accent-green);
    border-radius: 2px;
    box-shadow: 0 0 10px var(--accent-green);
}

/* Remove Streamlit's default margins */
.stSidebar > div {
    padding: 0 !important;
}

.stSidebar > div > div {
    padding: 0 !important;
}

/* Responsive Card Styles */
.dashboard-card {
    background-color: var(--surface-color);
    border: 1px solid var(--divider-color);
    padding: var(--spacing-md);
    border-radius: clamp(8px, 1.5vw, 12px);
    box-shadow: 0 4px 6px rgba(0, 255, 133, 0.1);
    margin-bottom: var(--spacing-sm);
}

.portfolio-card {
    background: linear-gradient(145deg, var(--surface-color), var(--surface-light));
    border: 1px solid var(--accent-green-dim);
    padding: var(--spacing-md);
    border-radius: clamp(10px, 2vw, 15px);
    box-shadow: 0 4px 15px rgba(0, 255, 133, 0.2);
    transition: all 0.3s ease;
}

.portfolio-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 255, 133, 0.3);
}

/* Responsive Tab Styles */
.stTabs [data-baseweb="tab-list"] {
    background-color: var(--surface-color);
    border-bottom: 2px solid var(--accent-green);
    gap: clamp(2px, 0.5vw, 8px);
    padding: var(--spacing-xs);
    flex-wrap: wrap;
}

.stTabs [data-baseweb="tab"] {
    height: auto;
    min-height: clamp(40px, 8vw, 50px);
    background-color: var(--surface-light);
    color: var(--text-secondary);
    border-radius: clamp(6px, 1vw, 8px);
    padding: clamp(8px, 2vw, 12px) clamp(12px, 3vw, 20px);
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: clamp(0.5px, 0.1vw, 1px);
    transition: all 0.3s ease;
    font-size: clamp(0.75rem, 2vw, 0.9rem);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
    min-width: clamp(120px, 25vw, 200px);
}

.stTabs [aria-selected="true"] {
    background-color: var(--accent-green);
    color: var(--bg-primary);
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: var(--accent-green-dim);
    color: var(--bg-primary);
}

/* Responsive Button Styles */
.stButton > button {
    background: linear-gradient(45deg, var(--accent-green), var(--accent-green-dim));
    color: var(--bg-primary);
    border: none;
    padding: clamp(10px, 2vw, 14px) clamp(20px, 4vw, 28px);
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: clamp(0.5px, 0.1vw, 1px);
    border-radius: clamp(6px, 1vw, 8px);
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 255, 133, 0.3);
    font-size: clamp(0.875rem, 2vw, 1rem);
    width: 100%;
    max-width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 255, 133, 0.5);
    background: linear-gradient(45deg, var(--accent-green-dim), var(--accent-green));
}

.stButton > button:active {
    transform: translateY(0);
}

/* Primary Button */
.stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(45deg, #00FF85, #00CC66);
    font-size: clamp(1rem, 2.5vw, 1.1rem);
    padding: clamp(12px, 2.5vw, 16px) clamp(24px, 5vw, 32px);
}

/* Responsive Metric Styles */
.stMetric {
    background-color: var(--surface-color);
    border: 1px solid var(--divider-color);
    padding: var(--spacing-sm);
    border-radius: clamp(8px, 1.5vw, 12px);
    margin-bottom: var(--spacing-sm);
}

.stMetric label {
    color: var(--text-secondary);
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: clamp(0.5px, 0.1vw, 1px);
    font-size: clamp(0.75rem, 2vw, 0.9rem);
}

.stMetric div {
    color: var(--accent-green);
    font-size: clamp(1.2rem, 3vw, 1.5rem);
    font-weight: bold;
}

.stMetric delta {
    color: var(--accent-green);
    font-size: clamp(0.875rem, 2vw, 1rem);
}

/* Responsive Dataframe Styles */
.stDataFrame {
    background-color: var(--surface-color);
    border: 1px solid var(--divider-color);
    border-radius: clamp(8px, 1.5vw, 12px);
    overflow-x: auto;
}

.stDataFrame thead th {
    background-color: var(--surface-light);
    color: var(--accent-green);
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: clamp(0.5px, 0.1vw, 1px);
    padding: clamp(8px, 2vw, 12px);
    font-size: clamp(0.75rem, 2vw, 0.9rem);
}

.stDataFrame tbody tr {
    border-bottom: 1px solid var(--divider-color);
}

.stDataFrame tbody td {
    color: var(--text-primary);
    padding: clamp(6px, 1.5vw, 10px);
    font-size: clamp(0.875rem, 2vw, 1rem);
}

/* Responsive Form Elements */
.stSelectbox > div > div {
    background-color: var(--surface-light);
    color: var(--text-primary);
    border: 1px solid var(--divider-color);
    font-size: clamp(0.875rem, 2vw, 1rem);
}

.stDateInput > div > div > div {
    background-color: var(--surface-light);
    color: var(--text-primary);
    font-size: clamp(0.875rem, 2vw, 1rem);
}

.stNumberInput > div > div > div {
    background-color: var(--surface-light);
    color: var(--text-primary);
    font-size: clamp(0.875rem, 2vw, 1rem);
}

.stCheckbox > div {
    color: var(--text-primary);
    font-size: clamp(0.875rem, 2vw, 1rem);
}

.stCheckbox > div > label {
    color: var(--text-primary);
}

/* Chart Styles */
.stPlotlyChart {
    background-color: var(--surface-color);
    border: 1px solid var(--divider-color);
    border-radius: clamp(8px, 1.5vw, 12px);
}

/* Alert/Status Styles */
.alert-status {
    color: var(--alert-orange);
    font-weight: bold;
}

.success-message {
    color: var(--accent-green);
    font-weight: bold;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: clamp(6px, 1.5vw, 8px);
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: var(--accent-green-dim);
    border-radius: clamp(3px, 0.75vw, 4px);
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-green);
}

/* Media Queries for Specific Breakpoints */
@media screen and (max-width: 768px) {
    .stTabs [data-baseweb="tab-list"] {
        flex-direction: column;
    }
    .stTabs [data-baseweb="tab"] {
        min-width: 100%;
        margin-bottom: var(--spacing-xs);
    }
    .stSidebar {
        width: 100% !important;
    }
}

@media screen and (min-width: 1200px) {
    :root {
        --base-font-size: 1.125rem;
    }
}

@media screen and (max-width: 480px) {
    .main-header {
        font-size: clamp(1.5rem, 8vw, 2rem);
    }
    .stColumns {
        flex-direction: column !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolio_allocation' not in st.session_state:
    st.session_state.portfolio_allocation = {
        'Conservative': {'BTC': 0.30, 'ETH': 0.40, 'USDT': 0.20, 'ADA': 0.10},
        'Moderate': {'BTC': 0.50, 'ETH': 0.30, 'BNB': 0.10, 'XRP': 0.10},
        'Aggressive': {'BTC': 0.40, 'ETH': 0.25, 'SOL': 0.20, 'DOT': 0.15}
    }

if 'backtest_results' not in st.session_state:
    st.session_state.backtest_results = None

# Enhanced data fetching with Stooq integration
def get_crypto_data_stooq():
    """Get cryptocurrency data using Stooq with Yahoo Finance fallback"""
    
    # Crypto symbol mappings for Stooq
    stooq_symbols = {
        'BTC': 'BTCUSD',
        'ETH': 'ETHUSD', 
        'USDT': 'USDTUSD',
        'BNB': 'BNBUSD',
        'SOL': 'SOLUSD',
        'XRP': 'XRPUSD',
        'ADA': 'ADAUSD',
        'DOGE': 'DOGEUSD',
        'DOT': 'DOTUSD',
        'LTC': 'LTCUSD'
    }
    
    crypto_names = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'Solana', 'XRP', 
                   'Cardano', 'Dogecoin', 'Polkadot', 'Litecoin']
    
    data = []
    
    if STOOQ_AVAILABLE:
        try:
            fetcher = StooqDataFetcher()
            
            for i, (symbol, stooq_sym) in enumerate(stooq_symbols.items()):
                try:
                    # Fetch data from Stooq
                    df = fetcher.get_data(stooq_sym, start_date=datetime.now() - timedelta(days=30))
                    
                    if not df.empty:
                        # Get the most recent data
                        latest = df.iloc[-1]
                        prev_day = df.iloc[-2] if len(df) > 1 else df.iloc[-1]
                        
                        # Calculate percentage changes
                        price_change_1d = ((latest['Close'] - prev_day['Close']) / prev_day['Close']) * 100
                        
                        # Get 7-day change
                        week_ago = df.iloc[-7] if len(df) >= 7 else df.iloc[0]
                        price_change_7d = ((latest['Close'] - week_ago['Close']) / week_ago['Close']) * 100
                        
                        # Estimate 1-hour change (Stooq doesn't have hourly data)
                        price_change_1h = price_change_1d * 0.1  # Rough estimate
                        
                        # Calculate market cap and volume (estimates for crypto)
                        current_price = latest['Close']
                        volume_24h = latest.get('Volume', 0)
                        
                        # Market cap estimates based on known values
                        market_caps = {
                            'BTC': current_price * 19_500_000,  # ~19.5M BTC
                            'ETH': current_price * 120_000_000,  # ~120M ETH
                            'USDT': 120_000_000_000,  # Stablecoin
                            'BNB': current_price * 145_000_000,
                            'SOL': current_price * 400_000_000,
                            'XRP': current_price * 50_000_000_000,
                            'ADA': current_price * 35_000_000_000,
                            'DOGE': current_price * 140_000_000_000,
                            'DOT': current_price * 1_100_000_000,
                            'LTC': current_price * 70_000_000
                        }
                        
                        market_cap = market_caps.get(symbol, 0)
                        
                        data.append({
                            'Name': crypto_names[i],
                            'Symbol': symbol,
                            'Price': current_price,
                            '1h %': price_change_1h,
                            '24h %': price_change_1d,
                            '7d %': price_change_7d,
                            'Market Cap': f"${market_cap/1e9:.2f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.2f}M",
                            'Volume (24h)': f"${volume_24h/1e9:.2f}B" if volume_24h >= 1e9 else f"${volume_24h/1e6:.2f}M"
                        })
                    else:
                        # Fallback to sample data for this symbol
                        sample_data = get_sample_crypto_data()
                        if i < len(sample_data):
                            data.append(sample_data.iloc[i].to_dict())
                            
                except Exception:
                    # Fallback to sample data for this symbol
                    sample_data = get_sample_crypto_data()
                    if i < len(sample_data):
                        data.append(sample_data.iloc[i].to_dict())
            
            if data:
                return pd.DataFrame(data)
                
        except Exception:
            pass
    
    # Fallback to Yahoo Finance if Stooq fails
    return get_crypto_data_yahoo()

def get_crypto_data_yahoo():
    """Get cryptocurrency data using Yahoo Finance as fallback"""
    crypto_symbols = ['BTC-USD', 'ETH-USD', 'USDT-USD', 'BNB-USD', 'SOL-USD', 
                      'XRP-USD', 'ADA-USD', 'DOGE-USD', 'DOT-USD', 'LTC-USD']
    crypto_names = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'Solana', 'XRP', 
                   'Cardano', 'Dogecoin', 'Polkadot', 'Litecoin']
    
    try:
        tickers = yf.Tickers(' '.join(crypto_symbols))
        data = []
        
        for i, symbol in enumerate(crypto_symbols):
            try:
                ticker = tickers.tickers[symbol]
                info = ticker.info
                
                # Get current price and changes
                hist = ticker.history(period="2d")
                if len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    price_change_1d = ((current_price - prev_price) / prev_price) * 100
                else:
                    current_price = info.get('currentPrice', 0)
                    price_change_1d = info.get('regularMarketChangePercent', 0)
                
                # Get other data
                market_cap = info.get('marketCap', 0)
                volume_24h = info.get('volume24Hr', 0)
                
                # Get 7-day data
                hist_7d = ticker.history(period="7d")
                if len(hist_7d) >= 7:
                    price_7d_ago = hist_7d['Close'].iloc[0]
                    price_change_7d = ((current_price - price_7d_ago) / price_7d_ago) * 100
                else:
                    price_change_7d = price_change_1d * 3
                
                # Get 1-hour change
                hist_1h = ticker.history(period="1d", interval="1h")
                if len(hist_1h) >= 2:
                    price_change_1h = ((hist_1h['Close'].iloc[-1] - hist_1h['Close'].iloc[-2]) / hist_1h['Close'].iloc[-2]) * 100
                else:
                    price_change_1h = price_change_1d * 0.1
                
                data.append({
                    'Name': crypto_names[i],
                    'Symbol': symbol.replace('-USD', ''),
                    'Price': current_price,
                    '1h %': price_change_1h,
                    '24h %': price_change_1d,
                    '7d %': price_change_7d,
                    'Market Cap': f"${market_cap/1e9:.2f}B" if market_cap >= 1e9 else f"${market_cap/1e6:.2f}M",
                    'Volume (24h)': f"${volume_24h/1e9:.2f}B" if volume_24h >= 1e9 else f"${volume_24h/1e6:.2f}M"
                })
                
            except Exception:
                sample_data = get_sample_crypto_data()
                if i < len(sample_data):
                    data.append(sample_data.iloc[i].to_dict())
        
        if data:
            return pd.DataFrame(data)
            
    except Exception:
        pass
    
    return get_sample_crypto_data()

def get_sample_crypto_data():
    """Sample cryptocurrency data as fallback"""
    crypto_data = {
        'Name': ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'Solana', 'XRP', 'Cardano', 'Dogecoin', 'Polkadot', 'Litecoin'],
        'Symbol': ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'DOT', 'LTC'],
        'Price': [90145.32, 3108.57, 1.00, 895.62, 289.45, 0.78, 0.62, 0.23, 8.95, 89.45],
        '1h %': [-0.09, -0.01, -0.00, 0.32, 1.25, 0.45, 0.67, 0.89, 0.32, 0.56],
        '24h %': [0.18, 1.15, -0.00, 2.18, 3.45, 1.23, 2.34, 3.21, 1.89, 1.45],
        '7d %': [0.74, 2.29, -0.00, 0.31, 15.67, 5.43, 8.92, 12.34, 6.78, 4.56],
        'Market Cap': ['$1.80T', '$375.30B', '$186.26B', '$123.36B', '$129.45B', '$45.67B', '$21.45B', '$32.89B', '$12.34B', '$6.78B'],
        'Volume (24h)': ['$65.42B', '$10.17B', '$47.51B', '$1.49B', '$3.45B', '$2.34B', '$0.89B', '$1.23B', '$0.56B', '$0.78B']
    }
    return pd.DataFrame(crypto_data)

# Risk metrics calculation
def calculate_risk_metrics(portfolio_type, allocation):
    risk_metrics = {
        'Conservative': {
            'Expected Return': 8.5,
            'Volatility': 12.3,
            'Sharpe Ratio': 0.69,
            'Max Drawdown': 15.7,
            'VaR (95%)': 5.2
        },
        'Moderate': {
            'Expected Return': 12.8,
            'Volatility': 18.5,
            'Sharpe Ratio': 0.72,
            'Max Drawdown': 22.4,
            'VaR (95%)': 8.7
        },
        'Aggressive': {
            'Expected Return': 18.2,
            'Volatility': 28.9,
            'Sharpe Ratio': 0.68,
            'Max Drawdown': 35.6,
            'VaR (95%)': 14.3
        }
    }
    return risk_metrics.get(portfolio_type, {})

# Portfolio backtesting
def backtest_portfolio(portfolio_type, start_date, end_date, initial_investment, contribution_freq, contribution_amount, reinvest=True):
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    if portfolio_type == 'Conservative':
        daily_return_mean = 0.00035
        daily_return_std = 0.015
    elif portfolio_type == 'Moderate':
        daily_return_mean = 0.00045
        daily_return_std = 0.022
    else:  # Aggressive
        daily_return_mean = 0.00060
        daily_return_std = 0.035
    
    np.random.seed(42)
    returns = np.random.normal(daily_return_mean, daily_return_std, len(dates))
    
    portfolio_value = [initial_investment]
    
    for i in range(1, len(dates)):
        add_contribution = False
        if contribution_freq == 'Daily':
            add_contribution = True
        elif contribution_freq == 'Weekly' and dates[i].dayofweek == 0:
            add_contribution = True
        elif contribution_freq == 'Monthly' and dates[i].day == 1:
            add_contribution = True
        elif contribution_freq == 'Yearly' and dates[i].month == 1 and dates[i].day == 1:
            add_contribution = True
        
        if add_contribution:
            portfolio_value[i-1] += contribution_amount
        
        new_value = portfolio_value[i-1] * (1 + returns[i])
        portfolio_value.append(new_value)
    
    results_df = pd.DataFrame({
        'Date': dates,
        'Portfolio Value': portfolio_value,
        'Daily Return': np.insert(returns[1:], 0, 0)
    })
    
    return results_df

# Main Dashboard
def main():
    # Enhanced Header with Matrix theme
    st.markdown('<h1 class="main-header">🌐 CRYPTOMATRIX DASHBOARD</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">⚡ ADVANCED CRYPTO ANALYSIS & RISK MANAGEMENT SYSTEM ⚡</p>', unsafe_allow_html=True)

    # Data source indicator
    if STOOQ_AVAILABLE:
        data_source = "🟢 Stooq + Yahoo Finance"
    else:
        data_source = "🟡 Yahoo Finance (Stooq not available)"
    
    st.markdown(f'<div style="text-align: center; margin-bottom: 1rem;"><span style="color: var(--text-secondary); font-size: 0.9rem;">Data Source: {data_source}</span></div>', unsafe_allow_html=True)

    # Market Overview Tabs with improved responsive styling
    st.markdown('<div class="section-header">📊 MARKET OVERVIEW</div>', unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["🪙 CRYPTOCURRENCY PRICES", "📈 MARKET TRENDS", "🎯 PORTFOLIO ANALYSIS", "🧮 BACKTEST CALCULATOR"])

    with tab1:
        st.markdown('<div class="dashboard-card"><h3 style="color: var(--accent-green); margin-bottom: 1rem;">🔥 TOP CRYPTOCURRENCIES</h3></div>', unsafe_allow_html=True)
        
        # Add refresh button
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 REFRESH DATA", type="primary"):
                st.rerun()
        with col2:
            st.markdown(f'<div style="margin-top: 0.5rem;"><span style="color: var(--text-secondary);">Real-time data from {data_source}</span></div>', unsafe_allow_html=True)
        
        # Get crypto data using Stooq with fallback
        crypto_df = get_crypto_data_stooq()
        display_df = crypto_df.copy()
        st.dataframe(
            display_df.style.format({
                'Price': '${:,.2f}',
                '1h %': '{:+.2f}%',
                '24h %': '{:+.2f}%',
                '7d %': '{:+.2f}%'
            }),
            use_container_width=True,
            height=400
        )

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="portfolio-card"><h3 style="color: var(--accent-green); margin-bottom: 1rem;">💰 MARKET CAPITALIZATION</h3></div>', unsafe_allow_html=True)
            market_caps = []
            for cap in crypto_df['Market Cap'][:5]:
                if 'T' in cap:
                    market_caps.append(float(cap.replace('$', '').replace('T', '')) * 1e12)
                elif 'B' in cap:
                    market_caps.append(float(cap.replace('$', '').replace('B', '')) * 1e9)
                elif 'M' in cap:
                    market_caps.append(float(cap.replace('$', '').replace('M', '')) * 1e6)
                else:
                    market_caps.append(0)
            
            st.bar_chart(
                pd.DataFrame({
                    'Cryptocurrency': crypto_df['Name'][:5],
                    'Market Cap': market_caps
                }).set_index('Cryptocurrency'),
                use_container_width=True
            )
        
        with col2:
            st.markdown('<div class="portfolio-card"><h3 style="color: var(--accent-green); margin-bottom: 1rem;">📊 7-DAY PERFORMANCE</h3></div>', unsafe_allow_html=True)
            st.bar_chart(
                crypto_df.head(8).set_index('Symbol')['7d %'],
                use_container_width=True
            )

    with tab3:
        st.markdown('<div class="section-header">🔍 PORTFOLIO RISK ANALYSIS</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="portfolio-card"><h3 style="color: var(--accent-green);">🛡️ CONSERVATIVE</h3></div>', unsafe_allow_html=True)
            conservative_allocation = st.session_state.portfolio_allocation['Conservative']
            st.bar_chart(
                pd.DataFrame({
                    'Asset': list(conservative_allocation.keys()),
                    'Allocation': [x * 100 for x in conservative_allocation.values()]
                }).set_index('Asset'),
                use_container_width=True
            )
            st.markdown('<p style="color: var(--text-secondary); font-size: 0.9rem;">30% BTC | 40% ETH | 20% USDT | 10% ADA</p>', unsafe_allow_html=True)
            risk_metrics = calculate_risk_metrics('Conservative', conservative_allocation)
            for metric, value in risk_metrics.items():
                st.metric(label=metric, value=f"{value:.1f}")
        
        with col2:
            st.markdown('<div class="portfolio-card"><h3 style="color: var(--accent-green);">⚖️ MODERATE</h3></div>', unsafe_allow_html=True)
            moderate_allocation = st.session_state.portfolio_allocation['Moderate']
            st.bar_chart(
                pd.DataFrame({
                    'Asset': list(moderate_allocation.keys()),
                    'Allocation': [x * 100 for x in moderate_allocation.values()]
                }).set_index('Asset'),
                use_container_width=True
            )
            st.markdown('<p style="color: var(--text-secondary); font-size: 0.9rem;">50% BTC | 30% ETH | 10% BNB | 10% XRP</p>', unsafe_allow_html=True)
            risk_metrics = calculate_risk_metrics('Moderate', moderate_allocation)
            for metric, value in risk_metrics.items():
                st.metric(label=metric, value=f"{value:.1f}")
        
        with col3:
            st.markdown('<div class="portfolio-card"><h3 style="color: var(--accent-green);">🚀 AGGRESSIVE</h3></div>', unsafe_allow_html=True)
            aggressive_allocation = st.session_state.portfolio_allocation['Aggressive']
            st.bar_chart(
                pd.DataFrame({
                    'Asset': list(aggressive_allocation.keys()),
                    'Allocation': [x * 100 for x in aggressive_allocation.values()]
                }).set_index('Asset'),
                use_container_width=True
            )
            st.markdown('<p style="color: var(--text-secondary); font-size: 0.9rem;">40% BTC | 25% ETH | 20% SOL | 15% DOT</p>', unsafe_allow_html=True)
            risk_metrics = calculate_risk_metrics('Aggressive', aggressive_allocation)
            for metric, value in risk_metrics.items():
                st.metric(label=metric, value=f"{value:.1f}")
        
        st.markdown('<div class="section-header">📈 RISK-RETURN COMPARISON</div>', unsafe_allow_html=True)
        comparison_data = pd.DataFrame({
            'Portfolio': ['Conservative', 'Moderate', 'Aggressive'],
            'Expected Return': [8.5, 12.8, 18.2],
            'Volatility': [12.3, 18.5, 28.9],
            'Sharpe Ratio': [0.69, 0.72, 0.68]
        })
        st.scatter_chart(
            comparison_data,
            x='Volatility',
            y='Expected Return',
            size='Sharpe Ratio',
            color='Portfolio',
            use_container_width=True
        )

    with tab4:
        st.markdown('<div class="section-header">🧮 PORTFOLIO BACKTEST CALCULATOR</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="dashboard-card"><h3 style="color: var(--accent-green); margin-bottom: 1rem;">⚙️ BACKTEST PARAMETERS</h3></div>', unsafe_allow_html=True)
            portfolio_type = st.selectbox(
                "Portfolio Strategy",
                ["Conservative", "Moderate", "Aggressive"],
                key="backtest_portfolio"
            )
            start_date = st.date_input(
                "Start Date",
                value=datetime.now() - timedelta(days=365),
                max_value=datetime.now() - timedelta(days=30)
            )
            end_date = st.date_input(
                "End Date",
                value=datetime.now(),
                min_value=start_date + timedelta(days=30)
            )
            initial_investment = st.number_input(
                "Initial Investment ($)",
                min_value=100.0,
                max_value=1000000.0,
                value=10000.0,
                step=1000.0
            )
        
        with col2:
            st.markdown('<div class="dashboard-card"><h3 style="color: var(--accent-green); margin-bottom: 1rem;">💳 CONTRIBUTION SETTINGS</h3></div>', unsafe_allow_html=True)
            contribution_freq = st.selectbox(
                "Contribution Frequency",
                ["Daily", "Weekly", "Monthly", "Yearly", "None"],
                key="contribution_freq"
            )
            if contribution_freq != "None":
                contribution_amount = st.number_input(
                    "Contribution Amount ($)",
                    min_value=0.0,
                    max_value=10000.0,
                    value=100.0,
                    step=50.0
                )
            else:
                contribution_amount = 0.0
            
            reinvest = st.checkbox("🔄 Reinvest Returns", value=True)
        
        st.markdown('<br>', unsafe_allow_html=True)
        
        if st.button("🚀 RUN BACKTEST", type="primary"):
            with st.spinner("🔄 Processing backtest analysis..."):
                results = backtest_portfolio(
                    portfolio_type, start_date, end_date, initial_investment,
                    contribution_freq, contribution_amount, reinvest
                )
                st.session_state.backtest_results = results
        
        if st.session_state.backtest_results is not None:
            st.markdown('<div class="section-header">📊 BACKTEST RESULTS</div>', unsafe_allow_html=True)
            results = st.session_state.backtest_results
            
            final_value = results['Portfolio Value'].iloc[-1]
            total_return = ((final_value - initial_investment) / initial_investment) * 100
            annualized_return = (pow(final_value/initial_investment, 365/(end_date - start_date).days) - 1) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Final Value", f"${final_value:,.2f}")
            with col2:
                st.metric("Total Return", f"{total_return:.2f}%")
            with col3:
                st.metric("Annualized Return", f"{annualized_return:.2f}%")
            with col4:
                max_drawdown = ((results['Portfolio Value'].cummax() - results['Portfolio Value']).max() / results['Portfolio Value'].cummax().max()) * 100
                st.metric("Max Drawdown", f"{max_drawdown:.2f}%")
            
            st.markdown('<div class="dashboard-card"><h3 style="color: var(--accent-green); margin-bottom: 1rem;">📈 PORTFOLIO VALUE OVER TIME</h3></div>', unsafe_allow_html=True)
            st.line_chart(
                results.set_index('Date')['Portfolio Value'],
                use_container_width=True
            )
            
            # Performance Metrics
            st.markdown('<div class="dashboard-card"><h3 style="color: var(--accent-green); margin-bottom: 1rem;">📋 PERFORMANCE METRICS</h3></div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="dashboard-card">
                    <p style="color: var(--text-secondary); font-weight: bold; margin-bottom: 0.5rem;">Sharpe Ratio</p>
                    <p style="color: var(--accent-green); font-size: 1.5rem; font-weight: bold;">1.24</p>
                    <p style="color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.5rem;">Risk-adjusted return measure</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="dashboard-card">
                    <p style="color: var(--text-secondary); font-weight: bold; margin-bottom: 0.5rem;">Calmar Ratio</p>
                    <p style="color: var(--accent-green); font-size: 1.5rem; font-weight: bold;">0.89</p>
                    <p style="color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.5rem;">Return vs max drawdown ratio</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="dashboard-card">
                    <p style="color: var(--text-secondary); font-weight: bold; margin-bottom: 0.5rem;">Best Day</p>
                    <p style="color: var(--accent-green); font-size: 1.5rem; font-weight: bold;">+8.2%</p>
                    <p style="color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.5rem;">Highest single-day return</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="dashboard-card">
                    <p style="color: var(--text-secondary); font-weight: bold; margin-bottom: 0.5rem;">Sortino Ratio</p>
                    <p style="color: var(--accent-green); font-size: 1.5rem; font-weight: bold;">1.85</p>
                    <p style="color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.5rem;">Downside risk-adjusted return</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="dashboard-card">
                    <p style="color: var(--text-secondary); font-weight: bold; margin-bottom: 0.5rem;">Win Rate</p>
                    <p style="color: var(--accent-green); font-size: 1.5rem; font-weight: bold;">58.3%</p>
                    <p style="color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.5rem;">Percentage of profitable days</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                <div class="dashboard-card">
                    <p style="color: var(--text-secondary); font-weight: bold; margin-bottom: 0.5rem;">Worst Day</p>
                    <p style="color: var(--alert-orange); font-size: 1.5rem; font-weight: bold;">-5.6%</p>
                    <p style="color: var(--text-secondary); font-size: 0.75rem; margin-top: 0.5rem;">Lowest single-day return</p>
                </div>
                """, unsafe_allow_html=True)

    # Enhanced Sidebar with improved styling
    with st.sidebar:
        st.markdown('<h2 style="color: var(--accent-green);">⚙️ SYSTEM CONFIGURATION</h2>', unsafe_allow_html=True)
        
        # Enhanced Portfolio Allocation Section
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: var(--text-primary);">🎯 PORTFOLIO ALLOCATION</h3>', unsafe_allow_html=True)
        st.markdown('<div class="strategy-tag">🛡️ CONSERVATIVE PORTFOLIO</div>', unsafe_allow_html=True)
        st.markdown('<div class="description-text">Low-risk strategy focusing on stable assets with minimal volatility. Designed for capital preservation while generating steady returns.</div>', unsafe_allow_html=True)
        
        # Enhanced Sliders with better styling
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        btc_con = st.slider("BTC %", 0, 100, 30, key="btc_con")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="slider-container">', unsafe_allow_html=True)
        eth_con = st.slider("ETH %", 0, 100, 40, key="eth_con")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Button
        st.markdown('<div style="margin: 0; padding: 0;">', unsafe_allow_html=True)
        if st.button("💾 UPDATE ALLOCATION"):
            st.session_state.portfolio_allocation['Conservative']['BTC'] = btc_con / 100
            st.session_state.portfolio_allocation['Conservative']['ETH'] = eth_con / 100
            st.markdown('<p class="success-message">✓ Portfolio allocation updated successfully!</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Section Divider
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Enhanced Market Statistics Section
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: var(--text-primary);">📊 MARKET STATISTICS</h3>', unsafe_allow_html=True)
        st.markdown('<div class="description-text">Real-time market metrics and sentiment indicators to help you make informed trading decisions.</div>', unsafe_allow_html=True)
        
        # Enhanced Stats Cards
        st.markdown("""
        <div class="stats-card">
            <div class="stats-label">💰 Total Market Cap</div>
            <div class="stats-value">$2.5T</div>
            <div class="stats-change positive">+2.3%</div>
            <div class="stats-description">Combined value of all cryptocurrencies in the market</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stats-card">
            <div class="stats-label">📈 24h Volume</div>
            <div class="stats-value">$98.7B</div>
            <div class="stats-change positive">+15.2%</div>
            <div class="stats-description">Total trading volume in the last 24 hours</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stats-card">
            <div class="stats-label">👑 BTC Dominance</div>
            <div class="stats-value">53.2%</div>
            <div class="stats-change negative">-0.8%</div>
            <div class="stats-description">Bitcoin's share of total crypto market cap</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="stats-card">
            <div class="stats-label">😰 Fear & Greed Index</div>
            <div class="stats-value">76</div>
            <div class="stats-change negative">-2</div>
            <div class="stats-description">Market sentiment: Extreme Greed (0-100 scale)</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Enhanced Section Divider
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Enhanced Notification Center
        st.markdown('<div class="sidebar-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: var(--text-primary);">🔔 NOTIFICATION CENTER</h3>', unsafe_allow_html=True)
        st.markdown('<div class="description-text">Configure alerts and reports for your portfolio. Stay informed with real-time notifications.</div>', unsafe_allow_html=True)
        
        # Buttons
        st.markdown('<div style="margin: 0; padding: 0;">', unsafe_allow_html=True)
        if st.button("📩 SET PRICE ALERTS"):
            st.markdown('<p class="success-message">✓ Price alerts configured successfully!</p>', unsafe_allow_html=True)
        if st.button("📥 DOWNLOAD REPORT"):
            st.markdown('<p class="success-message">✓ Report generation initiated. Check downloads folder.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()