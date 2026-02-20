#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════
FINAL TRADING STRATEGY - Indian Market Optimized
═══════════════════════════════════════════════════════════════════

Combines principles from legendary Indian traders:
• Rakesh Jhunjhunwala (Trend following, conviction, price+volume)
• Vijay Kedia (Small cap focus, patience, quality businesses)
• Nemish Shah (Entry on dips, long-term holding)
• Price Action (Support/Resistance, breakouts)

STRATEGIES INCLUDED:
1. IndianTrendStrategy    - Buy dips in strong uptrends
2. BreakoutStrategy       - Resistance breakouts with volume
3. RSIMeanReversion       - Oversold bounces (RSI < 30)
4. MACrossoverStrategy    - Moving average crossovers
5. CombinedEngine         - Votes from all strategies

USAGE:
    from final_strategy import CombinedEngine, RiskManager
    
    engine = CombinedEngine(available_funds=3786)
    signal = engine.analyze(
        symbol="RELIANCE",
        price=1423,
        price_history=[...],
        volume=100000,
        volume_history=[...]
    )
    
    if signal and signal.action == "BUY":
        print(f"Buy {signal.quantity} shares at ₹{signal.price}")
        print(f"Stop: ₹{signal.stop_loss}, Target: ₹{signal.target}")

═══════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple
from enum import Enum
import json

# ═══════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Signal:
    action: str  # BUY, SELL, HOLD
    symbol: str
    price: float
    quantity: int
    confidence: float  # 0.0 to 1.0
    reason: str
    strategy: str
    stop_loss: Optional[float] = None
    target: Optional[float] = None
    risk_percent: Optional[float] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            'action': self.action,
            'symbol': self.symbol,
            'price': self.price,
            'quantity': self.quantity,
            'confidence': self.confidence,
            'reason': self.reason,
            'strategy': self.strategy,
            'stop_loss': self.stop_loss,
            'target': self.target,
            'risk_percent': self.risk_percent,
            'timestamp': self.timestamp.isoformat()
        }

# ═══════════════════════════════════════════════════════════════════
# RISK MANAGEMENT (Capital Preservation First)
# ═══════════════════════════════════════════════════════════════════

class RiskManager:
    """
    Indian Trader Risk Rules:
    • Never risk more than 2% per trade
    • Never use more than 25% capital per position
    • Minimum 1:2 risk:reward ratio
    • Always have a stop loss
    """
    
    def __init__(self, available_funds: float = 3786.89, 
                 max_risk_percent: float = 2.0,
                 max_position_percent: float = 25.0):
        self.available = available_funds
        self.max_risk = max_risk_percent / 100
        self.max_position = max_position_percent / 100
    
    def calculate_position(self, entry: float, stop_loss: float, 
                          target: Optional[float] = None) -> Dict[str, Any]:
        """Calculate position size with risk management"""
        
        if entry <= 0 or stop_loss <= 0:
            return {"error": "Invalid prices", "quantity": 0}
        
        risk_per_share = abs(entry - stop_loss)
        if risk_per_share == 0:
            return {"error": "Stop loss equals entry", "quantity": 0}
        
        # Max risk amount (2% of capital)
        max_risk_amount = self.available * self.max_risk
        quantity = int(max_risk_amount / risk_per_share)
        
        # Position size limit (25% max per trade)
        max_position_value = self.available * self.max_position
        if quantity * entry > max_position_value:
            quantity = int(max_position_value / entry)
        
        position_value = quantity * entry
        
        # Default target: 1:2 risk:reward minimum
        if target is None:
            risk = entry - stop_loss
            target = entry + (2 * risk)
        
        return {
            "quantity": max(quantity, 0),
            "position_value": position_value,
            "risk_amount": quantity * risk_per_share,
            "risk_percent": (quantity * risk_per_share / self.available) * 100,
            "stop_loss": stop_loss,
            "target": target,
            "risk_reward": abs(target - entry) / risk_per_share
        }

# ═══════════════════════════════════════════════════════════════════
# STRATEGY 1: INDIAN TREND FOLLOWING (Jhunjhunwala Style)
# ═══════════════════════════════════════════════════════════════════

