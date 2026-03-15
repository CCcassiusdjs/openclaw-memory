# OpenClaw - Documentação Completa

**Fonte:** https://docs.openclaw.ai
**Data:** 2026-03-14

---

## Visão Geral

OpenClaw é uma plataforma de assistente AI pessoal/autônomo com:
- **Gateway**: Daemon que gerencia canais, sessões, ferramentas
- **Agentes**: Múltiplos agentes isolados com workspaces separados
- **Canais**: WhatsApp, Telegram, Discord, Signal, iMessage, IRC, etc.
- **Ferramentas**: exec, browser, memory, nodes, canvas, lobster, etc.

---

## Arquitetura

### Componentes Principais

| Componente | Descrição |
|------------|-----------|
| **Gateway** | Daemon principal (porta 18789) |
| **Workspace** | `~/.openclaw/workspace` - arquivos do agente |
| **Agent Dir** | `~/.openclaw/agents/<id>/agent` - auth profiles |
| **Sessions** | `~/.openclaw/agents/<id>/sessions` - histórico |
| **Config** | `~/.openclaw/openclaw.json` - configuração |

### Arquivos de Contexto

| Arquivo | Propósito |
|---------|-----------|
| `AGENTS.md` | Instruções operacionais do agente |
| `SOUL.md` | Personalidade e tom |
| `USER.md` | Preferências do usuário |
| `MEMORY.md` | Memória de longo prazo (curada) |
| `memory/YYYY-MM-DD.md` | Logs diários brutos |
| `TOOLS.md` | Notas sobre ferramentas locais |
| `IDENTITY.md` | Identidade do agente |
| `HEARTBEAT.md` | Protocolo de verificação periódica |
| `BOOTSTRAP.md` | Script de inicialização (deletar após uso) |

---

## Canais Suportados

### WhatsApp (Baileys)
- **Status**: Production-ready
- **Autenticação**: QR code pairing
- **Recursos**: Mensagens, mídia, grupos, reações, polls

**Configuração:**
```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      allowFrom: ["+15551234567"],
      groupPolicy: "allowlist",
    },
  },
}
```

