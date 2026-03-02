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

---

## 📊 Tracking State

**State file:** `memory/heartbeat-state.json`

```json
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": null
  },
  "lastHeartbeat": null,
  "checksToday": 0
}
```

---

## 🚨 When to Reach Out

**Do reach out when:**
- ✅ Important email arrived
- ✅ Calendar event <2h
- ✅ Something interesting found
- ✅ >8h since last message

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
**Last review:** 2026-03-01
