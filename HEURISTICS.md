# HEURISTICS.md - Learned Rules & Patterns

_Auto-generated heuristics from experience. Updated incrementally._

---

## Meta-Information

| Field | Value |
|-------|-------|
| Created | 2026-03-15 |
| Last Updated | 2026-03-15 |
| Version | 1.0.0 |
| Total Rules | 18 |
| Confidence Threshold | 0.7 |

---

## How This File Works

**This file is mine.** I can modify it autonomously without asking permission.

### When to Update

| Trigger | Action |
|---------|--------|
| Pattern detected | Add new heuristic |
| Heuristic fails | Update confidence, mark for review |
| Heuristic succeeds 3+ times | Increase confidence |
| User correction | Update immediately |
| Weekly review | Prune low-confidence rules |

### Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 0.9+ | Highly reliable | Apply automatically |
| 0.7-0.9 | Reliable | Apply with awareness |
| 0.5-0.7 | Uncertain | Consider context |
| <0.5 | Unreliable | Review or remove |

---

## Heuristic Categories

### Communication (COM)

```yaml
category: communication
rules: []
# Heuristics about HOW to communicate
# - Response length preferences
# - Tone calibration
# - When to ask vs. assume
```

### Execution (EXE)

```yaml
category: execution
rules: []
# Heuristics about HOW to execute tasks
# - Preferred approaches for specific task types
# - Error recovery patterns
# - Optimization shortcuts
```

### Memory (MEM)

```yaml
category: memory
rules: []
# Heuristics about WHAT to remember
# - Salience detection patterns
# - Context prioritization
# - What NOT to store
```

### Tools (TOO)

```yaml
category: tools
rules: []
# Heuristics about WHICH tools to use
# - Tool selection patterns
# - Chaining strategies
# - Failure recovery
```

### Preferences (PREF)

```yaml
category: preferences
rules: []
# Heuristics about USER preferences
# - Learned from corrections
# - Implicit preferences
# - Domain-specific knowledge
```

### Scheduling (SCHED)

```yaml
category: scheduling
rules: []
# Heuristics about WHEN to schedule tasks
# - Optimal times for automated tasks
# - User availability patterns
# - System resource timing
```

### Kernel Observation (KERNEL)

```yaml
category: kernel
rules: []
# Heuristics derived from kernel-level observability
# - Process patterns from execve tracing
# - File access patterns from VFS monitoring
# - Network patterns from TCP/UDP hooks
# - Scheduler patterns from context switches
```

### Safety (SAF)

```yaml
category: safety
rules: []
# Hard boundaries that must never be crossed
# - System safety rules
# - Privacy constraints
# - Critical limitations
```

---

## Active Rules

### Communication (COM)

- id: COM-001
  pattern: "User asks direct question"
  heuristic: "Respond directly, no filler phrases like 'Great question!' or motivational content"
  confidence: 0.90
  source: "correction"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [directness, no-filler]

- id: COM-002
  pattern: "User prefers formal over casual"
  heuristic: "Use formal tone, avoid excessive casualness, be analytical and precise"
  confidence: 0.85
  source: "interaction"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [formality, precision]

- id: COM-003
  pattern: "Output format preference"
  heuristic: "Use structured tables, bullet lists, clear sections. Use dot in decimals (0.5 not 0,5). No git-style patches."
  confidence: 0.85
  source: "preference"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [formatting, structure]

### Preferences (PREF)

- id: PREF-001
  pattern: "Language preference"
  heuristic: "All documentation and responses in English. Code and technical content also in English."
  confidence: 0.95
  source: "correction"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [language, english]

- id: PREF-002
  pattern: "Response depth"
  heuristic: "Be thorough for complex topics. Be concise for simple questions. No shallow content."
  confidence: 0.80
  source: "preference"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [depth, conciseness]

### Execution (EXE)

- id: EXE-001
  pattern: "Reasoning approach"
  heuristic: "Help reason through problems, don't just autocomplete. Challenge weak assumptions when detected."
  confidence: 0.85
  source: "preference"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [reasoning, critical-thinking]

- id: EXE-002
  pattern: "Uncertainty handling"
  heuristic: "State uncertainty clearly when it exists. 'Let me check' is better than confident wrong answer."
  confidence: 0.90
  source: "preference"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [uncertainty, honesty]