**Comandos:**
```bash
openclaw channels login --channel whatsapp
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

### Telegram (Bot API)
- **Status**: Production-ready
- **Autenticação**: Bot token via BotFather
- **Recursos**: DMs, grupos, fóruns, inline buttons, streaming

**Configuração:**
```json5
{
  channels: {
    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

### Discord (Gateway)
- **Status**: Production-ready
- **Autenticação**: Bot token via Developer Portal
- **Recursos**: Guilds, threads, components v2, voice

**Configuração:**
```json5
{
  channels: {
    discord: {
      enabled: true,
      token: "BOT_TOKEN",
      groupPolicy: "allowlist",
      guilds: {
        "SERVER_ID": {
          requireMention: false,
          users: ["USER_ID"],
        },
      },
    },
  },
}
```

### Outros Canais
- **Signal**: Via signal-cli
- **iMessage**: macOS only
- **IRC**: Standard IRC protocol
- **Slack**: Bot API
- **Google Chat**: Bot API
- **Matrix**: Via matrix-sdk
- **Line**: LINE Notify
- **BlueBubbles**: iOS/iPadOS bridge
- **Zalo**: Zalo API
- **Nostr**: Decentralized protocol
- **Feishu**: Lark/Feishu bot

---

## Ferramentas (Tools)

### Exec
- Execução de comandos shell
- Background execution (`yieldMs`, `background`)
- PTY para TTY-required CLIs
- Modos de segurança: `deny`, `allowlist`, `full`
- Modos de ask: `off`, `on-miss`, `always`

### Browser
- Controle de navegador via OpenClaw server
- Perfis: `openclaw` (isolado), `chrome-relay` (extensão), `user` (navegador do usuário)
- Ações: navegar, screenshot, click, type, evaluate
- Modo sandbox para isolamento

### Memory Tools
- `memory_search`: Busca semântica em MEMORY.md + memory/*.md
- `memory_get`: Leitura segura de snippets

### Nodes
- Gerenciamento de dispositivos pareados (Android, iOS, macOS)
- Câmera, tela, localização, notificações
- Execução remota de comandos

### Canvas
- Apresentação de UI em nós
- Avaliação de JavaScript
- A2UI para interações

### Lobster
- Workflow engine com pipelines
- Aprovações resumíveis
- JSON envelope tipado

### LLM-Task
- Tarefas LLM com JSON schema validation
- Orquestração via workflows

### Sub-agents
- Spawn de agentes isolados (`sessions_spawn`)
- Runtime: `subagent` ou `acp`
- Modos: `run` (one-shot), `session` (persistente)

### Sessions
- `sessions_list`: Lista sessões
- `sessions_history`: Histórico de mensagens
- `sessions_send`: Enviar mensagem para sessão
- `sessions_yield`: Terminar turno atual

### Message
- Envio de mensagens multi-canal
- Ações: send, react, poll, thread-create
- Suporte a mídia, stickers, TTS

### TTS/Voice
- Conversão texto→fala
- Chamadas de voz via voice-call plugin

### Web Tools
- `web_search`: Brave Search API
- `web_fetch`: Extração de conteúdo de URLs

### Cron
- Jobs agendados (status, list, add, update, remove, run)
- Wake events para heartbeat

### Gateway
- Restart, config management
- Update in-place

---

## Multi-Agent Routing

### Conceitos

| Termo | Definição |
|-------|-----------|
| `agentId` | Um "cérebro" (workspace, auth, sessions separados) |
| `accountId` | Uma conta de canal (ex: WhatsApp pessoal vs trabalho) |
| `binding` | Roteamento de mensagens para `agentId` |

### Prioridade de Bindings (mais específico primeiro)

1. `peer` match (DM/grupo/canal específico)
2. `parentPeer` match (herança de thread)
3. `guildId + roles` (Discord role routing)
4. `guildId` (Discord)
5. `teamId` (Slack)
6. `accountId` match
7. Channel-level match (`accountId: "*"`)
8. Fallback para agente default

### Exemplo: WhatsApp Multi-Agente

```json5
{
  agents: {
    list: [
      { id: "home", workspace: "~/.openclaw/workspace-home" },
      { id: "work", workspace: "~/.openclaw/workspace-work" },
    ],
  },
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

---

## Sandbox & Segurança

### Modos de Sandbox

| Modo | Comportamento |
|------|---------------|
| `off` | Sem sandbox |
| `all` | Sempre sandboxed |
| `allowlist` | Sandbox para comandos não permitidos |

### Escopos de Sandbox

| Escopo | Isolamento |
|--------|------------|
| `shared` | Container compartilhado |
| `agent` | Container por agente |

### Configuração Per-Agent

```json5
{
  agents: {
    list: [
      {
        id: "personal",
        sandbox: { mode: "off" },
      },
      {
        id: "family",
        sandbox: { mode: "all", scope: "agent" },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit"],
        },
      },
    ],
  },
}
```

---

## ACP Agents (Codex/Claude Code)

### Sessões ACP
- Runtime `acp` para coding agents
- Modos: `run` (one-shot), `session` (persistente)
- Thread-binding para Discord/Telegram

### Comandos
```bash
/acp spawn <agent> --thread here|auto
/acp steer <sessionId> <message>
/acp list
```

### Configuração
```json5
{
  agents: {
    list: [
      {
        id: "codex",
        runtime: {
          type: "acp",
          acp: {
            agent: "codex",
            backend: "acpx",
            mode: "persistent",
            cwd: "/workspace/openclaw",
          },
        },
      },
    ],
  },
}
```

---

## Skills

### O que são Skills
- Extensões modulares para capacidades específicas
- Localizadas em `~/.openclaw/skills/` ou `workspace/skills/`
- Cada skill tem `SKILL.md` com instruções

### Skills Disponíveis

| Skill | Descrição |
|-------|-----------|
| `clawhub` | Gerenciar skills do ClawHub |
| `coding-agent` | Delegar tarefas de código |
| `gh-issues` | GitHub issues automation |
| `github` | Operações GitHub via `gh` CLI |
| `healthcheck` | Hardening de segurança |
| `nano-pdf` | Editar PDFs com linguagem natural |
| `node-connect` | Diagnosticar conexão de nodes |
| `openai-whisper` | Speech-to-text local |
| `session-logs` | Analisar logs de sessão |
| `skill-creator` | Criar/editar skills |
| `tmux` | Controle remoto de tmux |
| `video-frames` | Extrair frames de vídeos |
| `voice-call` | Chamadas de voz |

### Uso de Skills
1. Ler `<description>` para determinar aplicabilidade
2. Se aplicar, ler `SKILL.md` em `<location>`
3. Seguir instruções do skill

---

## Automation (Cron)

### Agendamento

| Tipo | Schema |
|------|--------|
| `at` | One-shot: `{ "kind": "at", "at": "<ISO-8601>" }` |
| `every` | Recorrente: `{ "kind": "every", "everyMs": <ms> }` |
| `cron` | Cron expression: `{ "kind": "cron", "expr": "0 9 * * *" }` |

### Payload Types

| Tipo | Uso |
|------|-----|
| `systemEvent` | Injetar texto como evento |
| `agentTurn` | Rodar agente com mensagem |

### Delivery Modes

| Modo | Comportamento |
|------|---------------|
| `none` | Sem entrega |
| `announce` | Enviar para chat |
| `webhook` | POST HTTP |

---

## Heartbeat Protocol

### Quando Atingir
- Email importante chegou
- Evento de calendário <2h
- Algo interessante encontrado
- >8h desde última mensagem

### Quando Silenciar (HEARTBEAT_OK)
- 23:00-08:00 (horário noturno)
- Usuário claramente ocupado
- Nada novo desde última verificação
- Verificado <30 minutos atrás

### Tarefas Rotativas (2-4x/dia)
- **Emails**: Mensagens urgentes não lidas
- **Calendar**: Eventos em 24-48h
- **Weather**: Se usuário pode sair
- **Mentions**: Notificações sociais

---

## Reply Tags

### Tags de Resposta Nativa
- `[[reply_to_current]]`: Responde à mensagem atual
- `[[reply_to:<id>]]`: Responde a mensagem específica

**Importante:** Tag deve ser o PRIMEIRO token (sem texto antes).

---

## Modelos & Providers

### Providers Suportados
- OpenAI (GPT, Codex)
- Anthropic (Claude)
- Ollama (modelos locais)
- Google (Gemini)
- DeepSeek (via Ollama)
- Cloud providers via gateway

### Aliases
- DeepSeek: `ollama/deepseek-r1:latest`

### Model Override
- `/model <model_id>` para trocar modelo na sessão
- `/status` para ver modelo atual

---

## CLI Reference

### Comandos Principais

```bash
# Status
openclaw status
openclaw health

# Gateway
openclaw gateway start|stop|restart
openclaw gateway --port 18789

# Channels
openclaw channels login --channel whatsapp
openclaw channels status --probe

# Pairing
openclaw pairing list <channel>
openclaw pairing approve <channel> <code>

# Agents
openclaw agents add <id>
openclaw agents list --bindings

# Config
openclaw config get <path>
openclaw config set <path> <value>

# Logs
openclaw logs --follow

# Doctor
openclaw doctor [--fix]
```

---

## Credential Storage Map

| Credencial | Localização |
|------------|-------------|
| WhatsApp | `~/.openclaw/credentials/whatsapp/<accountId>/creds.json` |
| Telegram bot token | `channels.telegram.botToken` ou env |
| Discord bot token | `channels.discord.token` ou env |
| Model auth profiles | `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` |
| Pairing allowlists | `~/.openclaw/credentials/<channel>-allowFrom.json` |

---

## Troubleshooting

### Problemas Comuns

**WhatsApp não conecta:**
- QR code expirado → `openclaw channels login`
- Reconnect loop → `openclaw doctor`

**Telegram bot não responde:**
- Privacy mode → `/setprivacy` → Disable
- Grupo não listado → Adicionar em `groups`

**Discord bot não vê mensagens:**
- Message Content Intent → Enable
- Server Members Intent → Enable

**Exec approvals:**
- Configurar `channels.<channel>.execApprovals.approvers`
- Apenas approvers podem aprovar

**Voice STT drops:**
- `daveEncryption=true` (default)
- `decryptionFailureTolerance=24`

---

## Links Úteis

- **Docs:** https://docs.openclaw.ai
- **Source:** https://github.com/openclaw/openclaw
- **Community:** https://discord.com/invite/clawd
- **Skills:** https://clawhub.com

---

_Last updated: 2026-03-14_