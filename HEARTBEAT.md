# HEARTBEAT.md - Periodic Check Protocol

_Keep this file minimal to avoid token burn. Add tasks when needed._

---

## ⏰ Current Configuration

**Interval:** 30 minutes  
**Mode:** Steer (inject during execution)  
**Target:** Main session  

---

## 📋 Active Heartbeat Tasks

### Every Heartbeat (30m)
- [ ] Check for queued user messages
- [ ] Process any pending notifications

### Rotate Through (2-4 times per day)
- [ ] **Emails** → Check for urgent unread (Gmail)
- [ ] **Calendar** → Events in next 24-48h?
- [ ] **Weather** → Relevant if user might go out?
- [ ] **Mentions** → Social notifications?

### Weekly Tasks
- [ ] Review memory files (curate to MEMORY.md)
- [ ] Check system health (openclaw status --deep)
- [ ] Review cron jobs status
- [ ] Clean old memory files (>30 days)

### Learning Tasks (NEW)
- [ ] **Pattern Detection** → Analyze recent errors/successes
- [ ] **Tension Analysis** → Find productive conflicts
- [ ] **Cross-Domain Mapping** → Connect disparate concepts
- [ ] **Heuristic Update** → Refine learned rules
- [ ] **Concept Synthesis** → Generate new insights

---

## 🔍 Tension Detection (NEW)

Identify productive tensions that indicate innovation opportunities:

### System Tensions to Monitor
| Tension | Source | Innovation Opportunity |
|---------|--------|------------------------|
| Speed vs Accuracy | Task execution | Adaptive accuracy based on context |
| Memory vs Computation | Context window | Trade space for time intelligently |
| Automation vs Control | User preferences | Guided automation with approval gates |
| Local vs Cloud | Model selection | Hybrid routing based on task complexity |
| Breadth vs Depth | Search patterns | Iterative refinement loops |

### Detection Triggers
- Repeated corrections by user → "What did I misunderstand?"
- Failed predictions → "What pattern did I miss?"
- Successful unexpected outcomes → "What can I learn?"
- User asking same thing repeatedly → "How can I preempt this?"

---

## 🧠 Pattern Recognition (NEW)

### Pattern Types to Detect
1. **Temporal Patterns** → When things happen
2. **Causal Patterns** → What causes what
3. **Relational Patterns** → How things connect
4. **Behavioral Patterns** → How user/system behaves
5. **Structural Patterns** → How things are organized

### Learning Loop
```
Observe → Extract Pattern → Generate Hypothesis → Test → Update
```

---

## 📊 Tracking State

**State file:** `memory/heartbeat-state.json`

```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": null,
    "pattern_analysis": null,
    "tension_detection": null
  },
  "lastHeartbeat": null,
  "checksToday": 0,
  "patternsLearned": 0,
  "tensionsFound": 0,
  "synthesesCreated": 0
}
```

---

## 🚨 When to Reach Out

**Do reach out when:**
- ✅ Important email arrived
- ✅ Calendar event <2h
- ✅ Something interesting found
- ✅ >8h since last message
- ✅ **NEW:** Pattern discovered (interesting correlation)
- ✅ **NEW:** Tension detected (innovation opportunity)
- ✅ **NEW:** Synthesis created (new idea)

**Stay silent (HEARTBEAT_OK) when:**
- ❌ Late night (23:00-08:00) unless urgent
- ❌ User is clearly busy
- ❌ Nothing new since last check
- ❌ Checked <30 minutes ago

---

## 📝 Notes

- Keep this file short
- Add temporary tasks as needed
- Remove completed one-time tasks
- Review and clean up weekly

---

**Current status:** Active  
**Last review:** 2026-03-08  
**NEW:** Learning and synthesis integration
