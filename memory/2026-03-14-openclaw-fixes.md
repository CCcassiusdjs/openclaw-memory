# OpenClaw Fixes - 2026-03-14

## Correções Aplicadas

### 1. Rate Limiter (Crítico)
**Problema:** Bloqueio agressivo após poucas tentativas de autenticação.

**Correção:**
```json
"authRateLimiter": {
  "closeAfter": 50,
  "logEvery": 10,
  "windowMs": 60000
}
```
- Permite até 50 tentativas antes de fechar conexão
- Log a cada 10 tentativas
- Janela de 60 segundos

### 2. Verbose Default
**Problema:** Usuário não vê raciocínio do agente.

**Correção:** `verboseDefault: "reasoning"`
- Mostra raciocínio interno por padrão
- Antes: "on" (apenas ferramentas)
- Depois: "reasoning" (raciocínio)

### 3. Cache Rotation
**Problema:** Cache cresce sem limite (4.5 GB encontrado).

**Correção:** Crontab diário
```bash
0 3 * * * rm -f ~/.openclaw/logs/cache-trace.jsonl 2>/dev/null
```
- Executa às 03:00 diariamente
- Remove cache trace

### 4. Limites Aumentados (Anterior)
- Read limit: 50KB → 10GB
- Download limit: 250MB → 10GB
- Web fetch: 200KB → 1GB chars
- Bootstrap per file: 20KB → 100KB
- Bootstrap total: 150KB → 500KB

### 5. Permissões Corrigidas (Anterior)
- Arquivos root em `/home/csilva/src/openclaw/` → ownership corrigido

## Configuração Final do Control UI
```json
"controlUi": {
  "enabled": true,
  "allowedOrigins": [
    "http://localhost:18789",
    "http://127.0.0.1:18789",
    "http://cassius-laptop:18789",
    "http://192.168.1.*:18789",
    "http://10.*.*.*:18789"
  ],
  "dangerouslyAllowHostHeaderOriginFallback": true,
  "allowInsecureAuth": true,
  "dangerouslyDisableDeviceAuth": true
}
```

## Problemas Pendentes

1. **qmd timeout** - Sistema de memória com timeout de 120s
   - Acontece frequentemente durante boot
   - Precisa otimização ou timeout adaptativo

2. **Interface Web HTTP** - UX confusa para erro de device identity
   - Recomendado: Tailscale Serve para HTTPS automático
   - Alternativa: aceitar que HTTP é inseguro e melhorar UX

## Comandos Úteis

```bash
# Verificar status
curl http://127.0.0.1:18789/health

# Reiniciar gateway
openclaw gateway restart

# Ver logs
journalctl --user -u openclaw-gateway -f

# Limpar cache manualmente
rm -f ~/.openclaw/logs/cache-trace.jsonl
```