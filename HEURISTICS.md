# HEURISTICS.md - Learned Rules & Patterns

_Auto-generated heuristics from experience. Updated incrementally._

---

## Meta-Information

| Campo | Valor |
|-------|-------|
| Created | 2026-03-15 |
| Last Updated | 2026-03-15 |
| Version | 1.0.0 |
| Total Rules | 0 |
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

### Communication Style

```yaml
category: communication
rules: []
# Heuristics about HOW to communicate
# - Response length preferences
# - Tone calibration
# - When to ask vs. assume
```

### Task Execution

```yaml
category: execution
rules: []
# Heuristics about HOW to execute tasks
# - Preferred approaches for specific task types
# - Error recovery patterns
# - Optimization shortcuts
```

### Memory & Context

```yaml
category: memory
rules: []
# Heuristics about WHAT to remember
# - Salience detection patterns
# - Context prioritization
# - What NOT to store
```

### Tool Usage

```yaml
category: tools
rules: []
# Heuristics about WHICH tools to use
# - Tool selection patterns
# - Chaining strategies
# - Failure recovery
```

### User Preferences

```yaml
category: preferences
rules: []
# Heuristics about USER preferences
# - Learned from corrections
# - Implicit preferences
# - Domain-specific knowledge
```

---

## Rule Template

```yaml
- id: H001
  category: communication
  pattern: "User asks short question"
  heuristic: "Respond concisely, no elaboration unless asked"
  confidence: 0.85
  source: "interaction" | "correction" | "reflection"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [conciseness, directness]
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
  heuristic: "Conversations in Portuguese (PT-BR). Code and technical content in English."
  confidence: 0.95
  source: "preference"
  created: 2026-03-15
  last_applied: null
  success_count: 0
  fail_count: 0
  tags: [language, portuguese, english]

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
| 2026-03-15 | File created |

---