class IndianTrendStrategy:
    """
    Rakesh Jhunjhunwala Principles:
    • "Trend is your friend" - Trade with the trend
    • "Buy right, sit tight" - Quality entries, hold with conviction
    • Price + Volume confirmation
    • Buy on dips in strong uptrends
    
    Entry: Price pulls back to 10-day low but stays above 20 MA
    Exit: Stop below 20 MA or trailing stop
    """
    
    def __init__(self, risk_mgr: RiskManager):
        self.name = "IndianTrend"
        self.risk_mgr = risk_mgr
    
    def is_uptrend(self, prices: List[float]) -> Tuple[bool, float, float]:
        """Check: Price > 10MA > 20MA"""
        if len(prices) < 25:
            return False, 0, 0
        
        ma10 = sum(prices[-10:]) / 10
        ma20 = sum(prices[-20:]) / 20
        current = prices[-1]
        
        return (current > ma10 > ma20), ma10, ma20
    
    def analyze(self, symbol: str, price: float, 
                price_history: List[float], 
                volume: float, volume_history: List[float]) -> Optional[Signal]:
        
        if len(price_history) < 30 or len(volume_history) < 10:
            return None
        
        # Must be in uptrend
        is_up, ma10, ma20 = self.is_uptrend(price_history)
        if not is_up:
            return None
        
        # Pullback: Price near 10-day low but above MA20
        recent_low = min(price_history[-10:])
        recent_high = max(price_history[-20:])
        
        is_pullback = (price <= recent_low * 1.02) and (price > ma20 * 0.98)
        
        # Volume confirmation (30% above average)
        avg_volume = sum(volume_history[-10:]) / 10
        volume_ok = volume > avg_volume * 1.3 if avg_volume > 0 else False
        
        if not (is_pullback and volume_ok):
            return None
        
        # Calculate levels
        stop_loss = min(ma20 * 0.97, recent_low * 0.97)
        position = self.risk_mgr.calculate_position(price, stop_loss)
        
        if position.get('quantity', 0) == 0:
            return None
        
        return Signal(
            action="BUY",
            symbol=symbol,
            price=price,
            quantity=position['quantity'],
            confidence=0.75,
            reason=f"📈 Dip in uptrend: ₹{price:.2f} near ₹{recent_low:.2f} (10D low), MA20 ₹{ma20:.2f}",
            strategy=self.name,
            stop_loss=stop_loss,
            target=position['target'],
            risk_percent=position['risk_percent']
        )

# ═══════════════════════════════════════════════════════════════════
# STRATEGY 2: BREAKOUT TRADING
# ═══════════════════════════════════════════════════════════════════

class BreakoutStrategy:
    """
    Classic Breakout Strategy:
    • Buy when price breaks above 20-day high
    • Volume must confirm (30% above average)
    • Stop below breakout level
    • Target: 5-10% above entry
    """
    
    def __init__(self, risk_mgr: RiskManager):
        self.name = "Breakout"
        self.risk_mgr = risk_mgr
    
    def analyze(self, symbol: str, price: float,
                price_history: List[float],
                volume: float, volume_history: List[float]) -> Optional[Signal]:
        
        if len(price_history) < 25 or len(volume_history) < 10:
            return None
        
        # Find 20-day resistance
        resistance = max(price_history[-20:])
        
        # Breakout: Price 1% above resistance
        if price < resistance * 1.01:
            return None
        
        # Volume confirmation
        avg_volume = sum(volume_history[-10:]) / 10
        if volume < avg_volume * 1.3:
            return None
        
        # Calculate levels
        stop_loss = resistance * 0.98  # Below breakout
        target = price * 1.06  # 6% target
        position = self.risk_mgr.calculate_position(price, stop_loss, target)
        
        if position.get('quantity', 0) == 0:
            return None
        
        return Signal(
            action="BUY",
            symbol=symbol,
            price=price,
            quantity=position['quantity'],
            confidence=0.80,
            reason=f"🚀 Breakout: ₹{price:.2f} broke ₹{resistance:.2f} resistance with volume",
            strategy=self.name,
            stop_loss=stop_loss,
            target=target,
            risk_percent=position['risk_percent']
        )

