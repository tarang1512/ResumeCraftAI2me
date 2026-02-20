#!/bin/bash
# Auto Trading Bot Launcher
# Runs during market hours (9:15 AM - 3:30 PM IST)

cd /home/ubuntu/.openclaw/workspace

echo "=== TradeBot Auto-Trader ==="
echo "Starting at $(date)"

check_market_hours() {
    # Current hour in IST (UTC+5:30)
    # 9:15 AM IST = 3:45 AM UTC
    # 3:30 PM IST = 10:00 AM UTC
    hour=$(date -u +%H)
    minute=$(date -u +%M)
    
    # Convert to minutes for comparison
    current_mins=$((hour * 60 + minute))
    
    # Market open: 3:45 AM UTC (225 mins)
    # Market close: 10:00 AM UTC (600 mins)
    if [ "$current_mins" -ge 225 ] && [ "$current_mins" -le 600 ]; then
        return 0  # Market is open
    else
        return 1  # Market is closed
    fi
}

if ! check_market_hours; then
    echo "[!] Market is closed. Will wait for market open."
    echo "    Market hours: 9:15 AM - 3:30 PM IST"
    exit 0
fi

echo "[+] Market is OPEN. Starting auto-trader..."

# Check if already running
if pgrep -f "auto_trade_runner.py" > /dev/null; then
    echo "[!] Auto-trader already running. Exiting."
    exit 0
fi

# Run the bot
python3 upstox_bot/auto_trade_runner.py
