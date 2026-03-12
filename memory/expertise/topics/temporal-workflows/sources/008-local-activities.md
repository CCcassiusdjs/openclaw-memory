# Temporal Local Activities

**Source:** https://docs.temporal.io/local-activity
**Date:** 2026-03-12
**Status:** read

---

## What is a Local Activity?

An Activity Execution that runs in **the same process as the Workflow Execution** that spawns it.

## Benefits vs Regular Activities

| Aspect | Local Activity | Regular Activity |
|--------|---------------|------------------|
| **Latency** | Lower (no roundtrip to Service) | Higher |
| **Service Resources** | Fewer History events | More History events |
| **Duration** | Short (seconds) | Any duration |
| **Rate Limiting** | No global rate limiting | Yes |
| **Routing** | Same Worker only | Can route to specific Workers |

## When to Use Local Activities

Criteria (ALL must apply):
1. Implemented in same binary as Workflow
2. No need for global rate limiting
3. No need for routing to specific Worker/pool
4. Duration ≤ few seconds (including retries)

## Workflow Task Heartbeating

If Local Activity takes >80% of Workflow Task Timeout (default 10s):
- Worker requests new Workflow Task to extend "lease"
- Called Workflow Task Heartbeating

## Drawbacks of Long Local Activities

- Each new Workflow Task = 3 more Events in History
- Workflow won't receive new events (Signals, completions) until next heartbeat
- New Commands won't be sent until Activity completes or next heartbeat

## Recommendation

> **Use regular Activities unless your use case requires very high throughput and large Activity fan-outs of very short-lived Activities.**

---

## Takeaways

1. **Local Activities are for short, local operations** - same process, same binary
2. **Benefits come with tradeoffs** - less overhead but limited capabilities
3. **Watch duration** - >80% of Workflow Task Timeout triggers heartbeating
4. **Default to regular Activities** - only use Local when you understand limitations