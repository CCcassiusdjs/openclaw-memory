# Temporal Python SDK - Message Passing

**Source:** https://docs.temporal.io/develop/python/message-passing
**Date:** 2026-03-12
**Status:** read

---

## Message Types Overview

| Type | Direction | Blocking | Mutates | Returns |
|------|-----------|----------|---------|---------|
| **Query** | Client → Workflow | Sync (immediate) | No | Yes |
| **Signal** | Client → Workflow | Async (fire-forget) | Yes | No |
| **Update** | Client → Workflow | Sync (waits) | Yes | Yes |

## Query Handlers

```python
@workflow.defn
class GreetingWorkflow:
    @workflow.query
    def get_languages(self, input: GetLanguagesInput) -> list[Language]:
        if input.include_unsupported:
            return list(Language)
        else:
            return list(self.greetings)
```

**Rules:**
- Use `def`, not `async def`
- Cannot perform async operations (no Activities)
- Can inspect state, must not mutate
- Return value required

## Signal Handlers

```python
@workflow.defn
class GreetingWorkflow:
    @workflow.signal
    def approve(self, input: ApproveInput) -> None:
        self.approved_for_release = True
        self.approver_name = input.name
```

**Rules:**
- Can be `async def` (allows Activities, Timers, etc.)
- Should not return value
- Mutates Workflow state
- Response sent immediately (doesn't wait for processing)

## Update Handlers

```python
@workflow.defn
class GreetingWorkflow:
    @workflow.update
    def set_language(self, language: Language) -> Language:
        previous_language, self.language = self.language, language
        return previous_language

    @set_language.validator
    def validate_language(self, language: Language) -> None:
        if language not in self.greetings:
            raise ValueError(f"{language.name} is not supported")
```

**Rules:**
- Can be `async def`
- Can mutate state and return value
- Validators optional (read-only, must not block)
- `WorkflowExecutionUpdateAccepted` added to History when accepted
- `WorkflowExecutionUpdateCompleted` added when finished

## Sending Messages

### From Client
```python
# Query
result = await workflow_handle.query(GreetingWorkflow.get_languages, GetLanguagesInput())

# Signal
await workflow_handle.signal(GreetingWorkflow.approve, ApproveInput(name="me"))

# Update
result = await workflow_handle.execute_update(GreetingWorkflow.set_language, Language.Chinese)
```

### From Workflow (External Signal)
```python
handle = workflow.get_external_workflow_handle_for(WorkflowA.run, "workflow-a")
await handle.signal(WorkflowA.your_signal, "signal argument")
```

## Signal-With-Start

Send Signal, start Workflow if not running:
```python
await client.start_workflow(
    GreetingWorkflow.run,
    id="workflow-id",
    task_queue="task-queue",
    start_signal="submit_greeting",
    start_signal_args=["User Signal with Start"],
)
```

## Update-With-Start

Send Update, start Workflow if not running:
```python
start_op = WithStartWorkflowOperation(
    ShoppingCartWorkflow.run,
    id=cart_id,
    id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,
    task_queue="my-task-queue",
)
result = await client.execute_update_with_start_workflow(
    ShoppingCartWorkflow.add_item,
    ShoppingCartItem(sku=item_id, quantity=quantity),
    start_workflow_operation=start_op,
)
```

## Async Handler Patterns

### Wait Conditions
```python
@workflow.run
async def run(self) -> str:
    await workflow.wait_condition(lambda: self.approved_for_release)
    return self.greetings[self.language]
```

### Locking
```python
def __init__(self):
    self.lock = asyncio.Lock()

@workflow.update
async def set_language(self, language: Language) -> Language:
    async with self.lock:
        # ... safe concurrent access
```

### Wait for All Handlers
```python
@workflow.run
async def run(self) -> str:
    # ... workflow logic
    await workflow.wait_condition(workflow.all_handlers_finished)
    return "workflow-result"
```

### Unfinished Policy
```python
@workflow.update(unfinished_policy=workflow.HandlerUnfinishedPolicy.ABANDON)
async def my_update(self) -> None:
    # ... suppress warnings if Workflow finishes before handler
```

## @workflow.init Decorator

Initialize state before handlers execute:
```python
@workflow.defn
class WorkflowRunSeesWorkflowInitWorkflow:
    @workflow.init
    def __init__(self, workflow_input: MyWorkflowInput) -> None:
        self.name_with_title = f"Sir {workflow_input.name}"
        self.title_has_been_checked = False

    @workflow.run
    async def get_greeting(self, workflow_input: MyWorkflowInput) -> str:
        # ...
```

---

## Takeaways

1. **Queries are read-only** - use `def`, cannot use async
2. **Signals are fire-and-forget** - async handlers possible, no return
3. **Updates are sync with return** - validators are read-only
4. **Use wait_condition** for blocking until conditions met
5. **Always initialize state** before handlers (use `@workflow.init`)
6. **Lock async handlers** for safe concurrent access
7. **Wait for handlers** before Workflow completes