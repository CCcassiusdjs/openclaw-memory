# Temporal TypeScript SDK Overview

**Source:** https://docs.temporal.io/develop/typescript
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
- Develop a Basic Workflow
- Develop a Basic Activity
- Start an Activity Execution
- Run Worker Processes

## Temporal Client

Connect to Temporal Service:
- Connect to Development Temporal Service
- Connect to Temporal Cloud
- Start a Workflow Execution

## Testing

| Test Type | Description |
|-----------|-------------|
| Test Frameworks | Setup testing suite |
| Test Activities | Unit test Activity code |
| Test Workflows | Unit test Workflow code |
| Replay | Replay from Event History |

## Failure Detection

- Workflow Timeouts
- Activity Timeouts
- Activity Heartbeats

## Message Passing

- Signals (async, fire-and-forget)
- Queries (sync, read-only)
- Dynamic Handlers

## Cancellation & Interruption

- Cancellation scopes in TypeScript
- Reset a Workflow

## Versioning

- Introduction to Versioning
- How to Use the Patching API

## Observability

- Metrics
- Tracing
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
| Interceptors | Inbound/outbound SDK call interception |
| Vercel AI SDK | AI agents and AI-powered applications |

## TypeScript-Specific Notes

- Async/await native support
- Decorators for Workflow/Activity definitions
- Strong typing with TypeScript interfaces
- Native Promise integration
- Vercel AI SDK integration for AI applications

---

## Takeaways

1. **TypeScript SDK leverages async/await** - natural async patterns
2. **Full type safety** - interfaces for all components
3. **AI integration** - Vercel AI SDK for durable AI agents
4. **Modern JavaScript patterns** - decorators, promises, async/await