# ═══════════════════════════════════════════════════════════════════
# STRATEGY 3: RSI MEAN REVERSION
# ═══════════════════════════════════════════════════════════════════

class RSIMeanReversion:
    """
    RSI-Based Mean Reversion:
    • Buy when RSI < 30 (oversold)
    • Sell when RSI > 70 (overbought)
    • Works best in range-bound markets
    """
    
    def __init__(self, risk_mgr: RiskManager, period: int = 14,
                 oversold: float = 30, overbought: float = 70):
        self.name = "RSI_MeanReversion"
        self.risk_mgr = risk_mgr
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_rsi(self, prices: List[float]) -> float:
        if len(prices) < self.period + 1:
            return 50.0
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        gains = [d for d in deltas[-self.period:] if d > 0]
        losses = [-d for d in deltas[-self.period:] if d < 0]
        
        avg_gain = sum(gains) / len(gains) if gains else 0
        avg_loss = sum(losses) / len(losses) + 0.001 if losses else 0.001
        
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    def analyze(self, symbol: str, price: float,
                price_history: List[float]) -> Optional[Signal]:
        
        if len(price_history) < self.period + 5:
            return None
        
        rsi = self.calculate_rsi(price_history)
        
        # Oversold - Buy signal
        if rsi < self.oversold:
            # Stop below recent low
            recent_low = min(price_history[-10:])
            stop_loss = recent_low * 0.98
            position = self.risk_mgr.calculate_position(price, stop_loss)
            
            if position.get('quantity', 0) == 0:
                return None
            
            return Signal(
                action="BUY",
                symbol=symbol,
                price=price,
                quantity=position['quantity'],
                confidence=(self.oversold - rsi) / self.oversold,
                reason=f"📊 RSI Oversold: {rsi:.1f} < {self.oversold} (mean reversion)",
                strategy=self.name,
                stop_loss=stop_loss,
                target=position['target'],
                risk_percent=position['risk_percent']
            )
        
        return None

# ═══════════════════════════════════════════════════════════════════
# STRATEGY 4: MOVING AVERAGE CROSSOVER
# ═══════════════════════════════════════════════════════════════════

class MACrossoverStrategy:
    """
    Classic MA Crossover:
    • BUY: 10 MA crosses above 30 MA (golden cross short-term)
    • SELL: 10 MA crosses below 30 MA (death cross)
    • Simple trend following
    """
    
    def __init__(self, risk_mgr: RiskManager, 
                 short_window: int = 10, long_window: int = 30):
        self.name = "MA_Crossover"
        self.risk_mgr = risk_mgr
        self.short = short_window
        self.long = long_window
        self.last_position = None
    
    def analyze(self, symbol: str, price: float,
                price_history: List[float]) -> Optional[Signal]:
        
        if len(price_history) < self.long + 5:
            return None
        
        short_ma = sum(price_history[-self.short:]) / self.short
        long_ma = sum(price_history[-self.long:]) / self.long
        
        # Golden cross (short above long)
        if short_ma > long_ma and self.last_position != "BUY":
            self.last_position = "BUY"
            stop_loss = long_ma * 0.97
            position = self.risk_mgr.calculate_position(price, stop_loss)
            
            if position.get('quantity', 0) == 0:
                return None
            
            return Signal(
                action="BUY",
                symbol=symbol,
                price=price,
                quantity=position['quantity'],
                confidence=0.70,
                reason=f"📈 MA Crossover: {self.short}MA ₹{short_ma:.2f} > {self.long}MA ₹{long_ma:.2f}",
                strategy=self.name,
                stop_loss=stop_loss,
                target=position['target'],
                risk_percent=position['risk_percent']
            )
        
        return None

# ═══════════════════════════════════════════════════════════════════
# COMBINED ENGINE - Votes from All Strategies
# ═══════════════════════════════════════════════════════════════════

