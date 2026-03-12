# Temporal Retry Policies

**Source:** https://docs.temporal.io/encyclopedia/retry-policies
**Date:** 2026-03-12
**Status:** read

---

## Overview

A **Retry Policy** tells Temporal how and when to retry after failures:
- Declarative - specify behavior, Temporal handles execution
- Automatic retry for Activities (default)
- Workflow Executions don't retry by default

## Default Behavior

### Activities (Default: Retry Forever)
| Setting | Default Value |
|---------|---------------|
| Initial Interval | 1 second |
| Backoff Coefficient | 2.0 |
| Maximum Interval | 100 × Initial Interval |
| Maximum Attempts | ∞ (unlimited) |
| Non-Retryable Errors | [] (none) |

### Workflows (Default: No Retry)
- No Retry Policy by default
- Retrying entire Workflow is **not recommended**
- Workflows are deterministic - same logic repeats
- Better to retry failed Activities only

## Retry Interval Formula

```
interval = min(initial_interval × backoff_coefficient^attempts, maximum_interval)
```

Example with defaults:
- Attempt 1: 1s wait
- Attempt 2: 2s wait
- Attempt 3: 4s wait
- Attempt 4: 8s wait
- ... capped at 100s

## Properties

### Initial Interval
- Time before first retry
- Default: 1 second
- Base for backoff calculation

### Backoff Coefficient
- How much interval increases
- Default: 2.0
- 1.0 = constant interval (no backoff)

### Maximum Interval
- Cap on retry interval
- Default: 100 × Initial Interval
- Prevents infinite growth

### Maximum Attempts
- Limit on retry count
- 0 = unlimited
- 1 = single attempt, no retries
- Negative = error

### Non-Retryable Errors
- Error types that won't retry
- Matched against Application Failure type field
- Use for permanent failures (bad input, etc.)

## Per-Error Next Retry Delay

Activity/Workflow can throw Application Failure with custom next retry delay:
- Overrides Retry Policy interval
- Still capped by Maximum Attempts and timeouts

## Event History Nuances

### Activities
- `ActivityTaskStarted` not recorded until completion or final failure
- Use Describe API to see pending attempt count
- Avoids History noise

### Workflows with Retry Policy
- Failed run ends with `WorkflowExecutionFailed`, `retryState=IN_PROGRESS`
- New Execution created immediately
- First Workflow Task delayed by backoff duration

## When to Use Custom Retry Policy for Workflows

Rare cases:
- Temporal Cron Jobs / always-running stateless Workflows
- File-processing / media-encoding Workflows that download files

## Failure Types

| Type | Behavior | Example |
|------|----------|---------|
| **Transient** | Retry resolves | Network blip |
| **Intermittent** | Retry may resolve | Rate limit, brief outage |
| **Permanent** | Retry won't fix | Bad input data |

---

## Takeaways

1. **Activities retry by default** - infinite retries with exponential backoff
2. **Workflows don't retry by default** - design for determinism
3. **Use non-retryable errors for permanent failures** - surface issues immediately
4. **Maximum Attempts vs Timeout** - prefer timeouts to limit retry duration
5. **Per-error retry delay** - override policy for specific exceptions