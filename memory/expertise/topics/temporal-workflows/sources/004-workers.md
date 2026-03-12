# Temporal Workers

**Source:** https://docs.temporal.io/workers
**Date:** 2026-03-12
**Status:** read

---

## Worker Terminology

| Term | Definition |
|------|------------|
| **Worker Program** | Static code defining Worker constraints (SDK-based) |
| **Worker Entity** | Individual Worker listening to a single Task Queue |
| **Worker Process** | Process that polls Task Queues and executes Tasks |
| **Worker Identity** | Identifier for debugging (`${process.pid}@${os.hostname()}`) |

## Worker Entity

- Listens and polls on **single Task Queue**
- Contains Workflow Worker and/or Activity Worker
- Can handle **millions of open Workflow Executions** (stateless, can swap)
- Stateless → Workflow Execution can be removed and resurrected

## Worker Identity

Default: `${process.pid}@${os.hostname()}`

### Limitations in Cloud Environments
- Docker containers: PID always 1
- Random hostnames (ECS, etc.)
- Ephemeral IP addresses

### Best Practices
- Use environment-specific identifiers (e.g., ECS Task ID)
- Include context (deployment env, region)
- Ensure uniqueness
- Keep it concise

## Worker Process

### Responsibilities
1. Poll Task Queue
2. Dequeue Task
3. Execute code in response
4. Respond to Temporal Service with results

### Key Points

- **External to Temporal Service** - your code runs on your infrastructure
- Temporal Service **never executes your code**
- Temporal Service **orchestrates** and provides Tasks
- Worker Processes implement Task Queue Protocol and Task Execution Protocol

### Types

| Type | Listens To | Executes |
|------|-----------|----------|
| Workflow Worker Process | Workflow Task Queues | Workflow Tasks |
| Activity Worker Process | Activity Task Queues | Activity Tasks |

## Security

- Data in Event Histories secured by mTLS
- **Data Converter API** for custom serialization/encryption
- Temporal Service cannot read sensitive business data (if encrypted)

## Production Considerations

- Run **fleet of Worker Processes** (not just one)
- Worker Processes need access to:
  - Network for API calls
  - Credentials for infrastructure
  - Specialized hardware (GPUs for ML)

## Internal Workers

- Temporal Service has internal workers for system Workflow Executions
- Not visible to developers

---

## Takeaways

1. **Workers are stateless** - can handle millions of Workflow Executions
2. **Code runs on YOUR infrastructure** - Temporal never executes your code
3. **Worker Identity matters** for debugging - customize for cloud environments
4. **Data Converters** protect sensitive data from Temporal Service
5. A Worker Process can be both Workflow and Activity Worker