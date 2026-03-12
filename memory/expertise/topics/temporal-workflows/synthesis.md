# Temporal Workflows & Orchestration - Synthesis

**Topic:** Temporal Workflows & Orchestration
**Status:** Completed
**Date:** 2026-03-12
**Sources Read:** 25/25 (100%)
**Hours Studied:** 1.5

---

## Executive Summary

Temporal is a **durable execution platform** that enables building reliable distributed systems. Workflows are resilient function executions that can run for seconds to years, surviving infrastructure failures through event sourcing and replay.

---

## Core Concepts

### 1. Durable Execution
- Workflows persist across process restarts, crashes, and infrastructure failures
- Event History is the source of truth for Workflow state
- Replay reconstructs Workflow state from Event History

### 2. Deterministic Constraints
Workflows must be deterministic for consistent replay:
- ❌ No randomness
- ❌ No system time (`workflow.now()` instead)
- ❌ No external calls (use Activities)
- ❌ No global state mutation

### 3. Event Sourcing
- All state changes recorded as Events in Event History
- Commands issued by Workers → Events recorded by Service
- Event History enables replay and recovery

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Temporal Service                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Frontend   │  │  Matching   │  │      History        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Persistence Store (DB)                  │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Visibility Store (Search)               │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ Task Queues
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Worker Process                            │
│  ┌─────────────────────┐  ┌─────────────────────────────┐   │
│  │  Workflow Worker    │  │     Activity Worker         │   │
│  │  (Replay Engine)    │  │  (Execute Activities)       │   │
│  └─────────────────────┘  └─────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Components

### Workflows
- Durable function definitions
- Must be deterministic
- Can run for years
- Survive failures via replay

### Activities
- Single, well-defined operations
- Can be non-deterministic
- Handle external interactions (API calls, DB queries)
- Auto-retry with exponential backoff (default)
- Must be idempotent for retry safety

### Workers
- Poll Task Queues
- Execute Workflow Tasks and Activity Tasks
- Stateless (can handle millions of Workflows)
- Run on your infrastructure (Temporal never executes your code)

### Signals, Queries, Updates

| Type | Direction | Blocking | Mutates | Returns |
|------|-----------|----------|---------|---------|
| Query | Client → Workflow | Sync (immediate) | No | Yes |
| Signal | Client → Workflow | Async (fire-forget) | Yes | No |
| Update | Client → Workflow | Sync (waits) | Yes | Yes |

---

## Execution Model

### Workflow Lifecycle
1. **Started** → WorkflowExecutionStarted event
2. **Running** → Worker processes Tasks
3. **Completed/Failed/Canceled/Terminated** → Terminal state

### Commands & Events
- **Commands**: Worker-issued requests (ScheduleActivity, StartTimer, etc.)
- **Events**: Service-recorded history (ActivityTaskScheduled, TimerFired, etc.)

### Retry Policies
Activities retry by default:
- Initial interval: 1s
- Backoff coefficient: 2.0
- Max interval: 100 × initial
- Max attempts: ∞

### Heartbeating
Long-running Activities should heartbeat:
- Informs Service of progress
- Enables cancellation delivery
- Supports checkpoint data for retry recovery

---

## Message Passing Patterns

### Signal-With-Start
Send Signal, start Workflow if not running:
```python
await client.start_workflow(
    MyWorkflow.run,
    id="workflow-id",
    start_signal="submit",
    start_signal_args=["data"],
)
```

### Update-With-Start
Send Update, start Workflow if not running.

### Initialize State Before Handlers
```python
@workflow.defn
class MyWorkflow:
    @workflow.init
    def __init__(self):
        self.state = {}  # Initialize before handlers
    
    @workflow.signal
    def handle_signal(self, data):
        self.state["signal"] = data  # Safe now
```

---

## Best Practices

### 1. Activity Granularity
- Keep Activities focused on single operations
- Easier failure recovery
- Better timeout management
- Simpler idempotency

### 2. Heartbeat Long-Running Activities
```python
@activity.defn
async def long_activity():
    for i in range(1000):
        process_item(i)
        activity.heartbeat(i)  # Checkpoint progress
```

