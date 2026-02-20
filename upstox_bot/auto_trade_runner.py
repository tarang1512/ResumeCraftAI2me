#!/usr/bin/env python3
"""Auto Trading Bot Runner - Runs during market hours"""
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace')

from upstox_bot.bot import UpstoxTradingBot
from upstox_bot.strategy import MovingAverageCrossoverStrategy, RSIStrategy
from upstox_bot.auth import UpstoxAuth
import os

# Stock symbols from holdings (need to map to instrument tokens)
HOLDINGS = {
    "JIOFIN": "NSE_EQ|INE758E01017",
    "INDHOTEL": "NSE_EQ|INE053A01029",
    "RELIANCE": "NSE_EQ|INE002A01018",
    "HDFCBANK": "NSE_EQ|INE040A01034",
    "ITC": "NSE_EQ|INE154A01025",
    "GMRAIRPORT": "NSE_EQ|INE792C01016"
}

def run_auto_trader():
    """Initialize and run trading bot with strategies"""
    env = os.getenv("UPSTOX_ENVIRONMENT", "production")
    bot = UpstoxTradingBot(environment=env)
    
    # Check auth
    if not bot.auth.access_token:
        print("[!] Not authenticated. Getting auth URL...")
        url = bot.auth.get_authorization_url()
        print(f"Authorize: {url}")
        return
    
    print("[+] Bot authenticated. Loading strategies...")
    
    # Add RSI strategy for each holding (mean reversion)
    for name, symbol in HOLDINGS.items():
        rsi = RSIStrategy(
            name=f"{name}_RSI",
            rsi_period=14,
            oversold=35,    # Buy when RSI < 35
            overbought=65,  # Sell when RSI > 65
            symbol=symbol
        )
        bot.add_strategy(rsi)
        print(f"  [+] RSI strategy added: {name}")
    
    # Add MA Crossover strategy for trending stocks
    ma = MovingAverageCrossoverStrategy(
        name="RELIANCE_MA_Trend",
        short_window=10,
        long_window=30,
        symbol=HOLDINGS["RELIANCE"]
    )
    bot.add_strategy(ma)
    print(f"  [+] MA strategy added: RELIANCE")
    
    print(f"\n[+] Starting auto-trader...")
    print(f"    Strategies: {len(bot.strategies)}")
    print(f"    Scan interval: 5 minutes")
    print(f"    Press Ctrl+C to stop\n")
    
    # Run with 5-minute intervals
    bot.start(interval=300)

if __name__ == "__main__":
    run_auto_trader()
