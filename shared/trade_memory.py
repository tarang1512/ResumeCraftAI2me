"""
Trade Memory & Learning System
Logs all trades and lessons learned
"""

import os
import json
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from pathlib import Path
from dataclasses import asdict

from risk_manager import Trade


class TradeMemory:
    """Handles persistent storage of trades and learnings"""
    
    MEMORY_DIR = "/home/ubuntu/.openclaw/workspace/memory"
    TRADES_FILE = f"{MEMORY_DIR}/trades.json"
    LESSONS_FILE = f"{MEMORY_DIR}/lessons.json"
    
    def __init__(self):
        os.makedirs(self.MEMORY_DIR, exist_ok=True)
        self.trades: List[Dict] = self._load_json(self.TRADES_FILE)
        self.lessons: List[Dict] = self._load_json(self.LESSONS_FILE)
    
    def _load_json(self, filepath: str) -> List[Dict]:
        """Load JSON file or return empty list"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
        return []
    
    def _save_json(self, filepath: str, data: List[Dict]):
        """Save data to JSON file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving {filepath}: {e}")
    
    def log_trade_entry(self, trade: Trade):
        """Log when trade is entered"""
        trade_data = {
            "id": f"{trade.symbol}_{trade.timestamp.strftime('%Y%m%d_%H%M%S')}",
            "symbol": trade.symbol,
            "action": trade.action,
            "side": trade.side,
            "entry_price": trade.entry_price,
            "quantity": trade.quantity,
            "stop_loss": trade.stop_loss,
            "take_profits": trade.take_profit_targets,
            "timestamp": trade.timestamp.isoformat(),
            "status": "open"
        }
        
        self.trades.append(trade_data)
        self._save_json(self.TRADES_FILE, self.trades)
        print(f"📝 Trade logged: {trade_data['id']}")
    
    def log_trade_exit(self, trade_id: str, exit_price: float, 
                       pnl: float, notes: str = ""):
        """Log when trade is exited"""
        for trade in self.trades:
            if trade.get("id") == trade_id:
                trade["exit_price"] = exit_price
                trade["pnl"] = pnl
                trade["status"] = "closed"
                trade["exit_time"] = datetime.now().isoformat()
                trade["notes"] = notes
                
                # Calculate metrics
                if pnl > 0:
                    trade["result"] = "win"
                else:
                    trade["result"] = "loss"
                
                self._save_json(self.TRADES_FILE, self.trades)
                print(f"📝 Trade exit logged: {trade_id}, PnL: ${pnl:.2f}")
                return
    
    def add_lesson(self, symbol: str, what_worked: str, 
                   what_didnt: str, lesson: str, trade_type: str = ""):
        """Add a lesson learned"""
        lesson_data = {
            "id": f"lesson_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "symbol": symbol,
            "trade_type": trade_type,
            "what_worked": what_worked,
            "what_didnt": what_didnt,
            "lesson": lesson,
            "timestamp": datetime.now().isoformat()
        }
        
        self.lessons.append(lesson_data)
        self._save_json(self.LESSONS_FILE, self.lessons)
        
        # Also update MEMORY.md
        self._update_memory_md(lesson_data)
        
        print(f"🧠 Lesson learned: {lesson[:50]}...")
    
    def _update_memory_md(self, lesson: Dict):
        """Append lesson to MEMORY.md"""
        memory_path = "/home/ubuntu/.openclaw/workspace/MEMORY.md"
        
        entry = f"""
## {datetime.now().strftime('%Y-%m-%d %H:%M')} - {lesson['symbol']}

**Trade Type:** {lesson['trade_type']}

**What Worked:**
{lesson['what_worked']}

**What Didn't:**
{lesson['what_didnt']}

**Lesson:**
{lesson['lesson']}

---
"""
        
        try:
            with open(memory_path, 'a') as f:
                f.write(entry)
        except Exception as e:
            print(f"Could not update MEMORY.md: {e}")
    
    def remember_this(self, key: str, value: str, category: str = "general"):
        """Store a fact to remember"""
        memory_file = f"{self.MEMORY_DIR}/remembered.json"
        
        memories = self._load_json(memory_file)
        memories.append({
            "key": key,
            "value": value,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_json(memory_file, memories)
        print(f"🧠 Remembered: [{category}] {key}")
    
    def get_trade_stats(self) -> Dict[str, Any]:
        """Get trading statistics"""
        closed = [t for t in self.trades if t.get("status") == "closed"]
        winners = [t for t in closed if t.get("result") == "win"]
        losers = [t for t in closed if t.get("result") == "loss"]
        
        total_pnl = sum(t.get("pnl", 0) for t in closed)
        
        return {
            "total_trades": len(closed),
            "winning_trades": len(winners),
            "losing_trades": len(losers),
            "win_rate": len(winners) / len(closed) * 100 if closed else 0,
            "total_pnl": total_pnl,
            "avg_pnl": total_pnl / len(closed) if closed else 0
        }
    
    def get_symbol_history(self, symbol: str) -> List[Dict]:
        """Get all trades for a symbol"""
        return [t for t in self.trades if t.get("symbol") == symbol]
    
    def generate_report(self, days: int = 30) -> str:
        """Generate a trading report"""
        cutoff = datetime.now() - __import__('datetime').timedelta(days=days)
        recent_trades = [
            t for t in self.trades 
            if datetime.fromisoformat(t.get("timestamp", "")) > cutoff
        ]
        
        stats = self.get_trade_stats()
        
        report = f"""
# Trading Report - Last {days} Days

## Performance Summary
- Total Trades: {stats['total_trades']}
- Win Rate: {stats['win_rate']:.1f}%
- Total PnL: ${stats['total_pnl']:.2f}
- Average PnL per Trade: ${stats['avg_pnl']:.2f}

## Lessons Learned ({len(self.lessons)} total)
"""
        
        for lesson in self.lessons[-5:]:
            report += f"\n- {lesson['timestamp'][:10]}: {lesson['lesson'][:60]}..."
        
        return report