class CombinedEngine:
    """
    Master trading engine that combines all strategies.
    Requires 2+ strategies to agree for a BUY signal (consensus).
    """
    
    def __init__(self, available_funds: float = 3786.89,
                 consensus_threshold: int = 2):
        self.risk_mgr = RiskManager(available_funds)
        self.consensus = consensus_threshold
        
        # Initialize all strategies
        self.strategies = [
            IndianTrendStrategy(self.risk_mgr),
            BreakoutStrategy(self.risk_mgr),
            RSIMeanReversion(self.risk_mgr),
            MACrossoverStrategy(self.risk_mgr)
        ]
    
    def analyze(self, symbol: str, price: float,
                price_history: List[float] = None,
                volume: float = 0,
                volume_history: List[float] = None) -> Optional[Signal]:
        """
        Run all strategies and return consensus signal
        """
        price_history = price_history or []
        volume_history = volume_history or []
        
        signals = []
        
        for strategy in self.strategies:
            try:
                if strategy.name == "RSI_MeanReversion":
                    sig = strategy.analyze(symbol, price, price_history)
                elif strategy.name == "MA_Crossover":
                    sig = strategy.analyze(symbol, price, price_history)
                else:
                    sig = strategy.analyze(symbol, price, price_history, 
                                          volume, volume_history)
                
                if sig and sig.action == "BUY":
                    signals.append(sig)
            except Exception as e:
                continue
        
        # Consensus: Need 2+ strategies to agree
        if len(signals) >= self.consensus:
            # Pick highest confidence signal
            best = max(signals, key=lambda x: x.confidence)
            best.reason = f"🔥 CONSENSUS ({len(signals)}/4 strategies): {best.reason}"
            return best
        
        elif len(signals) == 1:
            # Single strategy - lower confidence
            sig = signals[0]
            sig.confidence *= 0.7
            sig.reason = f"⚠️ SINGLE ({sig.strategy}): {sig.reason}"
            return sig
        
        return None
    
    def get_all_signals(self, symbol: str, price: float,
                       price_history: List[float],
                       volume: float = 0,
                       volume_history: List[float] = None) -> List[Signal]:
        """Get signals from all strategies for analysis"""
        volume_history = volume_history or []
        signals = []
        
        for strategy in self.strategies:
            try:
                if strategy.name == "RSI_MeanReversion":
                    sig = strategy.analyze(symbol, price, price_history)
                elif strategy.name == "MA_Crossover":
                    sig = strategy.analyze(symbol, price, price_history)
                else:
                    sig = strategy.analyze(symbol, price, price_history,
                                          volume, volume_history)
                if sig:
                    signals.append(sig)
            except:
                continue
        
        return signals

# ═══════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def print_signal(signal: Signal):
    """Pretty print a trading signal"""
    print(f"\n{'='*50}")
    print(f"📢 SIGNAL: {signal.action}")
    print(f"{'='*50}")
    print(f"Symbol: {signal.symbol}")
    print(f"Price: ₹{signal.price:.2f}")
    print(f"Quantity: {signal.quantity}")
    print(f"Confidence: {signal.confidence*100:.0f}%")
    print(f"Strategy: {signal.strategy}")
    print(f"Reason: {signal.reason}")
    if signal.stop_loss:
        print(f"Stop Loss: ₹{signal.stop_loss:.2f}")
    if signal.target:
        print(f"Target: ₹{signal.target:.2f}")
    if signal.risk_percent:
        print(f"Risk: {signal.risk_percent:.2f}% of capital")
    print(f"{'='*50}\n")

# ═══════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Example: Test with sample data
    engine = CombinedEngine(available_funds=3786.89)
    
    # Sample price history (uptrend with pullback)
    sample_prices = [100, 102, 105, 103, 108, 110, 112, 109, 107, 111,
                    115, 113, 118, 120, 117, 114, 116, 119, 121, 118,
                    116, 114, 115, 117, 120, 122, 119, 117, 115, 118]
    
    sample_volumes = [1000] * 30
    
    signal = engine.analyze(
        symbol="RELIANCE",
        price=118,
        price_history=sample_prices,
        volume=1500,
        volume_history=sample_volumes
    )
    
    if signal:
        print_signal(signal)
    else:
        print("No consensus signal generated")
    
    # Show all strategy signals
    print("\n📊 ALL STRATEGY SIGNALS:")
    all_sigs = engine.get_all_signals("RELIANCE", 118, sample_prices, 1500, sample_volumes)
    for sig in all_sigs:
        print(f"  {sig.strategy}: {sig.action} (conf: {sig.confidence:.2f})")
