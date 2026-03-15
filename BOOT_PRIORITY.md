# OpenClaw Boot Priority Architecture

## Current State

| Service | Type | Starts After | Requires Root |
|---------|------|--------------|---------------|
| **openclaw-gateway** | User service | network-online, basic | No |
| **kernel-observer** | System service | gateway | Yes (eBPF) |
| **notification** | User service | gateway | No |

## Problem

```
Current boot order:
  1. systemd (PID 1)
  2. basic.target
  3. network-online.target
  4. user login
  5. openclaw-gateway (user service)
  6. ??? kernel-observer (needs root, not started)
  7. ??? notification (depends on gateway)

Issue: kernel-observer is NOT started at boot because:
  - It requires root (eBPF needs CAP_BPF, CAP_PERFMON)
  - It's not properly integrated with systemd
```

## Desired Boot Order

```
Boot Priority:

  ┌─────────────────────────────────────────────────────────────┐
  │  SYSTEM BOOT (PID 1)                                        │
  │                                                              │
  │  1. systemd starts                                          │
  │  2. sysinit.target (kernel, mounts, security)               │
  │  3. basic.target (core services)                            │
  │  4. network.target (network stack)                          │
  │  5. openclaw-kernel-observer (NEEDS ROOT)                    │
  │     - Starts eBPF programs                                   │
  │     - No dependency on user login                            │
  │     - Captures EVERYTHING from boot                          │
  │  6. network-online.target (network ready)                    │
  └─────────────────────────────────────────────────────────────┘
                           │
                           ▼
  ┌─────────────────────────────────────────────────────────────┐
  │  USER LOGIN                                                 │
  │                                                              │
  │  7. user session starts (gdm, wayland)                      │
  │  8. openclaw-gateway (user service)                          │
  │     - Gateway connects to kernel-observer                    │
  │     - WebSocket on localhost:18789                           │
  │  9. openclaw-notification (user service)                     │
  │     - Desktop notifications (notify-send)                    │
  │     - WhatsApp/Email push                                   │
  │  10. Heartbeat starts                                        │
  │     - Periodic checks                                        │
  │     - Pattern extraction                                     │
  └─────────────────────────────────────────────────────────────┘
```

## Why This Order?

### 1. Kernel Observer MUST Start First (If Desired)

```
Why start kernel-observer before user login?
  - eBPF programs run in kernel space (no user needed)
  - Captures boot process, service starts, early activity
  - Can detect anomalies during boot
  - Already running when user logs in

Why it needs system service?
  - Requires root (CAP_BPF, CAP_PERFMON)
  - Cannot run as user service
  - Must start before user session
```

### 2. Gateway Starts After User Login

```
Why gateway is user service?
  - No root needed
  - Needs user environment (HOME, PATH, config)
  - Runs as user csilva
  - Connects to kernel-observer via WebSocket
```

### 3. Notification Starts After Gateway

```
Why notification depends on gateway?
  - Needs Gateway to send WhatsApp/Email
  - Uses desktop notifications (requires user session)
  - Can work standalone (desktop only) but limited
```

## Implementation

### Option A: Kernel Observer at Boot (System Service)

```bash
# Install as system service (requires root)
sudo cp skills/kernel-observer/openclaw-kernel-observer.service /etc/systemd/system/

# Edit to remove user dependency
# (Already configured correctly)

# Enable at boot
sudo systemctl daemon-reload
sudo systemctl enable openclaw-kernel-observer

# Start now
sudo systemctl start openclaw-kernel-observer
```

### Option B: Kernel Observer on Demand (Recommended)

```bash
# Don't start at boot - start when needed
# Pros:
#   - No overhead when not needed
#   - No eBPF programs running all the time
#   - User control over when to trace
# Cons:
#   - Misses boot activity
#   - Needs manual start

# Start when needed
sudo systemctl start openclaw-kernel-observer
```

### Option C: Gateway Only (Current)

```
Current setup:
  - Gateway starts after user login
  - Kernel observer NOT started
  - Notification depends on gateway

This is the MINIMAL setup:
  - Gateway is always running
  - Kernel observer starts manually
  - Notifications work when gateway is up
```

## Recommended Priority

```
PRIORITY ORDER:

1. CRITICAL (Boot, always running):
   - openclaw-gateway (user service)
   
2. IMPORTANT (Start on demand):
   - openclaw-kernel-observer (system service, manual)
   
3. OPTIONAL (Depends on gateway):
   - openclaw-notification (user service, auto)

Why this order:
  - Gateway is the CORE - must always run
  - Kernel observer is OPTIONAL - overhead, privacy
  - Notification is NICE to have - depends on gateway
```

## Decision Matrix

| Scenario | Gateway | Kernel Observer | Notification |
|----------|---------|-----------------|--------------|
| **Minimal** | ✅ Boot | ❌ Manual | ✅ With gateway |
| **Full monitoring** | ✅ Boot | ✅ Boot | ✅ With gateway |
| **Privacy-focused** | ✅ Boot | ❌ Never | ❌ Manual |
| **Debug mode** | ✅ Boot | ✅ Manual | ❌ Off |

## My Recommendation

```
RECOMMENDED: Minimal + On-demand kernel observer

1. Gateway: ✅ Start at boot (user service)
   - Already configured
   - Low overhead
   - Always available

2. Kernel Observer: ❌ Manual start
   - Start when debugging/monitoring
   - Reduces privacy concerns
   - Lower overhead
   - sudo systemctl start openclaw-kernel-observer

3. Notification: ✅ Start with gateway
   - Low overhead
   - Critical for alerts
   - Desktop notifications work independently
```

## Service Files (For Reference)

### openclaw-gateway (User Service - CURRENT)

```ini
# ~/.config/systemd/user/openclaw-gateway.service
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target

[Service]
# ... (current config)

[Install]
WantedBy=default.target
```

### openclaw-kernel-observer (System Service - OPTIONAL)

```ini
# /etc/systemd/system/openclaw-kernel-observer.service
[Unit]
Description=OpenClaw Kernel Observer
After=network.target
Before=network-online.target
# Before user login to capture boot

[Service]
Type=simple
User=root
# ... (requires root)

[Install]
WantedBy=multi-user.target
# Start in multi-user, before graphical
```

### openclaw-notification (User Service - WITH GATEWAY)

```ini
# ~/.config/systemd/user/openclaw-notification.service
[Unit]
Description=OpenClaw Notification Manager
After=openclaw-gateway.service
Requires=openclaw-gateway.service

[Service]
# ... (current config)

[Install]
WantedBy=default.target
```

## Summary

| Question | Answer |
|----------|--------|
| **Should Gateway start at boot?** | ✅ YES - Critical, always needed |
| **Should Kernel Observer start at boot?** | ⚠️ OPTIONAL - Overhead, privacy, start on demand |
| **Should Notification start with Gateway?** | ✅ YES - Low overhead, important for alerts |
| **Priority order?** | Gateway > Notification > Kernel Observer |
| **Root required?** | Gateway: No, Notification: No, Kernel Observer: Yes |

## Final Recommendation

```
1. Keep Gateway as-is (user service, starts at login)
2. Make Notification depend on Gateway (user service)
3. Keep Kernel Observer manual (system service, start when needed)

Reasoning:
  - Gateway is lightweight, always needed
  - Notification is lightweight, important for alerts
  - Kernel Observer has overhead and privacy implications
  - User can choose when to enable deep monitoring
```