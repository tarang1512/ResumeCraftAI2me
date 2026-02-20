"""
Strategy Framework for Upstox Trading Bot
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from upstox_bot.logger import get_logger

logger = get_logger(__name__)


@dataclass
class Signal:
    """Trade signal data class"""
    action: str  # BUY, SELL, HOLD
    symbol: str
    price: float
    quantity: int
    confidence: float
    reason: str
    timestamp: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


class Strategy(ABC):
    """Abstract base class for trading strategies"""
    
    def __init__(self, name: str, **params):
        self.name = name
        self.params = params
        self.is_active = True
        
        logger.info(f"Strategy '{name}' initialized")
    
    @abstractmethod
    def analyze(self, data: Dict[str, Any]) -> Optional[Signal]:
        """Analyze market data and generate trading signal"""
        pass
    
    @abstractmethod
    def on_trade_executed(self, trade: Dict[str, Any]):
        """Called when a trade is executed"""
        pass
    
    def stop(self):
        """Stop the strategy"""
        self.is_active = False
        logger.info(f"Strategy '{self.name}' stopped")


class MovingAverageCrossoverStrategy(Strategy):
    """Simple Moving Average Crossover Strategy"""
    
    def __init__(self, name: str, short_window: int = 10, long_window: int = 30,
                 symbol: str = "NSE_EQ|INE002A01018", **params):
        super().__init__(name, short_window=short_window, long_window=long_window, **params)
        self.short_window = short_window
        self.long_window = long_window
        self.symbol = symbol
        self.prices = []
        self.position = None  # BUY, SELL, or None
        
    def analyze(self, data: Dict[str, Any]) -> Optional[Signal]:
        """Generate signals based on MA crossover"""
        current_price = data.get("price")
        if current_price is None:
            return None
        
        self.prices.append(current_price)
        
        if len(self.prices) < self.long_window:
            return None
        
        # Keep only recent prices
        if len(self.prices) > self.long_window * 2:
            self.prices = self.prices[-self.long_window * 2:]
        
        short_ma = sum(self.prices[-self.short_window:]) / self.short_window
        long_ma = sum(self.prices[-self.long_window:]) / self.long_window
        
        # Generate signal
        if short_ma > long_ma and self.position != "BUY":
            self.position = "BUY"
            return Signal(
                action="BUY",
                symbol=self.symbol,
                price=current_price,
                quantity=10,  # Simplified
                confidence=0.7,
                reason=f"{self.short_window} MA crossed above {self.long_window} MA"
            )
        elif short_ma < long_ma and self.position != "SELL":
            self.position = "SELL"
            return Signal(
                action="SELL",
                symbol=self.symbol,
                price=current_price,
                quantity=10,
                confidence=0.7,
                reason=f"{self.short_window} MA crossed below {self.long_window} MA"
            )
        
        return None
    
    def on_trade_executed(self, trade: Dict[str, Any]):
        """Handle executed trade"""
        logger.info(f"Trade executed for {self.name}: {trade}")


class RSIStrategy(Strategy):
    """RSI-based mean reversion strategy"""
    
    def __init__(self, name: str, rsi_period: int = 14,
                 oversold: float = 30, overbought: float = 70,
                 symbol: str = "NSE_EQ|INE002A01018", **params):
        super().__init__(name, rsi_period=rsi_period, oversold=oversold,
                        overbought=overbought, **params)
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought
        self.symbol = symbol
        self.prices = []
        self.last_signal = None
    
    def calculate_rsi(self, prices: list) -> float:
        """Calculate RSI value"""
        if len(prices) < self.rsi_period + 1:
            return 50.0
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d for d in deltas[-self.rsi_period:] if d > 0]
        losses = [-d for d in deltas[-self.rsi_period:] if d < 0]
        
        avg_gain = sum(gains) / len(gains) if gains else 0
        avg_loss = sum(losses) / len(losses) if losses else 0.001
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze(self, data: Dict[str, Any]) -> Optional[Signal]:
        """Generate signals based on RSI"""
        current_price = data.get("price")
        if current_price is None:
            return None
        
        self.prices.append(current_price)
        
        if len(self.prices) < self.rsi_period + 1:
            return None
        
        rsi = self.calculate_rsi(self.prices)
        
        if rsi < self.oversold and self.last_signal != "BUY":
            self.last_signal = "BUY"
            return Signal(
                action="BUY",
                symbol=self.symbol,
                price=current_price,
                quantity=10,
                confidence=(self.oversold - rsi) / self.oversold,
                reason=f"RSI oversold ({rsi:.2f} < {self.oversold})"
            )
        elif rsi > self.overbought and self.last_signal != "SELL":
            self.last_signal = "SELL"
            return Signal(
                action="SELL",
                symbol=self.symbol,
                price=current_price,
                quantity=10,
                confidence=(rsi - self.overbought) / (100 - self.overbought),
                reason=f"RSI overbought ({rsi:.2f} > {self.overbought})"
            )
        
        return None
    
    def on_trade_executed(self, trade: Dict[str, Any]):
        """Handle executed trade"""
        logger.info(f"Trade executed for {self.name}: {trade}")
