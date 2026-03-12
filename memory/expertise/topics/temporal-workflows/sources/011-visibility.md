# Temporal Visibility

**Source:** https://docs.temporal.io/visibility
**Date:** 2026-03-12
**Status:** read

---

## What is Visibility?

The subsystem and APIs that enable viewing, filtering, and searching for Workflow Executions within a Temporal Service.

### Visibility Store
- Stores persisted Workflow Execution Event History data
- Part of Persistence store
- Enables listing and filtering Workflow Executions

## Standard Visibility (Deprecated)

Predefined filters only:
- **Open Workflows**: Time + Workflow Type, Workflow Id, or Run Id
- **Closed Workflows**: Time + Workflow Type, Workflow Id, Run Id, or Execution Status

**Limitations:**
- No Custom Search Attributes
- Deprecated from Temporal Server v1.21

## Advanced Visibility

SQL-like List Filter for Workflow Executions:
- Available on SQL databases (MySQL 8.0.17+, PostgreSQL 12+)
- Also supports Elasticsearch
- Enabled by default on Temporal Cloud

### Benefits
- Custom SQL-like queries
- Relieves performance issues on high-volume systems
- Recommended for > few Workflow Executions

## Count API

Count Workflows matching a query:
```bash
temporal workflow count -q "WorkflowType='foo'"
```

Group by Search Attribute:
```bash
temporal workflow count -q "WorkflowType='foo' GROUP BY ExecutionStatus"
```

**Note**: GROUP BY currently only supports ExecutionStatus
**Note**: Counts are approximate

---

## Takeaways

1. **Use Advanced Visibility** - Standard is deprecated
2. **SQL databases or Elasticsearch** - Advanced Visibility available on both
3. **Count API for metrics** - approximate counts with grouping
4. **Performance benefit** - Visibility store offloads query load