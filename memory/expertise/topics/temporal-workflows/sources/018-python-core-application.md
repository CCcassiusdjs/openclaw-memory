# Temporal Python SDK - Core Application

**Source:** https://docs.temporal.io/develop/python/core-application
**Date:** 2026-03-12
**Status:** read

---

## Workflow Definition

### Basic Structure
```python
from temporalio import workflow

@workflow.defn(name="YourWorkflow")
class YourWorkflow:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            your_activity,
            YourParams("Hello", name),
            start_to_close_timeout=timedelta(seconds=10),
        )
```

### Key Decorators
| Decorator | Purpose |
|-----------|---------|
| `@workflow.defn` | Marks class as Workflow Definition |
| `@workflow.run` | Entry point method (must be async) |

### Workflow Parameters
- Use **dataclasses** for parameters (recommended)
- All parameters must be serializable
- Single dataclass parameter encouraged (easier to evolve)

```python
@dataclass
class YourParams:
    greeting: str
    name: str
```

### Workflow Return Values
- Must be serializable
- Use `return` to return results
- Access via `start_workflow()` or `execute_workflow()`

### Workflow Type
- Default: unqualified class name
- Custom: `@workflow.defn(name="custom-name")`

## Deterministic Constraints

Workflow code must be deterministic:
- ❌ No threading
- ❌ No randomness
- ❌ No external calls
- ❌ No network I/O
- ❌ No global state mutation
- ❌ No system date/time

Use SDK APIs instead:
- `workflow.now()` for time
- `workflow.random()` for random
- Activities for external calls

## Activity Definition

### Basic Structure
```python
from temporalio import activity

@activity.defn(name="your_activity")
async def your_activity(input: YourParams) -> str:
    return f"{input.greeting}, {input.name}!"
```

### Activity Styles
| Style | Use Case |
|-------|----------|
| `async def` | Non-blocking, recommended |
| `def` + ThreadPoolExecutor | Blocking I/O |
| `def` + ProcessPoolExecutor | CPU-bound work |

### Activity Parameters
- Limit: 2 MB per argument, 4 MB total
- Use single dataclass parameter
- All parameters must be serializable

### Activity Timeouts (Required)
| Timeout | Description |
|---------|-------------|
| `start_to_close_timeout` | Total Activity execution time |
| `schedule_to_close_timeout` | Includes queue wait time |
| `schedule_to_start_timeout` | Time waiting in queue |

## Worker Process

### Basic Worker
```python
from temporalio.client import Client
from temporalio.worker import Worker

async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue="your-task-queue",
        workflows=[YourWorkflow],
        activities=[your_activity],
    )
    await worker.run()
```

### Registration Rules
- All Workers on same Task Queue must register same types
- Unknown types cause Task failure (not Workflow failure)
- Workers can have both Workflows and Activities

## Imports Passed Through

For third-party modules used in Workflows:
```python
with workflow.unsafe.imports_passed_through():
    from your_activities import your_activity
    from your_dataobject import YourParams
```

---

## Takeaways

1. **Use dataclasses** for Workflow/Activity parameters (easier evolution)
2. **Set timeouts** on Activities (required)
3. **Workers poll Task Queues** - register all types consistently
4. **Pass through imports** for third-party modules in Workflows
5. **async def recommended** for Activities (non-blocking)