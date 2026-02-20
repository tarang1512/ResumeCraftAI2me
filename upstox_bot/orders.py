"""
Order management module for Upstox Trading Bot
"""

from typing import Dict, Any, Optional, List
from enum import Enum
from upstox_bot.logger import get_logger

logger = get_logger(__name__)


class OrderType(Enum):
    """Order types supported by Upstox"""
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    SL = "SL"
    SLM = "SLM"


class TransactionType(Enum):
    """Buy or Sell"""
    BUY = "BUY"
    SELL = "SELL"


class ProductType(Enum):
    """Product types for margin/leverage"""
    INTRADAY = "I"
    DELIVERY = "D"
    CO = "CO"
    OCO = "OCO"
    AMO = "AMO"


class DurationType(Enum):
    """Order duration"""
    DAY = "DAY"
    IOC = "IOC"


class Exchange(Enum):
    """Supported exchanges"""
    NSE = "NSE"
    BSE = "BSE"
    NFO = "NFO"
    BFO = "BFO"
    MCX = "MCX"


class OrderManager:
    """Manages orders for Upstox trading"""
    
    def __init__(self, client):
        self.client = client
        logger.info("OrderManager initialized")
    
    def place_order(self,
                   instrument_token: str,
                   transaction_type: TransactionType,
                   quantity: int,
                   order_type: OrderType = OrderType.MARKET,
                   product: ProductType = ProductType.DELIVERY,
                   price: Optional[float] = None,
                   trigger_price: Optional[float] = None,
                   exchange: Exchange = Exchange.NSE,
                   duration: DurationType = DurationType.DAY,
                   disclosed_quantity: int = 0,
                   tag: Optional[str] = None) -> Dict[str, Any]:
        
        payload = {
            "instrument_token": instrument_token,
            "transaction_type": transaction_type.value,
            "quantity": quantity,
            "order_type": order_type.value,
            "product": product.value,
            "exchange": exchange.value,
            "validity": duration.value,
            "disclosed_quantity": disclosed_quantity
        }
        
        if price is not None:
            payload["price"] = price
        if trigger_price is not None:
            payload["trigger_price"] = trigger_price
        if tag:
            payload["tag"] = tag
        
        logger.info(f"Placing {transaction_type.value} order: {payload}")
        response = self.client.post("/order/place", json=payload)
        
        if response.get("status") == "success":
            logger.info(f"Order placed successfully: {response.get('data', {})}")
        else:
            logger.error(f"Order failed: {response}")
        
        return response
    
    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        """Cancel an existing order"""
        logger.info(f"Cancelling order: {order_id}")
        return self.client.delete(f"/order/cancel?orderId={order_id}")
    
    def modify_order(self, order_id: str, **kwargs) -> Dict[str, Any]:
        """Modify an existing order"""
        logger.info(f"Modifying order: {order_id}")
        return self.client.put(f"/order/modify", json={"order_id": order_id, **kwargs})
    
    def get_order_history(self, order_id: str) -> Dict[str, Any]:
        """Get order history"""
        return self.client.get(f"/order/history?orderId={order_id}")
    
    def get_orders(self) -> List[Dict[str, Any]]:
        """Get all orders - Note: This endpoint may not be available in v2 API"""
        try:
            # Try the v2 order book endpoint first
            response = self.client.get("/order/orders")
            return response.get("data", [])
        except Exception as e:
            logger.warning(f"Could not fetch orders list: {e}")
            logger.info("Falling back to empty order list - portfolio and trades endpoints still work")
            return []
    
    def get_order_trades(self, order_id: str) -> List[Dict[str, Any]]:
        """Get trades for a specific order"""
        try:
            response = self.client.get(f"/order/trades?orderId={order_id}")
            return response.get("data", [])
        except Exception as e:
            logger.warning(f"Could not fetch trades for order {order_id}: {e}")
            return []
    
    def get_day_trades(self) -> List[Dict[str, Any]]:
        """Get all trades for the day - Note: Endpoint may require order_id"""
        logger.warning("get_day_trades() - This endpoint requires order_id in v2 API")
        return []
    
    def buy(self, instrument_token: str, quantity: int, **kwargs) -> Dict[str, Any]:
        """Convenience method to place a buy order"""
        return self.place_order(
            instrument_token=instrument_token,
            transaction_type=TransactionType.BUY,
            quantity=quantity,
            **kwargs
        )
    
    def sell(self, instrument_token: str, quantity: int, **kwargs) -> Dict[str, Any]:
        """Convenience method to place a sell order"""
        return self.place_order(
            instrument_token=instrument_token,
            transaction_type=TransactionType.SELL,
            quantity=quantity,
            **kwargs
        )
