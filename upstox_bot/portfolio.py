"""
Portfolio tracking module for Upstox Trading Bot
"""

from typing import Dict, Any, List, Optional
from upstox_bot.logger import get_logger

logger = get_logger(__name__)


class Portfolio:
    """Manages portfolio and holdings for Upstox"""
    
    def __init__(self, client):
        self.client = client
        logger.info("Portfolio initialized")
    
    def get_holdings(self) -> List[Dict[str, Any]]:
        """Get all holdings (long-term holdings)"""
        response = self.client.get("/portfolio/long-term-holdings")
        return response.get("data", [])
    
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all current positions (day and overnight)"""
        response = self.client.get("/portfolio/short-term-positions")
        return response.get("data", [])
    
    def get_day_positions(self) -> List[Dict[str, Any]]:
        """Get only day positions"""
        positions = self.get_positions()
        return [p for p in positions if p.get("product") == "I"]
    
    def get_overnight_positions(self) -> List[Dict[str, Any]]:
        """Get overnight/delivery positions"""
        positions = self.get_positions()
        return [p for p in positions if p.get("product") == "D"]
    
    def get_holdings_by_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get specific holding by symbol"""
        holdings = self.get_holdings()
        for holding in holdings:
            if holding.get("trading_symbol") == symbol:
                return holding
        return None
    
    def get_positions_by_symbol(self, symbol: str) -> List[Dict[str, Any]]:
        """Get positions by symbol"""
        positions = self.get_positions()
        return [p for p in positions if p.get("trading_symbol") == symbol]
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary including P&L"""
        holdings = self.get_holdings()
        positions = self.get_positions()
        
        total_investment = sum(h.get("investment", 0) for h in holdings)
        current_value = sum(h.get("last_price", 0) * h.get("quantity", 0) for h in holdings)
        pnl = current_value - total_investment
        pnl_percent = (pnl / total_investment * 100) if total_investment > 0 else 0
        
        return {
            "total_investment": total_investment,
            "current_value": current_value,
            "unrealized_pnl": pnl,
            "unrealized_pnl_percent": pnl_percent,
            "holdings_count": len(holdings),
            "positions_count": len(positions),
            "holdings": holdings,
            "positions": positions
        }
    
    def calculate_position_size(self, 
                               available_capital: float,
                               risk_percent: float,
                               entry_price: float,
                               stop_loss: float) -> Dict[str, Any]:
        """
        Calculate position size based on risk management
        
        Args:
            available_capital: Available trading capital
            risk_percent: Risk percentage per trade (0.01 = 1%)
            entry_price: Planned entry price
            stop_loss: Stop loss price
            
        Returns:
            Calculated position details
        """
        risk_amount = available_capital * risk_percent
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            logger.warning("Price risk is zero, cannot calculate position size")
            return {"quantity": 0, "message": "Invalid stop loss"}
        
        quantity = int(risk_amount / price_risk)
        position_value = quantity * entry_price
        
        return {
            "quantity": quantity,
            "position_value": position_value,
            "risk_amount": risk_amount,
            "price_risk": price_risk,
            "risk_percent": risk_percent * 100
        }
    
    def get_user_funds(self) -> Dict[str, Any]:
        """Get available funds and margin details"""
        response = self.client.get("/user/get-funds-and-margin")
        return response.get("data", {})
