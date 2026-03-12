# Temporal Failure Detection (Python SDK)

**Source:** https://docs.temporal.io/develop/python/failure-detection
**Date:** 2026-03-12
**Status:** read

---

## Exception Handling

### ApplicationError
The main Temporal error class to raise deliberately:
- Use `ApplicationError` for non-retryable errors
- Set `non_retryable=True` to prevent automatic retries
- Any other Python exception is converted to `ApplicationError`

```python
from temporalio.exceptions import ApplicationError

raise ApplicationError(
    type="MyNonRetryableError",
    message="Error message",
    non_retryable=True,
)
```

## Workflow Failures

### Key Principle
> An Activity Failure will never directly cause a Workflow Failure — a Workflow should never return as Failed unless deliberately.

### Workflow Task vs Execution Failure

| Failure Type | Cause | Result |
|--------------|-------|--------|
| **Workflow Task Failure** | Non-Temporal exception | Task retried until timeout |
| **Workflow Execution Failure** | `ApplicationError` | Workflow marked as Failed |

### Failing a Workflow
```python
try:
    result = await workflow.execute_activity(my_activity, ...)
except ActivityError as e:
    raise ApplicationError("Unable to process", "ProcessingError")
```

---

## Timeouts

### Workflow Timeouts (Not Recommended)
Workflows are designed to be long-running — timeouts limit resilience.
Use **Timers** instead for time-based logic.

| Timeout | Scope |
|---------|-------|
| `execution_timeout` | Entire Workflow Execution Chain |
| `run_timeout` | Single Workflow Run |
| `task_timeout` | Worker execution time |

### Activity Timeouts (Required)

| Timeout | Description |
|---------|-------------|
| `start_to_close_timeout` | Single Activity Task execution |
| `schedule_to_close_timeout` | Entire Activity Execution |
| `schedule_to_start_timeout` | Time waiting in queue |
| `heartbeat_timeout` | Max time between heartbeats |

**Must set either `start_to_close` or `schedule_to_close`.**

---

## Activity Retry Policy

Activities auto-retry with default policy:
- Initial interval: 1s
- Backoff coefficient: 2.0
- Max interval: 100s
- Max attempts: ∞

```python
from temporalio.common import RetryPolicy

result = await workflow.execute_activity(
    my_activity,
    input,
    start_to_close_timeout=timedelta(seconds=10),
    retry_policy=RetryPolicy(
        backoff_coefficient=2.0,
        maximum_attempts=5,
        initial_interval=timedelta(seconds=1),
        non_retryable_error_types=["ValueError"],
    ),
)
```

### Override Retry Delay
```python
raise ApplicationError(
    "Error message",
    next_retry_delay=timedelta(seconds=3 * attempt),
)
```

---

## Activity Heartbeats

### Why Heartbeat?
- Informs Temporal Service that Activity is making progress
- Enables cancellation delivery to Activities
- Supports detail data for checkpointing during retry

### How to Heartbeat
```python
@activity.defn
async def my_activity():
    activity.heartbeat("progress details")

    # On retry, get previous heartbeat details
    details = activity.info().heartbeat_details
```

### Heartbeat Timeout
```python
workflow.execute_activity(
    my_activity,
    heartbeat_timeout=timedelta(seconds=10),
)
```

**Recommendation:** Use short heartbeat timeout for long-running Activities.

---

## Takeaways

1. **Activities auto-retry** — use `non_retryable=True` for permanent failures
2. **Workflow failures must be explicit** — raise `ApplicationError` deliberately
3. **Heartbeat long-running Activities** — enables cancellation and checkpointing
4. **Set Activity timeouts** — `start_to_close` or `schedule_to_close` required
5. **Don't set Workflow timeouts** — use Timers for time-based logic