# Kernel Observer Skill

_Deepest system integration via eBPF - observe syscalls, processes, network, filesystem at kernel level._

---

## Overview

This skill provides kernel-level observability using eBPF (Extended Berkeley Packet Filter). It gives OpenClaw "X-ray vision" into the system - every syscall, file access, network connection, process spawn visible in real-time.

**What eBPF Provides:**
- Syscall tracing (every execve, open, read, write)
- Filesystem monitoring (every file access)
- Network observability (every packet, connection)
- Process lifecycle (spawn, exit, signals)
- Kernel events (scheduler, memory, block I/O)

---

## Prerequisites

```bash
# Install bpftrace (high-level tracing language)
sudo dnf install bpftrace bpftrace-tools

# Install bpftool (BPF utility)
sudo dnf install bpftool

# Verify kernel support
grep CONFIG_BPF /boot/config-$(uname -r)
# Should show: CONFIG_BPF_SYSCALL=y, CONFIG_BPF_JIT=y

# Check BPF LSM support (for security hooks)
grep CONFIG_BPF_LSM /boot/config-$(uname -r)
# Should show: CONFIG_BPF_LSM=y
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Space                                │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │ OpenClaw    │◄────│ Event Bridge │◄────│ bpftrace    │   │
│  │ Gateway     │     │ (WebSocket) │     │ (eBPF)      │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                 │            │
└─────────────────────────────────────────────────│────────────┘
                                                  │
┌─────────────────────────────────────────────────│────────────┐
│                     Kernel                      ▼            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                    eBPF Programs                       │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐        │   │
│  │  │ Syscall    │ │ Filesystem │ │ Network    │        │   │
│  │  │ Tracer     │ │ Watcher     │ │ Monitor    │        │   │
│  │  └────────────┘ └────────────┘ └────────────┘        │   │
│  │         │              │              │               │   │
│  │         └──────────────┼──────────────┘               │   │
│  │                        ▼                               │   │
│  │              ┌─────────────────┐                       │   │
│  │              │ Perf Buffer    │                       │   │
│  │              │ (events)       │                       │   │
│  │              └─────────────────┘                       │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                 Kernel Subsystems                     │   │
│  │  System Calls │ VFS │ Network Stack │ Scheduler      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Usage

### Start Kernel Observation

```
skill: kernel-observer
action: start
scope: [syscalls|files|network|processes|all]
filter: [optional process/command filter]
```

### Example Commands

```bash
# Start monitoring all syscalls
openclaw skill kernel-observer start --scope syscalls

# Monitor file access for specific directory
openclaw skill kernel-observer start --scope files --filter /home/csilva/projects

# Monitor network connections
openclaw skill kernel-observer start --scope network

# Monitor process spawns
openclaw skill kernel-observer start --scope processes

# Full observation (all scopes)
openclaw skill kernel-observer start --scope all
```

### Stop Observation

```
skill: kernel-observer
action: stop
```

### Query Events

```
skill: kernel-observer
action: query
filter: [process|syscall|file|time range]
```

---

## eBPF Scripts

### Syscall Monitor (syscalls.bt)

```bpftrace
#!/usr/bin/bpftrace
// Trace all execve syscalls to see every command execution
tracepoint:syscalls:sys_enter_execve
{
    printf("[%s] %s -> %s\n", strftime("%H:%M:%S", nsecs), comm, str(args->filename));
}
```

### File Access Monitor (files.bt)

```bpftrace
#!/usr/bin/bpftrace
// Trace file opens
tracepoint:syscalls:sys_enter_openat
{
    printf("[%s] %s (pid:%d) opens: %s\n", 
           strftime("%H:%M:%S", nsecs), 
           comm, pid, str(args->filename));
}
```

### Network Monitor (network.bt)

```bpftrace
#!/usr/bin/bpftrace
// Trace TCP connections
kprobe:tcp_connect
{
    printf("[%s] %s (pid:%d) TCP connect\n", 
           strftime("%H:%M:%S", nsecs), comm, pid);
}

kprobe:tcp_accept
{
    printf("[%s] %s (pid:%d) TCP accept\n", 
           strftime("%H:%M:%S", nsecs), comm, pid);
}
```

### Process Monitor (processes.bt)

```bpftrace
#!/usr/bin/bpftrace
// Trace process lifecycle
tracepoint:sched:sched_process_fork
{
    printf("[%s] FORK: %s (pid:%d) -> (pid:%d)\n", 
           strftime("%H:%M:%S", nsecs), 
           args->parent_comm, args->parent_pid, args->child_pid);
}

tracepoint:sched:sched_process_exit
{
    printf("[%s] EXIT: %s (pid:%d)\n", 
           strftime("%H:%M:%S", nsecs), comm, pid);
}
```

---

## Integration with OpenClaw

### Event Bridge (Node.js)

```javascript
// kernel-observer-bridge.js
const { spawn } = require('child_process');
const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:18789/kernel-events');

function startTrace(script) {
    const bpftrace = spawn('sudo', ['bpftrace', '-e', script]);
    
    bpftrace.stdout.on('data', (data) => {
        const event = parseBpftraceOutput(data.toString());
        ws.send(JSON.stringify({
            type: 'kernel_event',
            timestamp: Date.now(),
            data: event
        }));
    });
    
    bpftrace.stderr.on('data', (data) => {
        console.error('bpftrace error:', data.toString());
    });
    
    return bpftrace;
}

function parseBpftraceOutput(line) {
    // Parse: [HH:MM:SS] process (pid:123) action
    const match = line.match(/\[(\d{2}:\d{2}:\d{2})\] (\S+) \(pid:(\d+)\) (.+)/);
    if (match) {
        return {
            time: match[1],
            process: match[2],
            pid: parseInt(match[3]),
            action: match[4]
        };
    }
    return { raw: line };
}

