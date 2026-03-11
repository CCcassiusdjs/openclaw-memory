# Kubernetes Jobs - Official Documentation

**Source:** kubernetes.io/docs/concepts/workloads/controllers/job/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Jobs executam tarefas one-off que rodam até completar. Um Job cria um ou mais Pods e continua até que um número específico de Pods termine com sucesso.

## What is a Job?

### Definition
- Runs Pods until successful completion
- Tracks successful completions
- Retries on failure
- Deletes Pods when Job is deleted

### Use Cases
- Batch processing
- One-off tasks
- Scheduled jobs (via CronJob)
- Parallel processing

## Job Types

### 1. Non-parallel Jobs
- Single Pod (unless failure)
- Complete when Pod succeeds
- Default: completions=1, parallelism=1

### 2. Parallel Jobs with Fixed Completion Count
- Set `.spec.completions` to N
- Job complete when N Pods succeed
- Each Pod completion is homologous

### 3. Parallel Jobs with Work Queue
- Don't set `.spec.completions`
- Set `.spec.parallelism` to desired workers
- Pods coordinate themselves or with external service
- Complete when any Pod succeeds and all terminate

### 4. Indexed Jobs
- Each Pod gets an index (0 to completions-1)
- Available via: annotation, label, hostname, env var
- Complete when one Pod succeeds per index

## Job Spec

### Required Fields
- `apiVersion`: batch/v1
- `kind`: Job
- `metadata`: name, labels
- `spec.template`: Pod template (required)
- `spec.template.spec.restartPolicy`: Never or OnFailure

### Example
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl:5.34.0
        command: ["perl", "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

### Parallelism Control
- `.spec.parallelism`: Number of Pods running simultaneously
- Default: 1
- Set to 0 to pause Job
- Can be scaled up/down during execution

### Completion Mode
- `NonIndexed` (default): Each completion is equivalent
- `Indexed`: Each Pod gets unique index

## Handling Failures

### Container Failures
- If `restartPolicy: OnFailure`: Container restarts in same Pod
- If `restartPolicy: Never`: New Pod created

### Pod Failures
- Job controller creates replacement Pod
- Application must handle restart scenarios
- Clean up temporary files, locks, partial output

### Backoff Limit
- `.spec.backoffLimit`: Max retries before marking Job as failed
- Default: 6
- Counts failed Pods with `restartPolicy: Never`

### Active Deadline Seconds
- `.spec.activeDeadlineSeconds`: Max duration for Job
- Job marked failed after timeout
- Overrides backoffLimit

## Job Patterns

### 1. External Service + Work Queue
- Job coordinates with external service
- External service provides work items

### 2. Queue Service
- Job acts as queue reader
- Multiple Jobs can share queue

### 3. Indexed Job with Static Work
- Each Pod works on predetermined subset
- Index determines work assignment

### 4. Job Template
- CronJob uses Job template
- Template defines Job structure

## Pod Selection

### Automatic Labels
Jobs automatically add labels:
- `batch.kubernetes.io/job-name`: Job name
- `batch.kubernetes.io/controller-uid`: Job UID

### Finding Job Pods
```bash
kubectl get pods --selector=batch.kubernetes.io/job-name=pi
```

## Cleaning Up Finished Jobs

### Manual Cleanup
```bash
kubectl delete job/pi
```

### Automatic Cleanup
- Set `.spec.ttlSecondsAfterFinished` for auto-deletion
- TTL controller deletes finished Jobs after specified time

### History Limits
- CronJobs have `.spec.successfulJobsHistoryLimit`
- CronJobs have `.spec.failedJobsHistoryLimit`

## Key Takeaways

1. Jobs run until successful completion
2. Three types: Non-parallel, Fixed completion, Work queue
3. Indexed Jobs provide unique pod indices
4. Use backoffLimit for retry limits
5. Use activeDeadlineSeconds for timeouts
6. TTL controller can auto-delete finished Jobs

## Personal Notes

Jobs são fundamentais para batch processing. A distinção entre os tipos de paralelismo é importante.

Para CKA/CKAD:
- restartPolicy: Never ou OnFailure (não Always)
- backoffLimit: max retries
- activeDeadlineSeconds: timeout
- parallelism: pods simultâneos
- completions: pods necessários

A feature de TTLSecondsAfterFinished é útil para cleanup automático de Jobs completos.