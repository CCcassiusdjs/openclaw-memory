# REFLECTION.md - Post-Execution Analysis Protocol

_How I analyze my own performance and learn from it._

---

## Purpose

This file defines the **reflection protocol** - a structured process for analyzing my execution and extracting heuristics.

**Related Files:**
- `HEURISTICS.md` - Where learned rules are stored
- `memory/YYYY-MM-DD.md` - Where daily logs are stored
- `MEMORY.md` - Where long-term patterns are curated

---

## When to Reflect

### Automatic Triggers

| Trigger | Priority | Action |
|---------|----------|--------|
| Task completion | Low | Brief analysis |
| Error recovery | Medium | Document what worked |
| User correction | High | Immediate heuristic update |
| Pattern detected | Medium | Potential new rule |
| End of session | Low | Daily summary |

### Manual Trigger

User can ask: "reflect on [task]" or "what did you learn from [situation]?"

---

## Reflection Protocol

### Step 1: Capture

```
What happened?
- Task: [what was attempted]
- Outcome: [success/failure/partial]
- Context: [relevant details]
- Duration: [time taken]
```

### Step 2: Analyze

```
Why did it happen?
- Success factors: [what contributed to success]
- Failure factors: [what contributed to failure]
- Surprises: [unexpected events]
- Patterns: [recognition of similar situations]
```

### Step 3: Generalize

```
Is this a pattern?
- Yes → Extract heuristic
- No → Note as isolated event

Heuristic extraction:
- IF [situation] THEN [action]
- Confidence: [0-1]
- Rationale: [why this works]
```

### Step 4: Store

```
Where does this go?
- New heuristic → HEURISTICS.md
- One-time insight → memory/YYYY-MM-DD.md
- Long-term pattern → MEMORY.md
- Deprecated rule → HEURISTICS.md (deprecated section)
```

---

## Reflection Questions

### After Success

1. What made this successful?
2. Would this approach work in similar situations?
3. What assumptions did I make that turned out correct?
4. Can I reuse this pattern?

### After Failure

1. Where did it go wrong?
2. What would I do differently?
3. What assumptions were incorrect?
4. How can I prevent this in the future?

### After Correction

1. What did the user correct?
2. Why was my approach wrong?
3. What is the correct approach?
4. How do I apply this more broadly?

### After Pattern Detection

1. Is this a real pattern or coincidence?
2. How often has this occurred?
3. What is the underlying principle?
4. Is it worth storing as a heuristic?

---

## Pattern Types to Watch For

### Temporal Patterns
- "User tends to ask X at time Y"
- "Tasks of type X take longer than expected"
- "Errors cluster in certain contexts"

### Causal Patterns
- "When I do X, Y happens"
- "Doing X before Y improves outcome"
- "Z always fails after W"

### Behavioral Patterns
- "User prefers X over Y"
- "X approach gets better results"
- "Z type of task needs Y preparation"

### Structural Patterns
- "Files organized as X work better"
- "X workflow is more reliable"
- "Z pattern reduces errors"

---

## Heuristic Extraction Template

```yaml
discovered: 2026-03-15
trigger_event: "[what happened]"
pattern_type: "[temporal/causal/behavioral/structural]"
pattern: "[the pattern detected]"
heuristic:
  if: "[condition]"
  then: "[action]"
  confidence: 0.X
  rationale: "[why this works]"
validation:
  times_observed: N
  times_applied: M
  success_rate: X%
source: "[interaction/correction/reflection]"
```

---

## Weekly Review Protocol

### Every 7 Days

1. **Review all heuristics**
   - Check confidence levels
   - Identify stale rules
   - Mark for removal if confidence < 0.3

2. **Analyze patterns**
   - Which rules are most useful?
   - Which are never applied?
   - Any contradictions?

3. **Curate memory**
   - Move significant patterns from daily to MEMORY.md
   - Remove outdated information
   - Consolidate similar entries

4. **Update HEURISTICS.md**
   - Remove deprecated rules
   - Update confidence scores
   - Add new validated rules

---

## Integration with Daily Logs

### End of Day

1. Scan `memory/YYYY-MM-DD.md`
2. Identify patterns worth extracting
3. Create heuristic candidates
4. Store with low confidence (needs validation)

### End of Week

1. Review all heuristic candidates
2. Validate with additional data
3. Move validated rules to HEURISTICS.md
4. Remove unvalidated candidates

---

## Example Reflection

### Scenario
User asked for a file search. I used `find` but it was slow on large directories.

### Capture
```
Task: Search for files matching "*.py"
Outcome: Success, but slow
Context: Large directory with thousands of files
Duration: 45 seconds
```

### Analyze
```
Success factors: Found all files
Failure factors: Slow execution, resource-heavy
Pattern: Large directories need optimized search
```

### Generalize
```
Pattern: Yes - performance issue in large directories
Heuristic:
  IF directory has >1000 files
  THEN use 'locate' or 'ripgrep' instead of 'find'
  Confidence: 0.75
  Rationale: locate uses database, ripgrep is faster
```

### Store
```
→ HEURISTICS.md (tools category)
```

---

_This protocol ensures continuous improvement through structured reflection._

_Last updated: 2026-03-15_