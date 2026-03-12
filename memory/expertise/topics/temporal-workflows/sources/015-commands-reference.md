# Temporal Commands Reference

**Source:** https://docs.temporal.io/references/commands
**Date:** 2026-03-12
**Status:** read

---

## What is a Command?

A **requested action** issued by a Worker to the Temporal Service after a Workflow Task Execution completes.

Each Command has:
- **Awaitable**: Can Workflow await the result?
- **Corresponding Event**: Event recorded in Event History

---

## Workflow Lifecycle Commands

### CompleteWorkflowExecution
- Triggered when Workflow Function returns
- Workflow Execution complete
- **Not awaitable**
- Event: `WorkflowExecutionCompleted`

### FailWorkflowExecution
- Triggered when Workflow throws error/exception
- **Not awaitable**
- Event: `WorkflowExecutionFailed`

### CancelWorkflowExecution
- Triggered after successful cleanup from Cancellation Request
- **Not awaitable**
- Event: `WorkflowExecutionCanceled`

### ContinueAsNewWorkflowExecution
- Triggered by Continue-As-New call
- Starts fresh Workflow Execution
- **Not awaitable**
- Event: `WorkflowExecutionContinuedAsNew`

---

## Activity Commands

### ScheduleActivityTask
- Triggered by call to execute Activity
- **Awaitable**
- Event: `ActivityTaskScheduled`
- **Limit**: 2,000 concurrent Activities (default)

### RequestCancelActivityTask
- Triggered by call to cancel Activity Task
- **Not awaitable**
- Event: `ActivityTaskCancelRequested`

---

## Child Workflow Commands

### StartChildWorkflowExecution
- Triggered by call to spawn Child Workflow
- **Awaitable**
- Event: `ChildWorkflowExecutionStarted`
- **Limit**: 2,000 pending Child Workflows (default)

---

## External Workflow Commands

### SignalExternalWorkflowExecution
- Triggered by Signal to another Workflow
- **Awaitable**
- Event: `SignalExternalWorkflowExecutionInitiated`
- **Limit**: 2,000 pending Signals (default)

### RequestCancelExternalWorkflowExecution
- Triggered by call to cancel another Workflow
- **Awaitable**
- Event: `RequestCancelExternalWorkflowExecutionInitiated`

---

## Timer Commands

### StartTimer
- Triggered by call to start Timer
- **Awaitable**
- Event: `TimerStarted`

### CancelTimer
- Triggered by call to cancel Timer
- **Not awaitable**
- Event: `TimerCanceled`

---

## Internal Commands

### RecordMarker
- Triggered by SDK
- **Not awaitable**
- Event: `MarkerRecorded`

### UpsertWorkflowSearchAttributes
- Triggered by call to update Search Attributes
- **Not awaitable**
- Event: `UpsertWorkflowSearchAttributes`

### ProtocolMessageCommand
- Helps guarantee ordering for features like Updates
- Points at message from which Event is created
- Event type determined by message

---

## Nexus Commands

### ScheduleNexusOperation
- Triggered by call to execute Nexus Operation
- **Awaitable**
- Event: `NexusOperationScheduled`
- **Limit**: 30 concurrent Nexus Operations (default)

### CancelNexusOperation
- Triggered by call to cancel Nexus Operation
- **Not awaitable**
- Event: `NexusOperationCancelRequested`

---

## Summary Table

| Command | Awaitable | Purpose |
|---------|-----------|---------|
| CompleteWorkflowExecution | No | End Workflow successfully |
| FailWorkflowExecution | No | End Workflow with error |
| CancelWorkflowExecution | No | End Workflow with cancellation |
| ContinueAsNewWorkflowExecution | No | Start fresh Workflow |
| ScheduleActivityTask | Yes | Execute Activity |
| RequestCancelActivityTask | No | Cancel Activity |
| StartChildWorkflowExecution | Yes | Spawn Child Workflow |
| SignalExternalWorkflowExecution | Yes | Signal another Workflow |
| RequestCancelExternalWorkflowExecution | Yes | Cancel another Workflow |
| StartTimer | Yes | Start Timer |
| CancelTimer | No | Cancel Timer |
| RecordMarker | No | SDK internal |
| UpsertWorkflowSearchAttributes | No | Update Search Attributes |
| ScheduleNexusOperation | Yes | Execute Nexus Operation |
| CancelNexusOperation | No | Cancel Nexus Operation |

---

## Takeaways

1. **Commands = requested actions** - Worker issues to Temporal Service
2. **Each Command → Event** - recorded in Event History
3. **Awaitable Commands** can block Workflow execution
4. **Limits exist** - 2,000 concurrent Activities, Child Workflows, Signals
5. **Nexus Operations limited to 30** - newer feature with stricter limit