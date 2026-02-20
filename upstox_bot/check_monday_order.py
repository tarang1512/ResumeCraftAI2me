#!/usr/bin/env python3
"""Check Monday order status manually"""
import sys
sys.path.insert(0, '/home/ubuntu/.openclaw/workspace')
from upstox_bot.auth import UpstoxAuth
from upstox_bot.api_client import UpstoxClient
from upstox_bot.orders import OrderManager
import json

def check_orders():
    auth = UpstoxAuth()
    client = UpstoxClient(auth, environment=auth.environment)
    om = OrderManager(client)
    
    orders = om.get_orders()
    
    print("📋 YOUR ORDERS:")
    print("=" * 60)
    
    for order in orders:
        tag = order.get('tag', '')
        if 'monday_auto_buy' in tag or order.get('tradingsymbol') == 'NTPC':
            print(f"\n🔔 ORDER FOUND:")
            print(f"  Symbol: {order.get('tradingsymbol')}")
            print(f"  Status: {order.get('status')}")  # OPEN, COMPLETE, CANCELLED
            print(f"  Qty: {order.get('quantity')}")
            print(f"  Price: ₹{order.get('price')}")
            print(f"  Tag: {tag}")
            print(f"  Order ID: {order.get('order_id')}")
            
            if order.get('status') == 'COMPLETE':
                print(f"  ✅ FILLED at ₹{order.get('average_price')}")
            elif order.get('status') == 'OPEN':
                print(f"  ⏳ PENDING (not filled yet)")
            elif order.get('status') == 'CANCELLED':
                print(f"  ❌ CANCELLED")
    
    if not any('monday_auto_buy' in str(o.get('tag','')) for o in orders):
        print("No orders with tag 'monday_auto_buy' found yet.")
        print("Check again after 9:15 AM IST Monday.")

if __name__ == "__main__":
    check_orders()
