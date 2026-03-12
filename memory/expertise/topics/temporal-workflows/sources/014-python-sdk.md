# Temporal Python SDK Overview

**Source:** https://docs.temporal.io/develop/python
**Date:** 2026-03-12
**Status:** read

---

## Core Components

| Component | Description |
|-----------|-------------|
| **Workflows** | Durable function definitions |
| **Activities** | Single, well-defined operations |
| **Workers** | Process that polls and executes tasks |

## Key Features

### Core Application
- Develop a Basic Workflow
- Develop a Basic Activity
- Start an Activity Execution
- Run Worker Processes

### Temporal Client
- Connect to Development Temporal Service
- Connect to Temporal Cloud
- Start a Workflow Execution

### Standalone Activities
- Execute Activities independently without Workflow
- Get Activity result
- Get handle to existing Standalone Activity

### Python SDK Sandbox
- Use third-party modules without non-deterministic behavior

### Sync vs Async
- Implement synchronous or asynchronous Activities

## Testing

| Test Type | Description |
|-----------|-------------|
| Test Frameworks | Setup testing suite |
| Test Activities | Unit test Activity code |
| Test Workflows | Unit test Workflow code |
| Replay | Replay Workflow Execution from Event History |

## Failure Detection

- Workflow Timeouts
- Activity Timeouts
- Activity Heartbeats

## Message Passing

| Type | Direction | Blocking |
|------|-----------|----------|
| Signals | External → Workflow | Async |
| Queries | External → Workflow | Sync (immediate) |
| Updates | External → Workflow | Sync (waits) |

## Workflow Interruption

| Action | Description |
|--------|-------------|
| Cancel | Graceful cancellation |
| Terminate | Forceful termination |
| Reset | Resume from earlier Event History point |
| Cancel Activity | Cancel Activity from Workflow |

## Versioning

- Patching API for backward-compatible changes
- Workflow Definition changes without breaking replay

## Observability

- Metrics
- Tracing
- Logging
- Visibility APIs

## Advanced Features

| Feature | Description |
|---------|-------------|
| Schedules | Run Workflows on schedule |
| Cron Jobs | Temporal Cron Jobs |
| Start Delay | Delay Workflow start |
| Data Encryption | Custom converters and codecs |
| Nexus | Connect durable executions across Namespaces |
| Durable Timers | Sleep for seconds to years |
| Child Workflows | Spawn Child Workflow Executions |
| Continue-As-New | Fresh Execution with same Workflow ID |
| Interceptors | Inbound/outbound SDK call interception |

---

## Takeaways

1. **Python SDK mirrors core concepts** - Workflows, Activities, Workers
2. **Sandbox handles third-party modules** - prevents non-determinism
3. **Both sync and async Activities supported**
4. **Comprehensive testing support** - Activities, Workflows, Replay
5. **Nexus for cross-Namespace communication** - new feature