"""
Market Data module for Upstox Trading Bot
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from upstox_bot.logger import get_logger

logger = get_logger(__name__)


class MarketData:
    """Manages market data retrieval for Upstox"""
    
    def __init__(self, client):
        self.client = client
        logger.info("MarketData initialized")
    
    def get_instruments(self, exchange: str = "NSE") -> List[Dict[str, Any]]:
        """Get list of all instruments"""
        response = self.client.get(f"/market/instruments/{exchange}")
        return response.get("data", [])
    
    def get_quote(self, instrument_tokens: List[str]) -> Dict[str, Any]:
        """Get LTP and market depth"""
        tokens_str = ",".join(instrument_tokens)
        response = self.client.get(f"/market/quote?instrumentKey={tokens_str}")
        return response.get("data", {})
    
    def get_ohlc(self, instrument_tokens: List[str], interval: str = "1d") -> Dict[str, Any]:
        """Get OHLC data"""
        tokens_str = ",".join(instrument_tokens)
        response = self.client.get(f"/market/quote/ohlc?instrumentKey={tokens_str}&interval={interval}")
        return response.get("data", {})
    
    def get_historical_data(self, 
                          instrument_token: str,
                          interval: str,
                          from_date: datetime,
                          to_date: datetime) -> List[Dict[str, Any]]:
        """
        Get historical candlestick data
        
        Args:
            instrument_token: Instrument identifier
            interval: Candle duration (1m, 5m, 15m, 30m, 1h, 1d, 1w, 1M)
            from_date: Start date
            to_date: End date
        """
        from_str = from_date.strftime("%Y-%m-%d")
        to_str = to_date.strftime("%Y-%m-%d")
        
        url = f"/historical-candle/{instrument_token}/{interval}/{from_str}/{to_str}"
        response = self.client.get(url)
        return response.get("data", {}).get("candles", [])
    
    def get_instrument_details(self, instrument_token: str) -> Dict[str, Any]:
        """Get detailed instrument information"""
        response = self.client.get(f"/market/instruments/details?instrumentKey={instrument_token}")
        return response.get("data", {})
    
    def search_instruments(self, query: str, exchange: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for instruments"""
        params = {"search_string": query}
        if exchange:
            params["exchange"] = exchange
        response = self.client.get("/market/instruments/search", params=params)
        return response.get("data", [])
    
    def get_option_chain(self, instrument_token: str, expiry_date: str) -> Dict[str, Any]:
        """Get option chain for an instrument
        Args:
            instrument_token: Instrument identifier
            expiry_date: Expiry date for options
        Returns:
            Option chain data
        """
        response = self.client.get(f"/market/options?instrument_key={instrument_token}&expiry_date={expiry_date}")
        return response.get("data", {})