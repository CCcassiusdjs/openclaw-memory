# Intervention Skill - Automatic System Fixes

_Automatic or semi-automatic intervention when problems are detected._

---

## Overview

This skill enables OpenClaw to take action on detected problems, not just observe them.

**Intervention Levels:**
1. **Notify** → Tell user (current capability)
2. **Ask** → Request permission to act
3. **Auto-fix** → Fix automatically (whitelisted only)
4. **Block** → Prevent dangerous operations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Intervention Flow                        │
│                                                              │
│  Problem Detected (Kernel Observer / Heartbeat)             │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────┐                                        │
│  │  Rule Engine    │                                        │
│  │  - Match rule   │                                        │
│  │  - Check level  │                                        │
│  └────────┬────────┘                                        │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐                                        │
│  │  Permission     │                                        │
│  │  Check          │                                        │
│  └────────┬────────┘                                        │
│           │                                                  │
│     ┌─────┼─────┐                                           │
│     ▼     ▼     ▼                                           │
│  Notify  Ask   Auto-fix                                     │
│     │     │     │                                           │
│     │     │     └──► Execute whitelisted fix               │
│     │     │                                                  │
│     │     └────► Wait for user response                    │
│     │                                                        │
│     └──────► Send notification                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Intervention Rules

```yaml
# ~/.openclaw/workspace/intervention-rules.yaml

rules:
  # === DISK MANAGEMENT ===
  
  - name: disk_cleanup_logs
    trigger:
      condition: disk_usage > 85%
      mount: /home
    level: ask  # Notify and ask
    message: "Disk ${mount} is ${percent}% full. Clean up old logs?"
    actions:
      - name: "Clean logs older than 30 days"
        command: "find ~/.openclaw/logs -name '*.log' -mtime +30 -delete"
      - name: "Clean cache"
        command: "rm -rf ~/.cache/*"
      - name: "Show disk usage"
        command: "du -sh ~/* | sort -hr | head -10"
    rate_limit: 1h

  - name: disk_critical_cleanup
    trigger:
      condition: disk_usage > 95%
      mount: /home
    level: auto  # Auto-fix
    message: "CRITICAL: Disk ${mount} is ${percent}% full. Auto-cleaning..."
    auto_actions:
      - command: "find ~/.openclaw/logs -name '*.log' -mtime +7 -delete"
      - command: "rm -rf ~/.cache/*"
    notify_after: true  # Tell user what was done
    rate_limit: null

  # === PROCESS MANAGEMENT ===
  
  - name: runaway_process_kill
    trigger:
      condition: cpu_usage > 95% for 5m
      exclude_processes: [cargo, npm, yarn, make]  # Don't kill these
    level: ask
    message: "Process ${process} (pid ${pid}) using ${cpu}% CPU for 5m. Kill it?"
    actions:
      - name: "Kill process"
        command: "kill ${pid}"
      - name: "Show process details"
        command: "ps -fp ${pid}"
    rate_limit: 30m

  - name: zombie_process_cleanup
    trigger:
      condition: zombie_processes > 10
    level: auto
    message: "Cleaned ${count} zombie processes"
    auto_actions:
      - command: "ps aux | awk '$8 ~ /Z/ {print $2}' | xargs -r kill -9"
    rate_limit: 1h

  # === MEMORY MANAGEMENT ===
  
  - name: memory_low_cleanup
    trigger:
      condition: memory_available < 500MB
    level: ask
    message: "Memory critically low (${available}MB available). Free memory?"
    actions:
      - name: "Drop caches"
        command: "sync && echo 3 | sudo tee /proc/sys/vm/drop_caches"
      - name: "Show memory usage"
        command: "free -h"
    rate_limit: 15m

  # === SECURITY ===
  
  - name: suspicious_ssh_login
    trigger:
      condition: ssh_login_from_unknown_ip
    level: notify  # Always notify, never auto-block
    message: "Security: SSH login from ${ip} (${location})"
    channels: [desktop, whatsapp, email]
    rate_limit: null  # Always notify

  - name: brute_force_block
    trigger:
      condition: failed_login_attempts > 10 from same_ip
    level: auto
    message: "Blocked IP ${ip} for brute force attempts"
    auto_actions:
      - command: "sudo iptables -A INPUT -s ${ip} -j DROP"
    rate_limit: null

  # === SYSTEM HEALTH ===
  
  - name: service_restart
    trigger:
      condition: service_failed critical_service
    level: ask
    message: "Service ${service} failed. Restart?"
    actions:
      - name: "Restart service"
        command: "sudo systemctl restart ${service}"
      - name: "Show logs"
        command: "journalctl -u ${service} -n 50"
    rate_limit: 10m

  # === BUILD/DEVELOPMENT ===
  
  - name: build_cache_cleanup
    trigger:
      condition: target_directory_size > 5GB
      path: "*/target"
    level: ask
    message: "Rust target directory is ${size}. Clean up?"
    actions:
      - name: "Clean target"
        command: "cargo clean --manifest-path ${path}/Cargo.toml"
    rate_limit: 1d

---

## Permission Levels

| Level | Description | Requires User |
|-------|-------------|---------------|
| `notify` | Tell user, no action | No |
| `ask` | Request permission | Yes, always |
| `auto` | Automatic fix | No (whitelist) |
| `block` | Prevent operation | No |

### Whitelist for Auto-Fix

```yaml
whitelisted_auto_actions:
  # Safe actions that can run automatically
  - name: cleanup_logs
    command: "find ~/.openclaw/logs -name '*.log' -mtime +7 -delete"
    
  - name: cleanup_cache
    command: "rm -rf ~/.cache/*"
    
  - name: drop_caches
    command: "sync && echo 3 | sudo tee /proc/sys/vm/drop_caches"
    
  - name: kill_zombie
    command: "ps aux | awk '$8 ~ /Z/ {print $2}' | xargs -r kill -9"
    
  - name: cleanup_target
    command: "cargo clean"
