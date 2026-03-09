# Predictive Error Analysis Skill

Detects system patterns before failures occur.

## Purpose

Analyze system logs, application behavior, and resource usage to predict potential failures before they happen.

## Capabilities

- Monitor journalctl, syslog, application logs
- Detect patterns that precede failures
- Suggest preventive actions
- Learn from false positives/negatives

## Commands

### Analyze Logs
```bash
# Check recent system logs for warning patterns
journalctl -p warning --since "1 hour ago" -n 100
```

### Check Resource Trends
```bash
# Memory pressure
free -m
cat /proc/meminfo | grep -E "(MemAvailable|MemFree|MemTotal)"

# Disk pressure
df -h
df -i

# CPU load trends
cat /proc/loadavg
uptime
```

### Network Health
```bash
# Connection states
ss -tuln | wc -l
netstat -s | grep -E "(failed|errors|dropped)"
```

## Pattern Recognition

### Memory Exhaustion Pattern
1. Increasing memory usage over time
2. Growing cache vs available ratio
3. OOM killer triggers in logs
4. **Prediction:** Memory exhaustion in X hours

### Disk Space Pattern
1. Log file growth rate
2. Cache directory size trends
3. Temp file accumulation
4. **Prediction:** Disk full in X hours

### Network Degradation Pattern
1. Increasing connection timeouts
2. Rising packet loss rates
3. DNS resolution delays
4. **Prediction:** Network instability

### Process Instability Pattern
1. Zombie process accumulation
2. Increasing process count
3. CPU time vs wall time divergence
4. **Prediction:** System hang

## Learning

Records predictions and outcomes in `memory/learning-patterns.yaml`:
- Pattern detected
- Prediction made
- Actual outcome
- Accuracy score

## Integration

Integrates with HEARTBEAT.md for proactive alerts during heartbeat checks.