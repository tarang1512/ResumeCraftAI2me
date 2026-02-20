#!/bin/bash
# Stop Auto Trading Bot

echo "=== Stopping TradeBot ==="

PID=$(pgrep -f "auto_trade_runner.py")
if [ -n "$PID" ]; then
    echo "[+] Stopping auto-trader (PID: $PID)..."
    kill -TERM $PID
    sleep 2
    if pgrep -f "auto_trade_runner.py" > /dev/null; then
        echo "[!] Force killing..."
        kill -9 $PID
    fi
    echo "[+] Auto-trader stopped."
else
    echo "[!] Auto-trader not running."
fi