```

---

## Implementation

### Intervention Manager (Node.js)

```javascript
class InterventionManager {
    constructor() {
        this.rules = [];
        this.whitelist = new Map();
        this.permissionQueue = new Map();
    }
    
    async handleEvent(event, kernelObserver) {
        // Find matching rule
        const rule = this.findMatchingRule(event);
        if (!rule) return;
        
        // Check rate limit
        if (!this.checkRateLimit(rule)) return;
        
        // Handle based on level
        switch (rule.level) {
            case 'notify':
                await this.notify(rule, event);
                break;
            case 'ask':
                await this.ask(rule, event);
                break;
            case 'auto':
                await this.autoFix(rule, event);
                break;
            case 'block':
                await this.block(rule, event);
                break;
        }
    }
    
    findMatchingRule(event) {
        return this.rules.find(rule => rule.matches(event));
    }
    
    checkRateLimit(rule) {
        const last = this.lastSent.get(rule.name);
        if (!last) return true;
        
        const now = Date.now();
        const limitMs = this.parseDuration(rule.rate_limit);
        
        return (now - last) > limitMs;
    }
    
    async notify(rule, event) {
        const message = this.renderMessage(rule.message, event);
        await notificationManager.send({
            title: "OpenClaw Alert",
            message: message,
            priority: rule.priority || 'medium',
            channels: rule.channels || ['desktop']
        });
        this.lastSent.set(rule.name, Date.now());
    }
    
    async ask(rule, event) {
        const message = this.renderMessage(rule.message, event);
        
        // Send notification with action buttons
        const response = await notificationManager.ask(
            message,
            { options: rule.actions.map(a => a.name) }
        );
        
        // Handle response
        if (response) {
            const action = rule.actions.find(a => a.name === response);
            if (action) {
                await this.executeAction(action, event);
            }
        }
    }
    
    async autoFix(rule, event) {
        // Verify whitelist
        for (const action of rule.auto_actions) {
            if (!this.isWhitelisted(action.command)) {
                console.error(`Auto-action not whitelisted: ${action.command}`);
                continue;
            }
            
            await this.executeAction(action, event);
        }
        
        // Notify user what was done
        if (rule.notify_after) {
            await this.notify(rule, event);
        }
    }
    
    async block(rule, event) {
        // Log the block
        await logIntervention(rule, event, 'blocked');
        
        // Prevent the operation (requires kernel-level integration)
        // This would need to be implemented in the eBPF layer
    }
    
    async executeAction(action, event) {
        const command = this.renderCommand(action.command, event);
        
        // Log the intervention
        await logIntervention(action, event, 'executed');
        
        // Execute the command
        const result = await exec(command);
        
        return result;
    }
    