module.exports = { startTrace };
```

### OpenClaw Hook (hooks/kernel-events.js)

```javascript
// hooks/kernel-events.js
module.exports = {
    name: 'kernel-events',
    
    // Listen for kernel events
    async onEvent(event) {
        if (event.type !== 'kernel_event') return;
        
        // Extract patterns
        const { process, action } = event.data;
        
        // Update heuristics based on observations
        if (action.includes('opens:') && process === 'code') {
            // User is working on code
            await this.updateActivityContext('coding');
        }
        
        if (action.includes('TCP connect') && process === 'firefox') {
            // User browsing web
            await this.updateActivityContext('browsing');
        }
        
        // Log to memory for pattern extraction
        await this.logEvent({
            type: 'kernel_event',
            process,
            action,
            timestamp: event.timestamp
        });
    }
};
```

---

## Learning from Kernel Events

### Pattern Extraction

```javascript
// Analyze kernel events to learn user patterns
async function extractPatterns(events) {
    const patterns = {};
    
    for (const event of events) {
        const key = `${event.process}:${event.action}`;
        patterns[key] = (patterns[key] || 0) + 1;
    }
    
    // Find recurring patterns
    const learned = Object.entries(patterns)
        .filter(([_, count]) => count > 10) // threshold
        .map(([pattern, count]) => ({
            pattern,
            frequency: count,
            confidence: calculateConfidence(count, events.length)
        }));
    
    return learned;
}

// Example learned patterns:
// - "git status" every 5 minutes → working on code
// - "docker ps" every 30 seconds → debugging containers
// - "npm test" after "vim" → TDD workflow
```

### Heuristic Updates

```javascript
// Automatically update HEURISTICS.md based on kernel observations
async function updateHeuristics(patterns) {
    const heuristicsFile = 'HEURISTICS.md';
    let content = await fs.readFile(heuristicsFile, 'utf-8');
    
    for (const pattern of patterns) {
        if (pattern.frequency > 100 && pattern.confidence > 0.8) {
            // Add to heuristics
            content += `\n- id: OBS-${Date.now()}
  pattern: "${pattern.process} ${pattern.action}"
  heuristic: "Detected ${pattern.frequency} times, confidence ${pattern.confidence}"
  confidence: ${pattern.confidence}
  source: "kernel_observation"
  created: ${new Date().toISOString()}`;
        }
    }
    
    await fs.writeFile(heuristicsFile, content);
}
```

---

## Security Considerations

### What eBPF Can See

| Category | Visibility | Sensitivity |
|----------|------------|-------------|
| Syscalls | ALL | High |
| File access | ALL | High |
| Network | ALL packets | High |
| Process memory | Read possible | Critical |
| Kernel memory | Limited | Critical |

### What It Cannot See

| Category | Limitation |
|----------|------------|
| Encrypted content | TLS/SSL encrypted |
| Memory content | Needs explicit probes |
| Kernel internals | Limited without privileges |

### Privacy Safeguards

```javascript
// Configurable privacy filters
const privacyConfig = {
    // Exclude sensitive paths
    excludePaths: [
        '/home/csilva/.ssh/',
        '/home/csilva/.gnupg/',
        '/home/csilva/.password-store/',
    ],
    
    // Exclude processes
    excludeProcesses: [
        'password-manager',
        'keepassxc',
    ],
    
    // Redact patterns
    redactPatterns: [
        /password=\S+/g,
        /token=\S+/g,
        /key=\S+/g,
    ]
};
```

---

## Performance Impact

| Metric | Impact | Mitigation |
|--------|--------|------------|
| CPU | 0.1-2% per probe | Filter early |
| Memory | ~10MB per program | Limit programs |
| Latency | Microseconds | Use perf buffers |
| Disk I/O | Events written | Buffer + batch |

### Optimization

```bpftrace
// Use filters to reduce overhead
tracepoint:syscalls:sys_enter_execve
/comm != "systemd" && comm != "dbus-daemon"/
{
    // Only trace user processes
    printf("%s -> %s\n", comm, str(args->filename));
}
```

---

## Installation

```bash
# Install dependencies
sudo dnf install bpftrace bpftool

# Create skill directory
mkdir -p ~/.openclaw/workspace/skills/kernel-observer

# Install eBPF scripts
cp scripts/*.bt ~/.openclaw/workspace/skills/kernel-observer/

# Start the bridge
node ~/.openclaw/workspace/skills/kernel-observer/bridge.js
```

---

## Example Output

```json
{
  "type": "kernel_event",
  "timestamp": "2026-03-15T13:30:00.123Z",
  "data": {
    "process": "code",
    "pid": 12345,
    "action": "opens: /home/csilva/projects/app/src/main.rs",
    "category": "file_access"
  }
}
```

```json
{
  "type": "kernel_event",
  "timestamp": "2026-03-15T13:30:05.456Z",
  "data": {
    "process": "git",
    "pid": 12346,
    "action": "execve: git status",
    "category": "syscall"
  }
}
```

---

## Next Steps

1. **Install bpftrace** - `sudo dnf install bpftrace`
2. **Run test script** - `sudo bpftrace -e 'tracepoint:syscalls:sys_enter_execve { printf("%s\n", comm); }'`
3. **Create bridge** - Node.js WebSocket to Gateway
4. **Add hooks** - Process events in OpenClaw
5. **Learn patterns** - Extract heuristics from observations

---

_This skill requires root privileges for eBPF programs. The kernel (6.12.0) supports all required features._