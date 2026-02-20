#!/usr/bin/env python3
"""Quick Upstox Portfolio Check - Run this for instant summary"""
import requests
import os

API_BASE = 'https://api.upstox.com/v2'
ENV_PATH = '/home/ubuntu/.openclaw/workspace/upstox_bot/.env'

def get_token():
    """Load token from .env file"""
    with open(ENV_PATH, 'r') as f:
        for line in f:
            if line.startswith('UPSTOX_ACCESS_TOKEN='):
                return line.split('=', 1)[1].strip()
    return None

def get_portfolio():
    token = get_token()
    if not token:
        print("❌ Token not found")
        return
    
    HEADERS = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    
    print('💰 Fetching portfolio...\n')
    
    # Get holdings
    h_resp = requests.get(f'{API_BASE}/portfolio/long-term-holdings', headers=HEADERS, timeout=30)
    holdings_data = h_resp.json()
    
    # Get funds
    f_resp = requests.get(f'{API_BASE}/user/get-funds-and-margin', headers=HEADERS, timeout=30)
    funds_data = f_resp.json()
    
    # Funds
    if funds_data.get('status') == 'success':
        funds = funds_data.get('data', {})
        avail = funds.get('available_margin') or funds.get('net_balance') or 0
        print(f'💵 Available Funds: ₹{avail:,.2f}\n')
    
    # Holdings
    if holdings_data.get('status') == 'success':
        holdings = holdings_data.get('data', [])
        if not holdings:
            print('📭 No holdings')
            return
        
        print(f'📈 Holdings ({len(holdings)}):\n')
        
        total_inv = 0
        total_cur = 0
        
        for h in holdings:
            sym = h.get('trading_symbol', 'N/A')
            qty = h.get('quantity', 0)
            avg = h.get('average_price', 0)
            last = h.get('last_price', 0)
            
            inv = qty * avg
            cur = qty * last
            pnl = cur - inv
            
            total_inv += inv
            total_cur += cur
            
            emoji = '🟢' if pnl >= 0 else '🔴'
            print(f'{emoji} {sym}: {qty} @ ₹{avg:.2f} → ₹{last:.2f} | P&L: ₹{pnl:,.2f}')
        
        total_pnl = total_cur - total_inv
        pct = (total_pnl / total_inv * 100) if total_inv else 0
        
        print(f'\n💼 Total: ₹{total_cur:,.2f} (P&L: ₹{total_pnl:,.2f}, {pct:+.1f}%)')
    else:
        print(f'❌ Error: {holdings_data.get("message", "Unknown")}')

if __name__ == '__main__':
    get_portfolio()
