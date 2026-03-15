# Notification Skill - Proactive System Alerts

_Send desktop notifications, sounds, and messages when you're not looking._

---

## Overview

This skill enables OpenClaw to proactively reach you when important events occur, even when you're not actively in a chat session.

**Channels:**
- Desktop notifications (notify-send)
- System sounds/beeps
- WhatsApp messages (already configured)
- Email alerts (already configured)
- Terminal wall messages

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Trigger Sources                          │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ Kernel      │ │ Cron        │ │ Threshold   │            │
│  │ Observer    │ │ Heartbeat   │ │ Alerts      │            │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘            │
│         │               │               │                     │
│         └───────────────┼───────────────┘                     │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Notification Manager                  │   │
│  │  ┌─────────────────────────────────────────────────┐  │   │
│  │  │  Rules Engine                                    │  │   │
│  │  │  - Priority (critical, high, medium, low)       │  │   │
│  │  │  - Channel selection                             │  │   │
│  │  │  - Rate limiting                                 │  │   │
│  │  │  - Quiet hours                                   │  │   │
│  │  └─────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
│                         │                                    │
│         ┌───────────────┼───────────────┐                   │
│         ▼               ▼               ▼                    │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Desktop  │    │ WhatsApp │    │ Email    │              │
│  │ notify   │    │ message  │    │ alert    │              │
│  └──────────┘    └──────────┘    └──────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Notification Rules

```yaml
# ~/.openclaw/workspace/notification-rules.yaml

rules:
  - name: disk_critical
    trigger: disk_usage > 90%
    priority: critical
    channels:
      - desktop
      - whatsapp
      - email
    message: "Disk ${mount} is ${percent}% full. Cleanup needed."
    rate_limit: 1h  # Don't spam more than once per hour
    quiet_hours: null  # Always notify

  - name: cpu_overload
    trigger: cpu_usage > 95% for 5m
    priority: high
    channels:
      - desktop
    message: "CPU overload detected: ${process} using ${percent}%"
    rate_limit: 30m

  - name: memory_low
    trigger: memory_available < 500MB
    priority: high
    channels:
      - desktop
      - whatsapp
    message: "Memory critically low: ${available}MB available"
    rate_limit: 15m

  - name: build_failed
    trigger: process_exit(cargo, code != 0)
    priority: medium
    channels:
      - desktop
    message: "Build failed: ${process} exited with code ${code}"
    rate_limit: 5m

  - name: unusual_activity
    trigger: process_spawn_at(03:00)
    priority: low
    channels:
      - log
    message: "Unusual activity at 3am: ${process}"
    quiet_hours: "23:00-07:00"  # Don't wake user

  - name: security_event
    trigger: ssh_login_from_unknown_ip
    priority: critical
    channels:
      - desktop
      - whatsapp
      - email
    message: "Security: SSH login from unknown IP ${ip}"
    rate_limit: null  # Always notify immediately
```

---

## Desktop Notifications (notify-send)

```bash
# Simple notification
notify-send "OpenClaw Alert" "Disk /home is 92% full" --urgency=critical

# With icon
notify-send "OpenClaw" "Build complete" --icon=dialog-information

# With actions (requires notification daemon support)
notify-send "OpenClaw" "Update available. Install?" \
    --action=install="Install Now" \
    --action=later="Later"
```

### Implementation (Node.js)

```javascript
const { exec } = require('child_process');

class DesktopNotifier {
    async send(title, message, options = {}) {
        const urgency = options.urgency || 'normal'; // low, normal, critical
        const icon = options.icon ? `--icon=${options.icon}` : '';
        const expire = options.expire ? `--expire-time=${options.expire}` : '';
        
        const cmd = `notify-send "${title}" "${message}" --urgency=${urgency} ${icon} ${expire}`;
        
        return new Promise((resolve, reject) => {
            exec(cmd, (error, stdout, stderr) => {
                if (error) reject(error);
                else resolve(stdout);
            });
        });
    }
}
```

---

## System Sounds

