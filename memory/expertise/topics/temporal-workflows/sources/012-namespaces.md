# Temporal Namespaces

**Source:** https://docs.temporal.io/namespaces
**Date:** 2026-03-12
**Status:** read

---

## What is a Namespace?

A **unit of isolation** within the Temporal Platform:
- Task Queues belong to a Namespace
- Workflow Executions belong to a Namespace
- Workflow IDs are unique within a Namespace

## Key Properties

| Property | Behavior |
|----------|----------|
| **Workflow ID Uniqueness** | Guaranteed within Namespace |
| **Resource Isolation** | Heavy traffic in one Namespace doesn't impact others |
| **Configuration Boundaries** | Retention Period, Archival per Namespace |
| **Multi-tenancy** | Single Namespace is still multi-tenant |

## Default Namespace

If no Namespace specified:
- Temporal Service uses "default" Namespace
- You must create a Namespace before using it in your Client

## Multi-Tenancy

- Single Namespace = still multi-tenant
- Multiple applications/teams can share a Namespace
- Must coordinate on Workflow ID and Task Queue naming to avoid conflicts

---

## Takeaways

1. **Namespaces provide isolation** - resource and configuration boundaries
2. **Workflow IDs are Namespace-scoped** - same ID can exist in different Namespaces
3. **Create Namespaces before use** - "default" exists but custom ones need creation
4. **Coordinate naming** - shared Namespaces require coordination on IDs and Task Queues