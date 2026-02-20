"""
Risk Management Framework
Enforces trading rules and position sizing
"""

import os
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv('/home/ubuntu/.openclaw/workspace/config/.env')


@dataclass
class Trade:
    """Trade data class for tracking"""
    symbol: str
    action: str
    entry_price: float
    quantity: float
    side: str
    timestamp: datetime = field(default_factory=datetime.now)
    exit_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit_targets: List[float] = field(default_factory=list)
    pnl: Optional[float] = None
    status: str = "open"
    notes: str = ""
    lessons: str = ""


class RiskManager:
    """Enforces trading rules and risk management"""
    
    def __init__(self):
        self.max_pump_pct = float(os.getenv("MAX_PUMP_PERCENTAGE", 200))
        self.min_pullback_pct = float(os.getenv("MIN_PULLBACK_PERCENT", 20))
        self.max_pullback_pct = float(os.getenv("MAX_PULLBACK_PERCENT", 40))
        self.min_liquidity = float(os.getenv("MIN_LIQUIDITY_USD", 50000))
        self.stop_loss_pct = float(os.getenv("STOP_LOSS_PERCENT", 20))
        self.max_position_pct = float(os.getenv("MAX_POSITION_PERCENT", 2))
        self.max_position_usd = float(os.getenv("MAX_POSITION_USD", 40))
        self.max_portfolio_per_asset = float(os.getenv("MAX_PORTFOLIO_PER_ASSET", 10))
        self.max_trades_per_day = int(os.getenv("MAX_TRADES_PER_DAY", 3))
        self.max_losses_per_day = int(os.getenv("MAX_LOSSES_PER_DAY", 1))
        self.max_daily_loss_pct = float(os.getenv("MAX_DAILY_LOSS_PERCENT", 5))
        
        # Track daily stats
        self.daily_trades: List[Trade] = []
        self.daily_losses = 0
        self.daily_pnl = 0.0
        self.last_reset = date.today()
        
        self.blacklist: set = set()
    
    def _reset_daily_if_needed(self):
        """Reset daily counters if day changed"""
        today = date.today()
        if today != self.last_reset:
            self.daily_trades = []
            self.daily_losses = 0
            self.daily_pnl = 0.0
            self.last_reset = today
    
    def add_to_blacklist(self, symbol: str, reason: str = ""):
        """Add symbol to blacklist"""
        self.blacklist.add(symbol)
        print(f"⚠️  BLACKLISTED {symbol}: {reason}")
    
    def is_blacklisted(self, symbol: str) -> bool:
        """Check if symbol is blacklisted"""
        return symbol in self.blacklist
    
    def validate_entry(self, symbol: str, current_price: float, 
                       high_price: float, liquidity: Optional[float] = None,
                       pump_24h: float = 0, pump_7d: float = 0,
                       portfolio_value: float = 10000) -> Dict[str, Any]:
        """
        Validate trade entry against all rules
        
        Returns dict with 'valid' (bool) and 'reasons' (list of messages)
        """
        self._reset_daily_if_needed()
        reasons = []
        valid = True
        
        # Check blacklist
        if self.is_blacklisted(symbol):
            valid = False
            reasons.append(f"❌ {symbol} is blacklisted")
        
        # Check daily trade limit
        if len(self.daily_trades) >= self.max_trades_per_day:
            valid = False
            reasons.append(f"❌ Daily trade limit reached ({self.max_trades_per_day})")
        
        # Check daily loss limit
        if self.daily_losses >= self.max_losses_per_day:
            valid = False
            reasons.append(f"❌ Daily loss limit reached ({self.max_losses_per_day})")
        
        # Check pump percentage (No FOMO rule)
        max_recent_pump = max(pump_24h, pump_7d)
        if max_recent_pump > self.max_pump_pct:
            valid = False
            reasons.append(f"❌ Already pumped {max_recent_pump:.1f}% (> {self.max_pump_pct}%)")
        
        # Check pullback percentage
        if high_price > 0:
            pullback_pct = ((high_price - current_price) / high_price) * 100
            if pullback_pct < self.min_pullback_pct:
                valid = False
                reasons.append(f"❌ Pullback only {pullback_pct:.1f}% (need {self.min_pullback_pct}-{self.max_pullback_pct}%)")
            elif pullback_pct > self.max_pullback_pct:
                valid = False
                reasons.append(f"❌ Pulled back too far: {pullback_pct:.1f}% (> {self.max_pullback_pct}%)")
            else:
                reasons.append(f"✅ Pullback: {pullback_pct:.1f}% (target: {self.min_pullback_pct}-{self.max_pullback_pct}%)")
        
        # Check liquidity (crypto only)
        if liquidity is not None and liquidity < self.min_liquidity:
            valid = False
            reasons.append(f"❌ Low liquidity: ${liquidity:,.0f} (< ${self.min_liquidity:,.0f})")
        
        return {"valid": valid, "reasons": reasons, "can_trade": valid}
    
    def calculate_position_size(self, entry_price: float, portfolio_value: float,
                              is_crypto: bool = False) -> Dict[str, Any]:
        """Calculate safe position size"""
        # Max by percentage
        max_by_pct = portfolio_value * (self.max_position_pct / 100)
        
        # Max by USD limit
        max_by_usd = self.max_position_usd
        
        # Use minimum of both
        position_value = min(max_by_pct, max_by_usd)
        
        # Calculate quantity
        quantity = position_value / entry_price if entry_price > 0 else 0
        
        # Calculate stop loss price
        stop_loss = entry_price * (1 - self.stop_loss_pct / 100)
        
        return {
            "quantity": quantity,
            "position_value": position_value,
            "stop_loss": stop_loss,
            "stop_loss_pct": self.stop_loss_pct,
            "take_profit_1": entry_price * 2,   # 2x
            "take_profit_2": entry_price * 5,   # 5x
            "take_profit_3": entry_price * 10   # 10x
        }
    
    def record_trade(self, trade: Trade):
        """Record a trade"""
        self._reset_daily_if_needed()
        self.daily_trades.append(trade)
    
    def record_result(self, trade: Trade, exit_price: float):
        """Record trade result and update stats"""
        trade.exit_price = exit_price
        trade.status = "closed"
        
        if trade.side == "BUY":
            trade.pnl = (exit_price - trade.entry_price) * trade.quantity
        else:
            trade.pnl = (trade.entry_price - exit_price) * trade.quantity
        
        self.daily_pnl += trade.pnl
        
        if trade.pnl < 0:
            self.daily_losses += 1
        
        return trade.pnl
    
    def get_daily_summary(self) -> Dict[str, Any]:
        """Get daily trading summary"""
        self._reset_daily_if_needed()
        
        closed_trades = [t for t in self.daily_trades if t.status == "closed"]
        winning_trades = [t for t in closed_trades if t.pnl and t.pnl > 0]
        losing_trades = [t for t in closed_trades if t.pnl and t.pnl <= 0]
        
        return {
            "trades_today": len(self.daily_trades),
            "max_trades": self.max_trades_per_day,
            "closed_trades": len(closed_trades),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "daily_pnl": self.daily_pnl,
            "daily_losses": self.daily_losses,
            "max_losses": self.max_losses_per_day,
        "can_trade": (
            len(self.daily_trades) < self.max_trades_per_day and
            self.daily_losses < self.max_losses_per_day and
            self.daily_pnl > -self.max_daily_loss_pct
        )
    }
