# Temporal Service Architecture

**Source:** https://docs.temporal.io/temporal-service
**Date:** 2026-03-12
**Status:** read

---

## What is a Temporal Service?

A **Temporal Service** is the group of services, known as the Temporal Server, combined with Persistence and Visibility stores.

Together, they act as a component of the Temporal Platform.

## Components

| Component | Description |
|-----------|-------------|
| **Temporal Server** | Core services (History, Matching, Frontend) |
| **Persistence Store** | Database for Event History and state |
| **Visibility Store** | Database for listing/searching Workflows |

## Terminology Update

> **Note**: Temporal Cluster is now called **Temporal Service**.

## Architecture

```
┌─────────────────────────────────────┐
│           Temporal Service          │
│  ┌─────────────────────────────┐    │
│  │       Temporal Server       │    │
│  │  ┌─────────┬─────────┬─────┐│    │
│  │  │Frontend│Matching │History││   │
│  │  └─────────┴─────────┴─────┘│    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │     Persistence Store       │    │
│  │  (Event History, State)    │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │      Visibility Store       │    │
│  │  (Workflow Search/List)     │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

## Deployment Options

1. **Temporal Cloud** - Managed by Temporal
2. **Self-hosted** - Run your own Temporal Service

---

## Takeaways

1. **Temporal Service = Server + Persistence + Visibility**
2. **Workers run externally** - Your code runs on your infrastructure
3. **Temporal Service orchestrates** - Never executes your code
4. **Persistence is critical** - Event History is stored in database