# TOOLS.md - Local Tool Notes

_Your environment-specific tool configurations and conventions._

---

## 🔧 Tool Configuration Status

### Core Tools (Always Available)
| Tool | Status | Notes |
|------|--------|-------|
| **exec** | ✅ Full | Background execution enabled, security=full, ask=on-miss |
| **process** | ✅ Full | Manage background sessions (list, poll, log, kill) |
| **read** | ✅ Full | Text files + images (jpg, png, gif, webp) |
| **write** | ✅ Full | Auto-creates parent directories |
| **edit** | ✅ Full | Exact text replacement |
| **apply_patch** | ✅ Enabled | Workspace-only mode (safe) |

### Web Tools
| Tool | Status | Configuration |
|------|--------|---------------|
| **web_search** | ✅ Active | Brave Search API (key configured) |
| **web_fetch** | ✅ Active | HTML → Markdown extraction |
| **browser** | ✅ Available | Chrome/OpenClaw profiles |

### Memory Tools
| Tool | Status | Configuration |
|------|--------|---------------|
| **memory_search** | ✅ Active | Vector + FTS, local embedding model |
| **memory_get** | ✅ Active | Safe snippet retrieval |

### Session Tools
| Tool | Status | Notes |
|------|--------|-------|
| **sessions_list** | ✅ Active | List sessions with filters |
| **sessions_history** | ✅ Active | Fetch message history |
| **sessions_send** | ✅ Active | Send to other sessions |
| **sessions_spawn** | ✅ Active | Sub-agent creation |
| **session_status** | ✅ Active | Usage + time + cost |

### Advanced Tools
| Tool | Status | Notes |
|------|--------|-------|
| **lobster** | ✅ Enabled | Workflow engine (CLI installed) |
| **llm-task** | ✅ Enabled | JSON-only LLM calls |
| **subagents** | ✅ Active | Orchestration (list, steer, kill) |
| **canvas** | ✅ Available | Node canvas control |
| **nodes** | ✅ Available | Camera, screen, location |

### Communication Tools
| Tool | Status | Configuration |
|------|--------|---------------|
| **message** | ✅ Active | WhatsApp configured (+55 51 99769-4222) |
| **tts** | ⚠️ Not configured | No voice provider setup |
| **voice_call** | ⚠️ Not configured | No phone provider setup |

---

## 📧 Email Tools

### Gmail (Primary)
```bash
# Location
cd /home/csilva/.openclaw/workspace/skills/imap-smtp-email

# Config file
.env (configured for cassiojonesdhein@gmail.com)

# Check emails
node scripts/imap.js check --limit 10 --recent 1m

# Search emails
node scripts/imap.js search --unseen --recent 24h --limit 20

# Send email
node scripts/smtp.js send --to recipient@email.com --subject "Subject" --body "Body"
```

**Server Config:**
- IMAP: `imap.gmail.com:993` (TLS)
- SMTP: `smtp.gmail.com:587` (STARTTLS)
- Auth: App Password (2FA enabled)

### PUCRS Email (Pending)
```
Status: ⚠️ IMAP blocked by institution
Email: c.jones@edu.pucrs.br
Recommendation: Setup forwarding to Gmail
```

---

## 📱 WhatsApp Integration

### Status
- ✅ Connected: +55 51 99769-4222
- ✅ Full background execution enabled
- ✅ Elevated mode enabled for this number
- ✅ Cron job configured (email check every minute)

### Commands That Work
```
"verifique meus emails" → Check Gmail
"envie email para X" → Send via SMTP
"rode: <command>" → Execute shell command
"pesquise: <query>" → Web search
```

### Configuration
```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "elevated": true,
      "allowCommands": true,
      "allowFrom": ["+5551997694222"]
    }
  }
}
```

---

## 🔐 Safe Bins (No Approval Needed)

These commands run without approval:
```
cat, grep, sed, awk, jq, head, tail, wc, sort, uniq, cut, tr, xargs, find, ls, pwd, echo, printf
```

**Trusted directories:**
- `/bin`
- `/usr/bin`

---

## 🛠️ Custom Scripts & Aliases

