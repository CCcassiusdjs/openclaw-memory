# Temporal Self-Hosted Guide

**Source:** https://docs.temporal.io/self-hosted-guide
**Date:** 2026-03-12
**Status:** read

---

## Overview

Self-host open source infrastructure software that orchestrates your durable applications.

## Alternatives to Self-Hosting

| Option | Description |
|--------|-------------|
| **Temporal Cloud** | Managed service (recommended) |
| **Development Server** | Temporal CLI `temporal server start-dev` |

## Getting Started

- For learning: Use introductory tutorials and courses
- For development: Use development server via Temporal CLI
- For production: Self-host or use Temporal Cloud

## Self-Hosted Topics

| Topic | Description |
|-------|-------------|
| **Deployment** | Deploy Temporal Service |
| **Embedded Server** | Single-binary deployment |
| **Defaults** | Configuration defaults |
| **Production Checklist** | Checklist for production |
| **Namespaces** | Namespace management |
| **Security** | Security configuration |
| **Monitoring** | Observability setup |
| **Visibility** | Visibility subsystem |
| **Data Encryption** | Encryption at rest |
| **Upgrading Server** | Upgrade procedures |
| **Archival** | Archive Event History |
| **Multi-Cluster Replication** | Multi-datacenter setup |
| **Nexus** | Cross-namespace operations |

---

## Key Deployment Components

1. **Temporal Server** - Core services (Frontend, Matching, History)
2. **Persistence Store** - Database (PostgreSQL, MySQL, Cassandra)
3. **Visibility Store** - Search/indexing (SQL, Elasticsearch)
4. **Workers** - Your infrastructure

---

## Takeaways

1. **Development server for dev** - simplest setup via CLI
2. **Temporal Cloud for managed** - no infrastructure overhead
3. **Self-host for control** - but requires operational expertise
4. **Multiple deployment options** - embedded, single-binary, distributed