#!/bin/bash
# Predictive Error Analysis - Main Script

set -e

LOG_DIR="$HOME/.openclaw/workspace/memory"
PATTERNS_FILE="$LOG_DIR/learning-patterns.yaml"

# Create logs directory if needed
mkdir -p "$LOG_DIR"

echo "=== Predictive Error Analysis ==="
echo "Timestamp: $(date -Iseconds)"
echo ""

# 1. Memory Analysis
echo "## Memory Analysis"
MEM_TOTAL=$(free -m | awk '/^Mem:/ {print $2}')
MEM_USED=$(free -m | awk '/^Mem:/ {print $3}')
MEM_AVAIL=$(free -m | awk '/^Mem:/ {print $7}')
MEM_PCT=$((MEM_USED * 100 / MEM_TOTAL))

echo "Memory: ${MEM_USED}M / ${MEM_TOTAL}M (${MEM_PCT}% used, ${MEM_AVAIL}M available)"

if [ $MEM_PCT -gt 90 ]; then
    echo "⚠️  CRITICAL: Memory usage above 90%"
    echo "  - Consider killing memory-heavy processes"
    echo "  - Check for memory leaks"
elif [ $MEM_PCT -gt 80 ]; then
    echo "⚠️  WARNING: Memory usage above 80%"
fi

# 2. Disk Analysis
echo ""
echo "## Disk Analysis"
df -h / | tail -1 | awk '{print "Disk: "$3" / "$2" ("$5" used)"}'

DISK_PCT=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
if [ "$DISK_PCT" -gt 90 ]; then
    echo "⚠️  CRITICAL: Disk usage above 90%"
    echo "  - Run: du -sh /var/log/* | sort -h | tail -10"
    echo "  - Run: journalctl --vacuum-time=3d"
elif [ "$DISK_PCT" -gt 80 ]; then
    echo "⚠️  WARNING: Disk usage above 80%"
fi

# 3. Load Average Analysis
echo ""
echo "## Load Analysis"
cat /proc/loadavg | awk '{print "Load: "$1" "$2" "$3" (1/5/15 min)"}'

NPROC=$(nproc)
LOAD_1=$(cat /proc/loadavg | awk '{print $1}' | cut -d. -f1)
if [ "$LOAD_1" -gt "$NPROC" ]; then
    echo "⚠️  WARNING: 1-min load ($LOAD_1) exceeds CPU count ($NPROC)"
fi

# 4. Process Count
echo ""
echo "## Process Analysis"
PROC_COUNT=$(ps aux | wc -l)
ZOMBIE_COUNT=$(ps aux | awk '$8 ~ /Z/ {print}' | wc -l)
echo "Processes: $PROC_COUNT total, $ZOMBIE_COUNT zombies"

if [ "$ZOMBIE_COUNT" -gt 10 ]; then
    echo "⚠️  WARNING: High zombie process count"
fi

# 5. Network Connection Analysis
echo ""
echo "## Network Analysis"
CONN_COUNT=$(ss -tuln | wc -l)
echo "Listening connections: $CONN_COUNT"

# 6. Recent Errors in Logs
echo ""
echo "## Recent Errors (last 1h)"
ERROR_COUNT=$(journalctl -p err --since "1 hour ago" 2>/dev/null | wc -l)
WARN_COUNT=$(journalctl -p warning --since "1 hour ago" 2>/dev/null | wc -l)
echo "Errors: $ERROR_COUNT, Warnings: $WARN_COUNT"

if [ "$ERROR_COUNT" -gt 50 ]; then
    echo "⚠️  CRITICAL: High error rate in last hour"
    echo "Recent errors:"
    journalctl -p err --since "1 hour ago" -n 5 --no-pager 2>/dev/null || true
fi

# 7. Prediction Summary
echo ""
echo "=== Prediction Summary ==="

# Calculate prediction based on patterns
RISK_SCORE=0

[ "$MEM_PCT" -gt 80 ] && RISK_SCORE=$((RISK_SCORE + 20))
[ "$MEM_PCT" -gt 90 ] && RISK_SCORE=$((RISK_SCORE + 30))
[ "$DISK_PCT" -gt 80 ] && RISK_SCORE=$((RISK_SCORE + 20))
[ "$DISK_PCT" -gt 90 ] && RISK_SCORE=$((RISK_SCORE + 30))
[ "$LOAD_1" -gt "$NPROC" ] && RISK_SCORE=$((RISK_SCORE + 15))
[ "$ZOMBIE_COUNT" -gt 10 ] && RISK_SCORE=$((RISK_SCORE + 10))
[ "$ERROR_COUNT" -gt 50 ] && RISK_SCORE=$((RISK_SCORE + 25))

echo "Risk Score: $RISK_SCORE/100"

if [ "$RISK_SCORE" -gt 70 ]; then
    echo "🔴 HIGH RISK: Immediate action recommended"
    echo "  - Check system resources"
    echo "  - Review error logs"
    echo "  - Consider restart of problematic services"
elif [ "$RISK_SCORE" -gt 40 ]; then
    echo "🟡 MEDIUM RISK: Monitor closely"
elif [ "$RISK_SCORE" -gt 20 ]; then
    echo "🟢 LOW RISK: System healthy"
else
    echo "✅ SYSTEM STABLE: No issues detected"
fi

# Save prediction to learning patterns
if [ -f "$PATTERNS_FILE" ]; then
    # Append prediction to file
    echo "- timestamp: $(date -Iseconds)" >> "$PATTERNS_FILE.tmp"
    echo "  risk_score: $RISK_SCORE" >> "$PATTERNS_FILE.tmp"
    echo "  memory_pct: $MEM_PCT" >> "$PATTERNS_FILE.tmp"
    echo "  disk_pct: $DISK_PCT" >> "$PATTERNS_FILE.tmp"
    echo "  error_count: $ERROR_COUNT" >> "$PATTERNS_FILE.tmp"
fi