# Temporal Signals, Queries, and Updates

**Source:** https://docs.temporal.io/handling-messages
**Date:** 2026-03-12
**Status:** read

---

## Message Types

| Type | Direction | Blocking | Purpose |
|------|------------|----------|---------|
| **Signal** | External → Workflow | Async (fire-and-forget) | Mutate Workflow state |
| **Query** | External → Workflow | Sync (immediate return) | Read Workflow state |
| **Update** | External → Workflow | Sync (waits for completion) | Mutate and return result |

## Message Handler Concurrency

Temporal runs a loop that:
1. Processes messages in order received
2. Makes progress in Workflow's main method

**Key insight**: Single-threaded but can interleave:
- Signal handlers can block
- Update handlers can block
- Race conditions possible if handlers block

### Workflow Initialization

**Initialize state before handling messages!**

Message handlers run before main Workflow method in scenarios:
- Signal-with-Start
- Worker delays / backlogged Task Queue
- Messages arrive after Continue-As-New

**Pattern**: Use constructor/initializer for state setup.

## Message Handler Patterns

### 1. Synchronous Handlers
- Return immediately
- Don't block
- Guaranteed atomic execution

### 2. Waiting (Blocking)
- Handler blocks until Workflow reaches certain state
- Use Wait Conditions

### 3. Running Asynchronous Tasks
- Handler waits for long-running operations (Activities)
- Yields control back to loop
- Use mutex/semaphore primitives for safety

### 4. Inject Work into Main Workflow
- Handlers put work in queue
- Main Workflow picks up in event loop
- Avoids concurrency primitives

### 5. Finishing Handlers Before Workflow Completes
- Await `All Handlers Finished` before completion
- Or set `Handler Unfinished Policy` = `Abandon` to suppress warnings

### 6. Exactly-Once Message Processing

Temporal deduplicates messages BUT:
- **Continue-As-New breaks deduplication** - handle yourself
- Use idempotency key in message handler

For clients:
- **Update**: Custom Update ID for deduplication across callsites
- **Signal**: Idempotency key in Signal arguments

## Update Validators

Optional read-only operation to accept/reject Updates:
- **Accept** → Update added to history, handler runs
- **Reject** → Client notified, Workflow unaware (like Query)

**Rule**: Validators cannot block.

## Exception Handling

### Signals
| Exception Type | Result |
|---------------|--------|
| Application Failure | Workflow fails (unrecoverable) |
| Activity/Child Failure | Workflow fails |
| Other Exception | Workflow Task Failure (retries periodically) |

### Updates
| Exception Type | Result |
|---------------|--------|
| Validator rejection | Update fails, Workflow continues |
| Application Failure | Update fails, Workflow continues |
| Other Exception | Workflow Task Failure (blocks client) |

---

## Takeaways

1. **Initialize state before handlers** - prevents reading uninitialized variables
2. **Single-threaded but interleaved** - handlers can race if blocking
3. **Exactly-once needs help across Continue-As-New** - use idempotency keys
4. **Validators are read-only** - cannot block, accept/reject Updates
5. **Application Failures behave differently** - Signals fail Workflow, Updates fail Update