### 3. Use Local Activities Sparingly
- Only for short operations (seconds)
- Same process as Workflow
- No global rate limiting
- Can block Workflow if too long

### 4. Limit Child Workflows
- Max 1,000 Children per Parent
- Use for separate services, partitioning, or resource mapping
- Default to Activities when in doubt

### 5. Handle Non-Determinism in Activities
- Workflows must be deterministic
- Put randomness, time, external calls in Activities
- Use SDK APIs (`workflow.now()`, `workflow.random()`)

### 6. Version Before You Need It
- Plan for code changes with Worker Versioning
- Use Patching API for backward-compatible changes
- Test with replay testing

---

## SDK Comparison

| Feature | Python | Go | TypeScript |
|---------|--------|-----|------------|
| Async Support | ✅ Native | ✅ Goroutines | ✅ Native |
| Type Safety | ✅ Dataclasses | ✅ Structs | ✅ Interfaces |
| Testing | ✅ Mocks | ✅ Test framework | ✅ Test framework |
| AI Integration | — | — | ✅ Vercel AI SDK |
| Worker Sessions | — | ✅ | — |

---

## Common Patterns

### Saga Pattern
```python
try:
    result = await workflow.execute_activity(step1, ...)
    result = await workflow.execute_activity(step2, ...)
except ActivityError:
    # Compensating transactions
    await workflow.execute_activity(compensate, ...)
```

### Entity Workflow (Long-Running)
```python
@workflow.defn
class EntityWorkflow:
    @workflow.run
    async def run(self):
        while True:
            await workflow.wait_condition(lambda: self.has_work())
            await self.process_work()
            # Use Continue-As-New periodically
            if workflow.info().get_current_history_length() > 10000:
                workflow.continue_as_new()
```

### Fan-Out/Fan-In
```python
handles = [workflow.execute_activity(process, item) for item in items]
results = await asyncio.gather(*handles)
```

---

## Failure Handling

### Workflow Failures
- Only `ApplicationError` fails Workflow Execution
- Other exceptions fail Workflow Task (retried)

### Activity Failures
- Auto-retry with exponential backoff
- Use `non_retryable=True` for permanent failures
- Set `next_retry_delay` for custom retry timing

### Timeout Types

| Timeout | Scope | Use Case |
|---------|-------|----------|
| `start_to_close` | Activity Task | Single execution time |
| `schedule_to_close` | Activity Execution | Total time including queue |
| `heartbeat` | Activity Heartbeat | Max time between heartbeats |
| `execution` | Workflow Chain | Total chain duration |
| `run` | Workflow Run | Single run duration |

---

## Key Takeaways

1. **Temporal executes nothing** — Workers run on your infrastructure
2. **Event History is source of truth** — All state from replay
3. **Determinism is non-negotiable** — Same input = same Command sequence
4. **Activities for external interactions** — Network I/O, randomness, time
5. **Heartbeat long-running Activities** — Enable cancellation and checkpointing
6. **Queries are free** — No Event History write
7. **Signals are async** — Fire-and-forget
8. **Updates are sync** — Track completion, validate before accepting
9. **Worker Versioning for safe deployments** — Plan for code changes
10. **Continue-As-New for long-running** — Prevent Event History bloat

---

## References

- Official Docs: https://docs.temporal.io
- Python SDK: https://docs.temporal.io/develop/python
- Go SDK: https://docs.temporal.io/develop/go
- TypeScript SDK: https://docs.temporal.io/develop/typescript
- Blog: https://temporal.io/blog

---

## Next Steps for Mastery

1. **Hands-on Practice**: Build a simple Workflow with Activities, Signals, and Queries
2. **Testing**: Learn replay testing for determinism verification
3. **Production**: Study Worker deployment patterns, monitoring, and security
4. **Advanced Patterns**: Explore Nexus Operations, Child Workflows, Entity Workflows
5. **SDK Deep-Dive**: Master one SDK thoroughly (Python recommended for this workspace)

---

*Synthesis completed: 2026-03-12*
*Sources: 25 official documentation pages + supplementary articles*