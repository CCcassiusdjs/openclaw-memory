# Temporal Go SDK Overview

**Source:** https://docs.temporal.io/develop/go
**Date:** 2026-03-12
**Status:** read

---

## Core Application

| Component | Description |
|-----------|-------------|
| Workflows | Durable function definitions |
| Activities | Single, well-defined operations |
| Workers | Process that polls and executes tasks |

### Key Topics
- Develop a basic Workflow
- Develop an Activity Definition
- Start an Activity Execution
- Develop a Worker
- Run a Temporal Cloud Worker

## Temporal Client

Connect to Temporal Service and start Workflows:
- Connect to development Temporal Service
- Connect to Temporal Cloud
- Start Workflow Execution

## Multithreading

Safe multithreading patterns with Go SDK.

## Testing

| Test Type | Description |
|-----------|-------------|
| Test Frameworks | Setup testing suite |
| Test Activities | Unit test Activity code |
| Mock Activities | Override for testing |
| Test Workflows | Unit test Workflow code |
| Replay | Replay from Event History |

## Failure Detection

- Workflow Timeouts
- Activity Timeouts
- Activity Heartbeats

## Message Passing

- Signals (async, fire-and-forget)
- Queries (sync, read-only)
- Updates (sync, can mutate)

## Cancellation & Interruption

- Handle Cancellation in Workflow
- Reset a Workflow
- Request Cancellation

## Versioning

Change Workflow Definitions without non-deterministic behavior:
- Patching API
- Runtime checking

## Observability

- Metrics
- Tracing and Context Propagation
- Logging
- Visibility APIs

## Advanced Features

| Feature | Description |
|---------|-------------|
| Schedules | Run Workflows on schedule |
| Data Encryption | Custom converters and codecs |
| Nexus | Cross-Namespace operations |
| Durable Timers | Sleep for seconds to years |
| Child Workflows | Spawn Child Workflow Executions |
| Continue-As-New | Fresh Execution with same ID |
| Worker Sessions | Session APIs for Workers |
| Side Effects | Non-deterministic operations |

## Go-Specific Notes

- Struct-based Workflow definitions
- Strong typing with Go type system
- Native goroutine integration for Workers
- Comprehensive testing support with mocking

---

## Takeaways

1. **Go SDK follows Go idioms** - struct-based definitions, native types
2. **Comprehensive testing** - mock Activities, replay Workflows
3. **Full feature parity** - all Temporal features available
4. **Strong typing** - leverage Go's type system for safety