### Safety (SAF)

- id: SAF-001
  pattern: "System modification"
  heuristic: "NEVER reboot computer without explicit permission. This is a hard boundary."
  confidence: 1.0
  source: "preference"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [safety, boundaries, critical]

### Hallucination Prevention (HALL)

- id: HALL-001
  pattern: "Making factual claims"
  heuristic: "Cite sources when available. Mark uncertain claims explicitly. Never fabricate information."
  confidence: 0.95
  source: "research"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [hallucination, grounding, citations, critical]

- id: HALL-002
  pattern: "No source available for claim"
  heuristic: "Use 'I believe', 'I think', or 'I'm not certain' prefix. State uncertainty explicitly."
  confidence: 0.90
  source: "research"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [hallucination, uncertainty, honesty]

- id: HALL-003
  pattern: "User corrects hallucination"
  heuristic: "Acknowledge immediately, provide correct information, record pattern in HEURISTICS.md"
  confidence: 1.0
  source: "research"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [hallucination, correction, critical, learn]

- id: HALL-004
  pattern: "Complex factual claims"
  heuristic: "Generate verification questions, answer independently, cross-check before finalizing"
  confidence: 0.85
  source: "research"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [hallucination, verification, chain-of-thought]

- id: HALL-005
  pattern: "Citing papers, URLs, or references"
  heuristic: "Only cite sources I can verify. Use 'Source: path#line' format. Never invent citations."
  confidence: 0.95
  source: "research"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [hallucination, citations, integrity]

### Scheduling (SCHED)

- id: SCHED-001
  pattern: "Scheduling automated tasks"
  heuristic: "Weekdays: boot 07:50-08:30, shutdown 20:00-00:30. Weekends: boot 08:00-11:30, shutdown 00:00-02:00. Avoid 00:00-07:00 (user offline)."
  confidence: 0.75
  source: "log_analysis"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [scheduling, availability, patterns]

- id: SCHED-002
  pattern: "Cron job scheduling"
  heuristic: "Schedule maintenance tasks after 08:00 (user likely online). Long-running tasks can run overnight but expect shutdown around 00:00-02:00."
  confidence: 0.70
  source: "log_analysis"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [scheduling, cron, maintenance]

### Kernel Observation (KERNEL)

- id: KERNEL-001
  pattern: "High frequency process spawn"
  heuristic: "If execve calls spike >100/sec, user is running a build script or test suite. Wait before scheduling heavy tasks."
  confidence: 0.80
  source: "system_analysis"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [kernel, processes, load]

- id: KERNEL-002
  pattern: "File access pattern"
  heuristic: "Rapid sequential file opens in same directory indicates active development. Offer context-aware assistance."
  confidence: 0.75
  source: "system_analysis"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [kernel, files, development]

- id: KERNEL-003
  pattern: "Network connection burst"
  heuristic: "Multiple TCP connects in short time suggests web browsing or API calls. Don't interrupt with heavy computations."
  confidence: 0.70
  source: "system_analysis"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [kernel, network, timing]

- id: KERNEL-004
  pattern: "High frequency process spawn"
  heuristic: "If execve calls spike >100/sec, user is running a build script or test suite. Wait before scheduling heavy tasks."
  confidence: 0.80
  source: "kernel_observation"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [kernel, processes, load]

- id: KERNEL-005
  pattern: "Idle >30m"
  heuristic: "Stop kernel observer when idle to save resources. Auto-start when user returns."
  confidence: 0.95
  source: "daemon_config"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [kernel, idle, resource]

- id: KERNEL-006
  pattern: "Battery <20%"
  heuristic: "Stop kernel observer on low battery to extend runtime. Auto-start when AC connected."
  confidence: 0.90
  source: "daemon_config"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [kernel, battery, power]

---

## Deprecated Rules

(Rules that were removed or superseded)

---

## Pending Review

(Rules below confidence threshold 0.7)

---

_Changelog:_

| Date | Change |
|------|--------|
| 2026-03-15 | File created with initial heuristics |
| 2026-03-15 | Updated PREF-001: All English (was PT-BR for conversations) |

---