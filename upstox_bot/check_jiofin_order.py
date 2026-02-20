#!/usr/bin/env python3
"""Monitor JIOFIN order and send WhatsApp alert when filled"""
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace')

from dotenv import load_dotenv
load_dotenv('/home/ubuntu/.openclaw/workspace/config/.env')

from upstox_bot.auth import UpstoxAuth
from upstox_bot.api_client import UpstoxClient
from upstox_bot.orders import OrderManager
import json
import os

def check_order():
    auth = UpstoxAuth(environment='production')
    client = UpstoxClient(auth, environment='production')
    orders = OrderManager(client)
    
    try:
        all_orders = orders.get_orders()
        for order in all_orders:
            if order.get('order_id') == '260216000001108':
                status = order.get('status')
                if status == 'complete':
                    print(f"✅ JIOFIN ORDER FILLED!")
                    print(f"Quantity: {order.get('quantity')}")
                    print(f"Price: ₹{order.get('average_price')}")
                    return True
                else:
                    print(f"Order status: {status}")
                    return False
        print("Order not found")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if check_order():
        sys.exit(0)  # Success - order filled
    else:
        sys.exit(1)  # Not filled yet
