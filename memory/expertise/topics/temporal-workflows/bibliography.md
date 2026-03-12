# Temporal Workflows - Bibliography

**Status:** researching
**Priority:** 10 (highest)
**Created:** 2026-03-12
**Last Updated:** 2026-03-12

---

## Overview

Temporal is a durable execution platform that enables developers to build reliable distributed systems. This bibliography catalogs key resources for learning Temporal workflows.

---

## Official Documentation (Primary Sources)

### Core Concepts
| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| Workflows Overview | https://docs.temporal.io/workflows | unread | Core concept - durable execution units |
| Activities | https://docs.temporal.io/activities | unread | Activities for external interactions |
| Child Workflows | https://docs.temporal.io/child-workflows | unread | Hierarchical workflow composition |
| Workers | https://docs.temporal.io/workers | unread | Worker processes, entities, identity |
| Task Queues | https://docs.temporal.io/task-queues | unread | Task distribution mechanism |
| Namespaces | https://docs.temporal.io/namespaces | unread | Isolation units within Temporal |
| Visibility | https://docs.temporal.io/visibility | unread | Workflow search and filtering |

### Workflow Execution
| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| Workflow Definition | https://docs.temporal.io/workflow-definition | unread | How workflows are defined |
| Workflow Execution | https://docs.temporal.io/workflow-execution | unread | Execution lifecycle |
| Continue-As-New | https://docs.temporal.io/workflow-execution/continue-as-new | unread | Long-running workflow pattern |
| Commands Reference | https://docs.temporal.io/references/commands | unread | Worker-issued commands |
| Events Reference | https://docs.temporal.io/references/events | unread | Event history documentation |

### Data & Communication
| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| Signals & Queries | https://docs.temporal.io/handling-messages | unread | Async/sync messaging patterns |
| Data Converter | https://docs.temporal.io/dataconversion | unread | Payload serialization/encoding |
| Retry Policies | https://docs.temporal.io/encyclopedia/retry-policies | unread | Activity retry configuration |
| Local Activity | https://docs.temporal.io/local-activity | unread | In-process activities |

### Temporal Service
| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| Temporal Service | https://docs.temporal.io/temporal-service | unread | Server + persistence overview |

---

## SDK Documentation

### Python SDK
| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| Python SDK Guide | https://docs.temporal.io/develop/python | unread | Python SDK overview |
| Core Application | https://docs.temporal.io/develop/python/core-application | unread | Workflows, Activities, Workers |

### Go SDK
| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| Go SDK Guide | https://docs.temporal.io/develop/go | pending | Go SDK overview |

### TypeScript SDK
| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| TypeScript SDK Guide | https://docs.temporal.io/develop/typescript | pending | TypeScript SDK overview |

---

## Academic Papers & Research

| Paper | URL | Status | Notes |
|-------|-----|--------|-------|
| Workflow Engine Principles (Sergey Kleyman) | https://temporal.io/blog/workflow-engine-principles | pending | Core architecture principles |

---

## Blog Posts & Articles

| Article | URL | Status | Notes |
|---------|-----|--------|-------|
| Temporal Blog | https://temporal.io/blog | pending | Official blog with patterns and best practices |

---

## Tutorials & Courses

| Resource | URL | Status | Notes |
|----------|-----|--------|-------|
| Temporal Courses | https://docs.temporal.io/courses | pending | Official learning path |
| AI Cookbook | https://docs.temporal.io/ai-cookbook | pending | AI/ML workflow patterns |
| Code Exchange | https://docs.temporal.io/code-exchange | pending | Community examples |

---

## Key Concepts to Understand

1. **Durable Execution**: Workflows persist state across process restarts
2. **Determinism**: Workflow code must be deterministic (no randomness, no system time, no network I/O)
3. **Event Sourcing**: All state changes recorded as events in Event History
4. **Workers**: Poll Task Queues, execute Workflow/Activity tasks
5. **Activities**: External interactions (API calls, DB queries) with retry policies
6. **Signals/Queries**: Async and sync communication with running workflows
7. **Child Workflows**: Hierarchical composition pattern
8. **Continue-As-New**: Long-running workflow state checkpointing
9. **Data Converter**: Custom serialization/encryption for payloads
10. **Visibility**: Search and list workflow executions

---

## Reading Order (Recommended)

### Phase 1: Core Concepts
1. Workflows Overview
2. Activities
3. Workers
4. Task Queues

### Phase 2: Execution Model
5. Workflow Definition
6. Workflow Execution
7. Commands Reference
8. Events Reference

### Phase 3: Communication Patterns
9. Signals & Queries
10. Child Workflows
11. Continue-As-New

### Phase 4: Production Concerns
12. Retry Policies
13. Data Converter
14. Visibility
15. Namespaces

---

## Source Categories

- **Official Docs**: 20+ pages documented
- **SDK Guides**: Python, Go, TypeScript (partially covered)
- **Blog Posts**: Pending collection
- **Papers**: 1 identified
- **Tutorials**: Pending review

---

## Notes

- Temporal evolved from Amazon SWF and Uber Cadence
- Key differentiator: Deterministic workflow replay
- Supports Python, Go, TypeScript, Java, PHP, .NET SDKs
- Cloud offering available (Temporal Cloud) or self-hosted

---

## Next Steps

1. Read remaining official documentation pages
2. Complete Python SDK deep-dive
3. Review workflow patterns and best practices
4. Study retry policy configurations
5. Explore testing strategies