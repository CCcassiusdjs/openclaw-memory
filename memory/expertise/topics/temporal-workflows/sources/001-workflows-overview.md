# Temporal Workflows Overview

**Source:** https://docs.temporal.io/workflows
**Date:** 2026-03-12
**Status:** read

---

## Key Concepts

### What is a Workflow?
- **Workflow Definition**: Code that defines your workflow
- **Workflow Type**: Name that maps to a Workflow Definition (identifier)
- **Workflow Execution**: Running instance of a Workflow Definition

### Core Properties
1. **Resilient**: Can run for years, survive infrastructure failures
2. **Replay-based**: State recreated from Event History on failure
3. **Deterministic**: Must follow deterministic constraints for consistent replay

## Event History
- Records all Commands and Events
- Used to recreate state on Worker failure
- Key to durability guarantees

## Deterministic Constraints
Workflow code must be deterministic to ensure consistent replay:
- No randomness
- No system time
- No external calls inside workflow code

## Related Concepts
- Workflow Definition → `/workflow-definition`
- Workflow Execution → `/workflow-execution`
- Schedules → `/schedule`
- Dynamic Handler → `/dynamic-handler`
- Cron Job → `/cron-job`

---

## Takeaways

1. Workflows are **resilient by default** - designed for long-running processes
2. The **Event History** is the source of truth for workflow state
3. **Determinism** is critical for replay guarantees
4. Workflows are written in general-purpose languages (Go, Java, TypeScript, Python)
5. A single Workflow Definition can have multiple executions with different inputs