```javascript
const { exec } = require('child_process');

class SoundNotifier {
    async beep(frequency = 1000, duration = 200) {
        // Linux beep (requires beep package)
        return new Promise((resolve, reject) => {
            exec(`beep -f ${frequency} -l ${duration}`, (error) => {
                if (error) {
                    // Fallback: speaker-test
                    exec(`speaker-test -t sine -f ${frequency} -l 1`, resolve);
                } else {
                    resolve();
                }
            });
        });
    }
    
    async alertSound() {
        // Three beeps
        await this.beep(1000, 200);
        await new Promise(r => setTimeout(r, 100));
        await this.beep(1200, 200);
        await new Promise(r => setTimeout(r, 100));
        await this.beep(1500, 300);
    }
}
```

---

## Terminal Wall Messages

```bash
# Broadcast to all terminals
wall "OpenClaw Alert: Disk critical"

# Write to specific terminal
echo "OpenClaw: Build complete" > /dev/pts/0
```

---

## Integration with Kernel Observer

```javascript
// When kernel event triggers notification rule
kernelObserver.on('event', async (event) => {
    const rules = await loadRules();
    
    for (const rule of rules) {
        if (rule.matches(event)) {
            await notificationManager.send({
                rule: rule.name,
                priority: rule.priority,
                channels: rule.channels,
                message: rule.render(event)
            });
        }
    }
});
```

---

## Quiet Hours

```yaml
quiet_hours:
  start: "23:00"
  end: "07:00"
  timezone: "America/Belem"
  
  exceptions:
    - priority: critical  # Always notify critical
    - priority: high      # Notify high priority but delayed
      
  behavior:
    critical: immediate
    high: queue_until_morning
    medium: drop
    low: drop
```

---

## Rate Limiting

```javascript
class RateLimiter {
    constructor() {
        this.lastSent = new Map();
    }
    
    canSend(ruleName, rateLimit) {
        if (!rateLimit) return true;
        
        const last = this.lastSent.get(ruleName);
        if (!last) return true;
        
        const now = Date.now();
        const limitMs = this.parseDuration(rateLimit);
        
        return (now - last) > limitMs;
    }
    
    markSent(ruleName) {
        this.lastSent.set(ruleName, Date.now());
    }
    
    parseDuration(duration) {
        const units = { s: 1000, m: 60000, h: 3600000 };
        const match = duration.match(/^(\d+)([smh])$/);
        return match ? parseInt(match[1]) * units[match[2]] : 0;
    }
}
```

---

## Intervention Levels

### Level 1: Notify (Current)
- Send message to active channels
- User decides action
- Safe, no automatic changes

### Level 2: Suggest and Ask
```javascript
// Ask for permission first
async function cleanupDisk() {
    const response = await notificationManager.ask(
        "Disk 95% full. Clean up old logs?",
        { options: ["Yes", "No", "Show what"] }
    );
    
    if (response === "Yes") {
        await exec("rm -rf ~/.openclaw/logs/*.old");
        await notificationManager.send("Cleaned 2GB of old logs");
    }
}
```

### Level 3: Automatic Intervention (Future)
```javascript
// Requires explicit permission
const ALLOWED_AUTO_ACTIONS = [
    'cleanup_logs',
    'clear_cache',
    'kill_runaway_process'
];

async function autoIntervene(rule, event) {
    if (rule.auto_fix && ALLOWED_AUTO_ACTIONS.includes(rule.auto_fix)) {
        await logIntervention(rule, event);
        await executeFix(rule.auto_fix);
    }
}
```

---

## Installation

```bash
# Desktop notifications (usually pre-installed)
sudo dnf install libnotify

# Beep for sounds
sudo dnf install beep

# Add to notification-rules.yaml
mkdir -p ~/.openclaw/workspace
cp notification-rules.yaml ~/.openclaw/workspace/
```

---

## Usage in OpenClaw

```javascript
// From kernel observer or heartbeat
const { NotificationManager } = require('./skills/notification/manager');

const notifier = new NotificationManager();

// Send alert
await notifier.send({
    title: "OpenClaw Alert",
    message: "CPU usage 95% - cargo build running",
    priority: "high",
    channels: ["desktop", "whatsapp"]
});

// Ask question
const response = await notifier.ask(
    "Unusual process detected: backup-restore at 3am. Intentional?",
    { options: ["Yes", "No, investigate", "Ignore"] }
);
```

---

_This skill bridges the gap between "I see a problem" and "I can tell you about it."_