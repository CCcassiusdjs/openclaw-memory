# Temporal Activities

**Source:** https://docs.temporal.io/activities
**Date:** 2026-03-12
**Status:** read

---

## What is an Activity?

An Activity is a normal function or method that executes a **single, well-defined action** (short or long running):
- Calling another service
- Transcoding a media file
- Sending an email message

## Key Properties

### Non-Deterministic Code
- Activity code **can be non-deterministic** (unlike Workflows)
- Must be **idempotent** for retry safety

### Execution by Workers
- Activity Functions execute in Worker Processes
- Results sent back as `ActivityTaskCompleted` Event
- Events added to Workflow Execution's Event History

## Use Cases

Activities encompass small units of work:

1. **Single write operations**
   - Updating user information
   - Submitting credit card payment

2. **Batches of similar writes**
   - Creating multiple orders
   - Sending multiple messages

3. **Read-then-write operations**
   - Check product status + user address → update order status

4. **Memoized reads**
   - LLM calls
   - Large downloads
   - Slow-polling reads

## Best Practices

### Granularity
- Break large functionality into **multiple activities**
- Benefits:
  - Easier failure recovery
  - Shorter timeouts
  - Better idempotency

### Failure Handling
- If Activity fails, retries start from initial state
- Use **Heartbeat details payloads** for checkpointing
- Store state on server for resume capability

## Standalone Activities

If you only need to execute one Activity Function:
- **No Workflow required**
- Use SDK Client to invoke directly as Standalone Activity

## Activity vs Workflow

| Aspect | Activity | Workflow |
|--------|----------|-----------|
| Determinism | Can be non-deterministic | Must be deterministic |
| Purpose | Single operation | Orchestration |
| State | No internal state tracking | Full Event History |
| External calls | Allowed and encouraged | Not allowed |

---

## Takeaways

1. Activities are the **primary primitive** for external interactions
2. **Idempotency is critical** - activities may retry on failure
3. Use **heartbeats** for long-running activities with checkpointing
4. Keep activities **focused** - single well-defined action
5. Can run **standalone** without Workflow for simple use cases