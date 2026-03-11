# Kubernetes CronJobs - Official Documentation

**Source:** kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

CronJobs criam Jobs em um schedule repetitivo. Similar ao crontab do Unix, executa Jobs periodicamente baseado em uma expressão Cron.

## What is a CronJob?

### Definition
- Creates Jobs on a repeating schedule
- Uses Cron format syntax
- Suitable for backups, report generation, scheduled tasks
- Feature status: Stable (v1.21+)

### Example
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hello
spec:
  schedule: "* * * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hello
            image: busybox:1.28
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the Kubernetes cluster
          restartPolicy: OnFailure
```

## Schedule Syntax

### Cron Format
```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of week (0 - 6)
# │ │ │ │ │
# * * * * *
```

### Examples
- `0 3 * * 1` - Every Monday at 3 AM
- `*/15 * * * *` - Every 15 minutes
- `0 0 1 * *` - First day of month at midnight

### Special Entries

| Entry | Description | Equivalent |
|-------|-------------|------------|
| @yearly | Run once a year | 0 0 1 1 * |
| @monthly | Run once a month | 0 0 1 * * |
| @weekly | Run once a week | 0 0 * * 0 |
| @daily | Run once a day | 0 0 * * * |
| @hourly | Run once an hour | 0 * * * * |

### Time Zone
- Default: kube-controller-manager local time zone
- Set `.spec.timeZone` to specify time zone (v1.27+)
- Example: `timeZone: "Etc/UTC"`

## CronJob Spec

### Required Fields
- `schedule`: Cron expression
- `jobTemplate`: Template for Jobs

### Optional Fields

#### startingDeadlineSeconds
- Deadline for starting Job if missed schedule
- If missed, CronJob skips that instance
- Example: 200 seconds grace period

#### concurrencyPolicy
- `Allow` (default): Allow concurrent Jobs
- `Forbid`: Skip new Job if previous still running
- `Replace`: Replace running Job with new one

#### suspend
- Set to `true` to pause execution
- Does not affect already running Jobs
- Defaults to `false`

#### successfulJobsHistoryLimit
- Number of successful Jobs to keep
- Default: 3
- Set to 0 to keep none

#### failedJobsHistoryLimit
- Number of failed Jobs to keep
- Default: 1
- Set to 0 to keep none

## CronJob Limitations

### Unrelated CronJobs
- Multiple CronJobs can run concurrently
- concurrencyPolicy only applies to same CronJob

### Schedule Modification
- Changes apply to new Jobs only
- Running Jobs are not affected

### Job Creation
- Approximately once per schedule time
- May create 0, 1, or 2 Jobs in edge cases
- Jobs should be idempotent

### Missed Schedules
- If >100 missed schedules, logs error and doesn't start
- `startingDeadlineSeconds` changes count window
- CronJob counts missed schedules from last scheduled time

### Time Zone Issues
- CRON_TZ or TZ in schedule NOT supported
- Use `.spec.timeZone` field instead

## Best Practices

### Idempotency
Jobs should be idempotent because:
- May run twice in edge cases
- Should produce same result if run multiple times

### History Limits
Set appropriate limits:
- `successfulJobsHistoryLimit: 3` (default)
- `failedJobsHistoryLimit: 1` (default)
- Adjust based on debugging needs

### Concurrency
Choose wisely:
- `Allow` for independent tasks
- `Forbid` for tasks that shouldn't overlap
- `Replace` for tasks that should restart

### Deadline
Set `startingDeadlineSeconds` for:
- Catch-up after downtime
- Grace period for delayed starts
- Avoid infinite catch-up loops

## Key Takeaways

1. CronJobs create Jobs on schedule (Cron format)
2. Use `.spec.timeZone` for time zone (v1.27+)
3. concurrencyPolicy: Allow, Forbid, Replace
4. Set history limits for cleanup
5. Jobs should be idempotent
6. May miss schedules if >100 missed

## Personal Notes

CronJobs são essenciais para tarefas agendadas. A syntax Cron é familiar mas tem nuances.

Para CKA/CKAD:
- schedule: cron expression
- jobTemplate: defines Job structure
- concurrencyPolicy: Allow/Forbid/Replace
- startingDeadlineSeconds: grace period
- successfulJobsHistoryLimit/failedJobsHistoryLimit: cleanup

A limitação de 100 missed schedules é importante para entender comportamento em cenários de downtime. Jobs idempotentes são CRÍTICOS para evitar duplicação de trabalho.