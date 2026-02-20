"""
Example: Basic Strategy Usage with Upstox Bot
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy import MovingAverageCrossoverStrategy, RSIStrategy
from bot import UpstoxTradingBot


def run_example(environment="sandbox"):
    """Run example strategy"""
    # Initialize bot
    bot = UpstoxTradingBot(environment=environment)
    
    # Check authentication
    if not bot.auth.access_token:
        print("=== Authentication Required ===")
        print("Visit this URL to authorize:")
        auth_url = bot.auth.get_authorization_url(scope="orders holdings user")
        print(auth_url)
        print("\nAfter authorization, you'll get a code. Run:")
        print("  python -c \"from bot import auth; auth.exchange_code_for_token('YOUR_CODE')\"")
        return
    
    # Add strategies
    ma_strategy = MovingAverageCrossoverStrategy(
        name="Infosys_MA_Crossover",
        short_window=5,
        long_window=20,
        symbol="NSE_EQ|INE009A01021"  # Infosys
    )
    bot.add_strategy(ma_strategy)
    
    rsi_strategy = RSIStrategy(
        name="Reliance_RSI",
        rsi_period=14,
        oversold=30,
        overbought=70,
        symbol="NSE_EQ|INE002A01018"  # Reliance
    )
    bot.add_strategy(rsi_strategy)
    
    print("=== Starting Bot ===")
    print("Strategies loaded:", [s.name for s in bot.strategies])
    print("Press Ctrl+C to stop")
    
    # Start bot with 5-minute intervals
    bot.start(interval=300)


if __name__ == "__main__":
    run_example()
