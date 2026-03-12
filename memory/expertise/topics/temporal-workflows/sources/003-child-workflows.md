# Temporal Child Workflows

**Source:** https://docs.temporal.io/child-workflows
**Date:** 2026-03-12
**Status:** read

---

## Definition

A Child Workflow Execution is a Workflow Execution spawned from within another Workflow in the same Namespace.

## Parent-Child Relationship

- Parent Workflow must **await on the Child to spawn**
- Parent can optionally **await on the result**
- Parent Close Policy determines behavior when Parent closes
- Child Workflows **do NOT carry over** when Parent uses Continue-As-New

## When to Use Child Workflows

### ❌ Don't Use For Code Organization
- Single Workflow with bounded Activity count is simpler
- Use object-oriented structure for code organization
- Starting with single Workflow is recommended

### ✅ Valid Use Cases

#### 1. Separate Service
- Child can be processed by **completely separate Workers**
- Acts as entirely separate service
- **Trade-off**: No shared local state with Parent
- Communication only via async Signals

#### 2. Partition Large Workloads
- Event History has **size limits**
- Parent with 1,000 Children × 1,000 Activities = 1,000,000 Activity Executions
- **Limit**: Don't spawn more than 1,000 Children per Parent

#### 3. Single Resource Mapping
- One-to-one mapping with a resource
- Use Workflow ID for uniqueness
- Example: Host upgrades with one Child per hostname
- All operations on resource serialized

#### 4. Periodic Logic Execution
- Child executes periodic logic
- Uses Continue-As-New for iterations
- Parent sees single Child invocation
- Prevents Parent Event History overload

## Child Workflow vs Activity

| Aspect | Child Workflow | Activity |
|--------|---------------|----------|
| Workflow APIs | Full access | No access |
| Determinism | Same constraints as Workflow | Can be non-deterministic |
| Event Tracking | Full Event History | Only input/output/retry attempts |
| Cancellation | Can continue if ABANDON policy | Always canceled with Workflow |
| Use Case | Composite operations | Single operation |

## Parent Close Policy

When Parent Workflow closes, Children are handled based on policy:
- **ABANDON**: Child continues running
- **TERMINATE**: Child is terminated
- **REQUEST_CANCEL**: Cancellation request sent to Child

## Best Practice

> **"When in doubt, use an Activity."**

---

## Takeaways

1. Child Workflows enable **hierarchical composition**
2. Use for **separate services**, **resource mapping**, or **workload partitioning**
3. **Limit**: Maximum 1,000 Children per Parent
4. Children have their own **Event History** (separate from Parent)
5. **Start simple** - single Workflow with Activities first