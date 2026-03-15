#!/bin/bash
#
# Smart Kernel Observer Manager
# 
# Start kernel observer only when needed, stop when idle.
#
# Usage:
#   kernel-observer.sh start    # Start if not running
#   kernel-observer.sh stop     # Stop if running
#   kernel-observer.sh status   # Check status
#   kernel-observer.sh auto      # Auto-start based on conditions
#

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_FILE="/tmp/kernel-observer.log"
PID_FILE="/tmp/kernel-observer.pid"
IDLE_THRESHOLD=1800  # 30 minutes

start_observer() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
        echo "Kernel observer already running (PID: $(cat $PID_FILE))"
        return 0
    fi
    
    echo "Starting kernel observer..."
    sudo node "$SCRIPT_DIR/bridge.js" --scope=all > "$LOG_FILE" 2>&1 &
    echo $! | sudo tee "$PID_FILE" > /dev/null
    
    sleep 2
    if kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        echo "✓ Kernel observer started (PID: $(cat $PID_FILE))"
        return 0
    else
        echo "✗ Failed to start kernel observer"
        cat "$LOG_FILE"
        return 1
    fi
}

stop_observer() {
    if [ ! -f "$PID_FILE" ]; then
        echo "Kernel observer not running"
        return 0
    fi
    
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping kernel observer (PID: $PID)..."
        sudo kill "$PID" 2>/dev/null
        sudo rm -f "$PID_FILE"
        echo "✓ Kernel observer stopped"
    else
        echo "Kernel observer not running (stale PID file)"
        sudo rm -f "$PID_FILE"
    fi
}

check_status() {
    if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        PID=$(cat $PID_FILE)
        MEM=$(ps -p "$PID" -o rss= 2>/dev/null | awk '{printf "%.1f MB", $1/1024}')
        CPU=$(ps -p "$PID" -o %cpu= 2>/dev/null | awk '{printf "%.1f%%", $1}')
        echo "✓ Kernel observer running (PID: $PID, CPU: $CPU, Memory: $MEM)"
        return 0
    else
        echo "✗ Kernel observer not running"
        return 1
    fi
}

auto_start() {
    # Check if already running
    if [ -f "$PID_FILE" ] && kill -0 "$(cat $PID_FILE)" 2>/dev/null; then
        return 0
    fi
    
    # Conditions to start:
    # 1. Gateway is running
    # 2. User is active (not idle)
    # 3. Not on battery (optional)
    
    # Check gateway
    if ! pgrep -f "openclaw gateway" > /dev/null; then
        echo "Gateway not running, skipping"
        return 0
    fi
    
    # Check idle time (if available)
    if command -v xprintidle &> /dev/null; then
        IDLE_MS=$(xprintidle)
        if [ "$IDLE_MS" -gt "$((IDLE_THRESHOLD * 1000))" ]; then
            echo "User idle for $((IDLE_MS / 1000 / 60)) minutes, skipping"
            return 0
        fi
    fi
    
    # Check battery (optional)
    if [ -f /sys/class/power_supply/BAT0/status ]; then
        STATUS=$(cat /sys/class/power_supply/BAT0/status)
        if [ "$STATUS" = "Discharging" ]; then
            echo "On battery, skipping"
            return 0
        fi
    fi
    
    # Start observer
    start_observer
}

case "$1" in
    start)
        start_observer
        ;;
    stop)
        stop_observer
        ;;
    status)
        check_status
        ;;
    auto)
        auto_start
        ;;
    *)
        echo "Usage: $0 {start|stop|status|auto}"
        exit 1
        ;;
esac