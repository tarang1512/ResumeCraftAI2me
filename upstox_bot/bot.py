"""
Main Upstox Trading Bot
"""

import os
import time
import signal
from typing import Dict, Any, List
from dotenv import load_dotenv
from upstox_bot.logger import get_logger
from upstox_bot.auth import UpstoxAuth
from upstox_bot.api_client import UpstoxClient
from upstox_bot.orders import OrderManager, OrderType
from upstox_bot.market_data import MarketData
from upstox_bot.portfolio import Portfolio
from upstox_bot.strategy import Signal

logger = get_logger(__name__)


class UpstoxTradingBot:
    """Main trading bot class"""
    
    def __init__(self, environment: str = "sandbox"):
        load_dotenv('/home/ubuntu/.openclaw/workspace/config/.env')
        self.environment = environment or os.getenv("UPSTOX_ENVIRONMENT", "sandbox")
        self.is_running = False
        self.strategies = []
        self.auth = UpstoxAuth(environment=self.environment)
        self.client = UpstoxClient(self.auth, environment=self.environment)
        self.orders = OrderManager(self.client)
        self.market_data = MarketData(self.client)
        self.portfolio = Portfolio(self.client)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        logger.info(f"Upstox Trading Bot Initialized ({self.environment})")
    
    def _signal_handler(self, signum, frame):
        logger.info("Shutdown signal received. Stopping bot...")
        self.stop()
    
    def add_strategy(self, strategy):
        self.strategies.append(strategy)
        logger.info(f"Strategy '{strategy.name}' added")
    
    def execute_signal(self, signal: Signal) -> Dict[str, Any]:
        if signal.action == "HOLD":
            return {"status": "hold"}
        if signal.action == "BUY":
            order_type = OrderType.MARKET if signal.metadata.get("order_type") == "MARKET" else OrderType.LIMIT
            result = self.orders.buy(
                instrument_token=signal.symbol,
                quantity=signal.quantity,
                order_type=order_type,
                price=signal.price if order_type == OrderType.LIMIT else None
            )
        elif signal.action == "SELL":
            order_type = OrderType.MARKET if signal.metadata.get("order_type") == "MARKET" else OrderType.LIMIT
            result = self.orders.sell(
                instrument_token=signal.symbol,
                quantity=signal.quantity,
                order_type=order_type,
                price=signal.price if order_type == OrderType.LIMIT else None
            )
        else:
            return {"status": "error", "message": f"Unknown action: {signal.action}"}
        return result
    
    def run_strategy_cycle(self):
        for strategy in self.strategies:
            if not strategy.is_active:
                continue
            try:
                data = {"timestamp": time.time()}
                signal = strategy.analyze(data)
                if signal and signal.action != "HOLD":
                    result = self.execute_signal(signal)
                    strategy.on_trade_executed(result)
            except Exception as e:
                logger.error(f"Strategy error: {e}")
    
    def start(self, interval: int = 60):
        if not self.auth.access_token:
            logger.error("No access token. Authenticate first.")
            return
        self.is_running = True
        logger.info(f"Bot started (interval: {interval}s)")
        try:
            while self.is_running:
                self.run_strategy_cycle()
                time.sleep(interval)
        except Exception as e:
            logger.error(f"Bot error: {e}")
        finally:
            self.stop()
    
    def stop(self):
        self.is_running = False
        logger.info("Bot stopped")
        for strategy in self.strategies:
            strategy.stop()


def main():
    bot = UpstoxTradingBot()
    if not bot.auth.access_token:
        print("Authenticate first:", bot.auth.get_authorization_url())
        return
    bot.start()


if __name__ == "__main__":
    main()
