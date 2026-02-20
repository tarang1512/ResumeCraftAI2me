#!/usr/bin/env python3
"""Auto-place NTPC order Monday open"""
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace')
from upstox_bot.auth import UpstoxAuth
from upstox_bot.api_client import UpstoxClient
from upstox_bot.orders import OrderManager, OrderType, TransactionType, ProductType, Exchange
import json

def place_ntpc_order():
    auth = UpstoxAuth()
    client = UpstoxClient(auth, environment=auth.environment)
    om = OrderManager(client)
    
    # NTPC buy order
    token = 'NSE_EQ|INE733E01010'
    quantity = 11
    price = 340.0
    
    print(f'Placing BUY: NTPC')
    print(f'Qty: {quantity} @ ₹{price}')
    
    response = om.place_order(
        instrument_token=token,
        transaction_type=TransactionType.BUY,
        quantity=quantity,
        order_type=OrderType.LIMIT,
        product=ProductType.DELIVERY,
        price=price,
        trigger_price=price,
        exchange=Exchange.NSE,
        tag='monday_auto_buy'
    )
    
    print(json.dumps(response, indent=2))
    return response

if __name__ == "__main__":
    place_ntpc_order()
