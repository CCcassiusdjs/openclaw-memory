# Temporal Continue-As-New

**Source:** https://docs.temporal.io/workflow-execution/continue-as-new
**Date:** 2026-03-12
**Status:** read

---

## What is Continue-As-New?

A mechanism to **checkpoint Workflow state** and start a fresh Workflow Execution.

## Why Use Continue-As-New?

### 1. Event History Size Limits
- Long/large Workflows bog down with performance issues
- May exceed Event History limits
- Solution: Start fresh with new Event History

### 2. Versioning Problems
- Workflow running on old code version
- Then starts executing on new code version
- Solution: Periodic Continue-As-New to run on current version

## How It Works

1. Pass latest relevant state into Continue-As-New
2. New Execution in same Execution Chain
3. State passed as arguments to new Workflow
4. Same Workflow Id, different Run Id
5. Fresh Event History starts

## Entity Workflows

Workflows that use Continue-As-New repeatedly can run **forever**:
- Called "Entity Workflows"
- Represent durable objects, not just processes

## When to Continue-As-New?

Temporal tells you when via **Continue-As-New Suggested**:
- Check at spots where you're ready to checkpoint state
- Use to prevent running on stale code versions
- Deploy frequency determines how often to Continue-As-New

## Important Notes

- **Child Workflows don't carry over** when Parent uses Continue-As-New
- **Signal deduplication breaks** across Continue-As-New boundaries
- Handle deduplication yourself in message handlers

---

## Takeaways

1. **Use for long-running Workflows** - prevents Event History bloat
2. **Use for versioning hygiene** - run on current code versions
3. **Same Workflow Id, new Run Id** - part of Execution Chain
4. **Entity Workflows run forever** - represent durable objects
5. **Handle Signal deduplication yourself** - built-in dedup doesn't work across boundaries