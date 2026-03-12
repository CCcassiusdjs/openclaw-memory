# Temporal Failures Reference

**Source:** https://docs.temporal.io/references/failures
**Date:** 2026-03-12
**Status:** read

---

## Failure Types Overview

| Failure | SDK Class | Cause |
|---------|-----------|-------|
| **TemporalFailure** | Base class | Parent of all Temporal failures |
| **ApplicationFailure** | ApplicationError (Python) | User-thrown failures |
| **CancelledFailure** | CancelledError | Workflow/Activity cancellation |
| **ActivityFailure** | ActivityError | Activity execution failure |
| **ChildWorkflowFailure** | ChildWorkflowError | Child Workflow failure |
| **TimeoutFailure** | TimeoutError | Activity/Workflow timeout |
| **TerminatedFailure** | TerminatedError | Workflow termination |
| **ServerFailure** | ServerError | Temporal Service errors |

---

## Application Failure

The only Temporal Failure created by user code.

### In Workflows

| Exception Type | Result |
|----------------|--------|
| `ApplicationError` | Workflow Execution Failure |
| Other exceptions | Workflow Task Failure (retried) |

### In Activities

| Exception Type | Result |
|----------------|--------|
| `ApplicationError` | Propagated to Workflow |
| Other exceptions | Converted to `ApplicationError` |

### Fields
- `type` — Error type name
- `message` — Error message
- `non_retryable` — Skip retry policy
- `details` — Additional data
- `cause` — Underlying cause
- `next_retry_delay` — Override retry interval

---

## Cancelled Failure

When cancellation is requested for Workflow, Activity, or Nexus Operation.

### Behavior
- Thrown to indicate successful cancellation
- Check with `isCancellation()` helper (TypeScript)
- Catch with `except CancelledError` (Python)

---

## Activity Failure

Delivered to Workflow when Activity fails.

### Structure
- `activity_type` — Activity name
- `activity_id` — Activity instance ID
- `cause` — Underlying failure (Timeout, Application, etc.)

### Handling
```python
try:
    result = await workflow.execute_activity(my_activity, ...)
except ActivityError as e:
    # e.cause contains the actual failure
    if isinstance(e.cause, TimeoutError):
        # Handle timeout
    elif isinstance(e.cause, ApplicationError):
        # Handle application failure
```

---

## Child Workflow Failure

Delivered to parent Workflow when Child fails.

### Structure
- `workflow_type` — Child Workflow type
- `workflow_id` — Child Workflow ID
- `cause` — Underlying failure

---

## Timeout Failure

Represents Activity or Workflow timeout.

### Behavior
- Last Heartbeat details attached when Activity times out
- Check `last_heartbeat_details` for checkpoint data

---

## Terminated Failure

Used when Workflow is terminated externally.

### Occurs In
- Waiting for Child Workflow result
- Waiting for Workflow result on Client

---

## Server Failure

Errors originating from Temporal Service.

### Use Cases
- Service unavailable
- Internal errors
- Configuration issues

---

## Nexus Operation Failure

Delivered to Workflow when Nexus Operation fails.

### Fields
- `endpoint` — Nexus endpoint name
- `service` — Service name
- `operation` — Operation name
- `operation_token` — Token for async operations
- `message` — Error message
- `cause` — Underlying Application Failure

### Retryable vs Non-Retryable

| Error Type | Retryable |
|------------|-----------|
| `HandlerErrorTypeInternal` | Yes |
| `HandlerErrorTypeResourceExhausted` | Yes |
| `HandlerErrorTypeBadRequest` | No |
| `HandlerErrorTypeNotFound` | No |
| `UnsuccessfulOperationError` | No |

---

## Takeaways

1. **ApplicationError is user-created** — all others are SDK/Service created
2. **Activity/Child failures wrap underlying cause** — check `e.cause`
3. **Workflow Task vs Execution Failure** — non-Temporal exceptions only fail the task
4. **Heartbeat details preserved in Timeout** — use for checkpointing
5. **Nexus Operations have built-in retry policy** — customize with `non_retryable`