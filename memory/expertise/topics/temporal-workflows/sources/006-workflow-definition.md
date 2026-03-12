# Temporal Workflow Definition

**Source:** https://docs.temporal.io/workflow-definition
**Date:** 2026-03-12
**Status:** read

---

## What is a Workflow Definition?

Code that defines the Workflow, written with a Temporal SDK:
- Typically implemented as function or object method
- Encompasses end-to-end steps of a Temporal application

**Terminology:**
- **Workflow Definition** → Source code for Workflow Execution
- **Workflow Function** → Source code for Workflow Function Execution
- **Workflow Execution** → Executes once to completion
- **Workflow Function Execution** → Occurs many times during Workflow Execution life (replay!)

## Deterministic Constraints

**Critical**: Workflow Definitions must be deterministic:
- Same input → Same Workflow API calls in same sequence
- Re-execution (replay) must match existing Event History

### Safe Changes (Non-Deterministic)
- Input parameters, return values, timeouts
- Adding/removing non-Command-producing APIs

### Unsafe Changes (Break Replay)
Cannot reorder, add, or remove without proper versioning:
- Timer start/cancel
- Activity scheduling/cancellation
- Child Workflow start/cancellation
- Signals to external Workflows
- Workflow termination (complete/fail/cancel/continue-as-new)
- Versioning calls (Patched/GetVersion)
- Search Attribute upserts
- Memo upserts
- SideEffect/MutableSideEffect

## Intrinsic Non-Determinism

**Forbidden in Workflows:**
- Local time calls (`local_clock()`)
- Random number generation inline
- External calls without SDK APIs

**Solution**: Use SDK-provided APIs:
- `workflow.now()` for time
- `workflow.random()` for random
- Activities for external calls

## Workflow Versioning

Two strategies for handling code changes:

### 1. Worker Versioning (Recommended)
- Keep Workers tied to specific code revisions
- Old Workers → old code paths
- New Workers → new code paths

### 2. Patching
- Make code changes compatible across versions
- SDK-specific patching APIs

## Handling Unreliable Workers

**You don't handle Worker failure in Workflow Definition.**
- Workflow Function Executions are oblivious to Worker failures
- Temporal Platform ensures state recovery
- Only failure: code throwing error, not infrastructure

## Workflow Type

Name that maps to a Workflow Definition:
- Single Type → Multiple Executions
- Scoped by Task Queue
- Same name can map to different Definitions with different Workers

---

## Takeaways

1. **Determinism is non-negotiable** - same input must produce same Command sequence
2. **Replay is fundamental** - Workflow Function executes many times (replay), not once
3. **Version before you need it** - plan for code changes with Worker Versioning or Patching
4. **Use SDK APIs for non-determinism** - time, random, external calls all via SDK
5. **Worker failures are transparent** - Temporal handles recovery automatically