### Workspace Utilities
```bash
# Git commit helper
alias oc-commit='cd ~/.openclaw/workspace && git add . && git commit -m'

# Status check
alias oc-status='openclaw status --deep'

# Memory check
alias oc-memory='openclaw config get agents.defaults.memorySearch'
```

### Email Check Script
```bash
#!/bin/bash
# ~/bin/check-email.sh
cd /home/csilva/.openclaw/workspace/skills/imap-smtp-email
node scripts/imap.js check --limit 5 --recent 5m | jq '.[] | {from, subject, date}'
```

---

## 📊 System Resources

### Current Limits
| Resource | Limit | Notes |
|----------|-------|-------|
| **Max Concurrent Agents** | 16 | Configured |
| **Max Sub-agents** | 32 | Configured |
| **Timeout (default)** | 1800s | 30 minutes |
| **Context Tokens** | 200k | Per session |

### Model Configuration
| Model | Provider | Context | Max Tokens | Status |
|-------|----------|---------|------------|--------|
| qwen3.5:397b-cloud | Ollama | 256k | 65536 | ✅ Primary |
| glm-4.7:cloud | Ollama | 198k | 32768 | ✅ Fallback |

---

## 🔧 Tool-Specific Notes

### exec Tool
- **Security mode:** `full` (strictest)
- **Ask mode:** `on-miss` (ask when not in safe bins)
- **Background:** Enabled with `yieldMs` or `background: true`
- **PTY:** Available for TTY-required CLIs

### browser Tool
- **Profiles:** `chrome` (extension relay), `openclaw` (isolated)
- **Default:** `chrome` (when extension attached)
- **Target:** `host` (default), `sandbox`, `node`

### memory_search Tool
- **Vector index:** Ready (embeddinggemma-300M)
- **FTS index:** Ready
- **Cache:** Enabled
- **Files indexed:** MEMORY.md + memory/*.md

### lobster Tool
- **CLI:** Installed (`/usr/local/bin/lobster`)
- **Status:** Enabled in tools.alsoAllow
- **Use case:** Workflow automation with approvals

---

## ⚠️ Tool Limitations & Gotchas

### Known Issues
1. **apply_patch** → Workspace-only by default (safe)
2. **browser** → Needs Chrome extension attached for `profile="chrome"`
3. **tts/voice_call** → Not configured (no provider)
4. **PUCRS email** → IMAP blocked, needs forwarding

### Workarounds
- **Email from PUCRS:** Setup Gmail forwarding
- **Remote browser access:** Use Tailscale or SSH tunnel
- **Voice features:** Configure ElevenLabs or similar provider

---

## 📝 Tool Usage Patterns

### Recommended Patterns

**File Operations:**
```bash
# Read large files (use offset/limit)
read --path file.txt --offset 1 --limit 100

# Edit precisely (exact match required)
edit --path file.txt --oldText "exact text" --newText "replacement"

# Write with auto-directory creation
write --path new/dir/file.txt --content "content"
```

**Background Execution:**
```bash
# Long-running command (auto-background after 10s)
exec --command "long-task" --yieldMs 10000

# Immediate background
exec --command "background-task" --background true

# Poll for results
process --action poll --sessionId <id> --timeout 30000
```

**Memory Operations:**
```bash
# Search memory (semantic)
memory_search --query "what did we decide about X" --maxResults 5

# Get specific snippet
memory_get --path MEMORY.md --from 10 --lines 20
```

---

## 🔑 API Keys & Credentials

### Configured
| Service | Key Location | Status |
|---------|-------------|--------|
| **Brave Search** | openclaw.json (redacted) | ✅ Active |
| **Gmail** | .env (app password) | ✅ Active |
| **WhatsApp** | Session token | ✅ Active |

### Not Configured
| Service | Needed For | Priority |
|---------|-----------|----------|
| **ElevenLabs** | TTS voices | Low |
| **Twilio** | Voice calls | Low |
| **Telegram Bot** | Telegram channel | Medium |
| **Discord Bot** | Discord channel | Low |

---

_Last updated: 2026-03-01_
_Next review: When tools are added/removed or configuration changes_
