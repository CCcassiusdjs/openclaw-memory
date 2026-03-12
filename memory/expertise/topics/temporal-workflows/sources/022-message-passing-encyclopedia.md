# Temporal Workflow Message Passing - Encyclopedia

**Source:** https://docs.temporal.io/encyclopedia/workflow-message-passing
**Date:** 2026-03-12
**Status:** read

---

## Overview

Workflows can be thought of as **stateful web services** that receive messages. The Workflow can have powerful message handlers akin to endpoints that react to incoming messages in combination with current Workflow state.

## Message Types

| Type | Behavior | Purpose |
|------|----------|---------|
| **Queries** | Read requests | Read current state (cannot block) |
| **Signals** | Async write requests | Cause changes (fire-and-forget) |
| **Updates** | Sync write requests | Track completion, get result/error |

---

## Choosing Between Signals and Updates

### When to Use Signals

| Requirement | Use Signals When... |
|-------------|---------------------|
| Asynchronous | Client wants to quickly move on |
| Result handling | "Fire and forget" - no result needed |
| Worker availability | Don't depend on Worker being available |
| Concurrency | Don't want to limit concurrent messages |
| Latency | Latency not relevant (no result expected) |

### When to Use Updates

| Requirement | Use Updates When... |
|-------------|---------------------|
| Asynchronous | Client wants to track completion |
| Result handling | Need result or exception without query |
| Worker availability | Want to validate before accepting into history |
| Concurrency | Within allowed limits per Workflow |
| Latency | Want low-latency end-to-end operation |

---

## For Read Requests

### Use Queries (Preferred)
- **Efficient** - never add entries to Event History
- Can operate on **completed Workflows**

### Use Updates (Sometimes)
When goal is to read once Workflow achieves certain state:
- Option 1: Poll periodically with Queries
- Option 2: Write as Update (better efficiency/latency, writes to History)

---

## For Read/Write Requests

**Use Update** for synchronous read/write requests.

If request must be **asynchronous**, consider:
1. Send Signal
2. Poll with Query

---

## Summary Table

| Aspect | Query | Signal | Update |
|--------|-------|--------|--------|
| Direction | Client → Workflow | Client → Workflow | Client → Workflow |
| Blocking | Sync (immediate) | Async (fire-forget) | Sync (waits) |
| Mutates | No | Yes | Yes |
| Returns | Yes | No | Yes |
| History | No write | Writes event | Writes event (if accepted) |
| Worker needed | Yes | No | Yes |

---

## Takeaways

1. **Queries for reads** - efficient, no History write, works on completed Workflows
2. **Signals for async writes** - fire-and-forget, no Worker dependency
3. **Updates for sync writes** - track completion, validate before accepting
4. **Read/write = Update** - or Signal + Query poll pattern