    isWhitelisted(command) {
        // Check against whitelist
        return this.whitelist.has(command);
    }
}
```

---

## Safety Mechanisms

### 1. Confirmation for Destructive Actions

```javascript
// Never auto-delete user data
const DESTRUCTIVE_PATTERNS = [
    /rm\s+-rf\s+~\//,  // rm -rf ~/
    /rm\s+-rf\s+\/home/,  // rm -rf /home
    /mkfs/,  // Format disk
    /dd\s+if=.*of=\/dev/,  // dd to device
];

function isDestructive(command) {
    return DESTRUCTIVE_PATTERNS.some(p => p.test(command));
}

// Always ask for destructive actions
async function executeAction(action, event) {
    if (isDestructive(action.command)) {
        // Force ask level, never auto
        return await this.ask({ 
            ...action, 
            level: 'ask',
            message: `DANGEROUS: ${action.command}. Proceed?`
        }, event);
    }
    
    // ... execute normally
}
```

### 2. Rollback Mechanism

```javascript
// Before executing, save rollback state
async function executeWithRollback(action, event) {
    const rollback = await this.createRollback(action);
    
    try {
        const result = await this.executeAction(action, event);
        return result;
    } catch (error) {
        // Automatic rollback on failure
        await rollback.restore();
        throw error;
    }
}

async function createRollback(action) {
    // For file deletions, move to trash instead
    // For service restarts, save previous state
    // For configuration changes, backup old config
}
```

### 3. Audit Log

```javascript
// Log all interventions
async function logIntervention(rule, event, status) {
    const log = {
        timestamp: new Date().toISOString(),
        rule: rule.name,
        event: event,
        status: status,  // 'executed', 'blocked', 'asked', 'rejected'
        user: process.env.USER
    };
    
    await fs.appendFile(
        '~/.openclaw/logs/interventions.log',
        JSON.stringify(log) + '\n'
    );
}
```

---

## Examples

### Example 1: Disk Cleanup

```
Event: disk_usage(/home) = 92%

Rule matches: disk_cleanup_logs

Level: ask

Notification:
  "Disk /home is 92% full. Clean up old logs?"
  [Clean logs older than 30 days] [Clean cache] [Show disk usage]

User clicks: "Clean logs older than 30 days"

Action:
  find ~/.openclaw/logs -name '*.log' -mtime +30 -delete

Result:
  "Cleaned 2.3GB of old logs. Disk now at 85%."
```

### Example 2: Runaway Process

```
Event: process(cargo) CPU 98% for 5 minutes

Rule matches: runaway_process_kill

Level: ask

Notification:
  "Process cargo (pid 12345) using 98% CPU for 5m. Kill it?"
  [Kill process] [Show process details]

User clicks: "Show process details"

Action:
  ps -fp 12345

Result shows:
  cargo build --release (compiling your project)

User decides: Don't kill, let it finish
```

### Example 3: Critical Disk (Auto-Fix)

```
Event: disk_usage(/home) = 97%

Rule matches: disk_critical_cleanup

Level: auto

Auto-actions:
  find ~/.openclaw/logs -name '*.log' -mtime +7 -delete
  rm -rf ~/.cache/*

Executed automatically.

After-notification:
  "CRITICAL: Disk was 97% full. Auto-cleaned 5GB. Now at 90%."
```

---

## Configuration

```bash
# Install intervention skill
mkdir -p ~/.openclaw/workspace/skills/intervention

# Copy rules
cp intervention-rules.yaml ~/.openclaw/workspace/

# Edit rules for your system
vim ~/.openclaw/workspace/intervention-rules.yaml
```

---

## Testing

```bash
# Test notification
node -e "require('./manager').test()"

# Simulate event
node -e "require('./manager').simulate('disk_critical_cleanup', { percent: 95 })"

# View intervention log
tail -f ~/.openclaw/logs/interventions.log
```

---

## Integration with Kernel Observer

```javascript
// In kernel-observer bridge
kernelObserver.on('event', async (event) => {
    // Check intervention rules
    await interventionManager.handleEvent(event, kernelObserver);
});
```

---

_This skill bridges the gap between "I see a problem" and "I can fix it."_