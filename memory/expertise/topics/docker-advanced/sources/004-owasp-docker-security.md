# OWASP Docker Security Cheat Sheet

**Fonte:** https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
**Tipo:** Guia de Segurança
**Lido em:** 2026-03-10
**Status:** completed

---

## Regras de Segurança Docker (OWASP)

### RULE #0 - Keep Host and Docker up to date
- Containers compartilham kernel do host
- Vulnerabilidades de kernel afetam todos containers
- Exemplo: Dirty COW, Leaky Vessels
- **Ação:** Atualizar kernel + Docker Engine regularmente

### RULE #1 - Do not expose the Docker daemon socket
- `/var/run/docker.sock` = acesso root irrestrito
- **NUNCA:**
  - `-H tcp://0.0.0.0:XXX` (expõe Docker daemon)
  - `-v /var/run/docker.sock:/var/run/docker.sock` (monta socket em container)
- Socket read-only também é risco

### RULE #2 - Set a user
Rodar containers como usuário não-privilegiado:

**Runtime:**
```bash
docker run -u 4000 alpine
```

**Build time (Dockerfile):**
```dockerfile
FROM alpine
RUN groupadd -r myuser && useradd -r -g myuser myuser
USER myuser
```

**Daemon level:**
```bash
dockerd --userns-remap=default
```

**Kubernetes:**
```yaml
securityContext:
  runAsUser: 4000
```

### RULE #3 - Limit capabilities
Capacidades Linux = privilégios granulares

**Melhor prática:**
```bash
docker run --cap-drop all --cap-add CHOWN alpine
```

**NUNCA usar `--privileged`** (adiciona TODAS as capacidades)

**Kubernetes:**
```yaml
securityContext:
  capabilities:
    drop:
      - ALL
    add: ["CHOWN"]
```

### RULE #4 - Prevent in-container privilege escalation
```bash
docker run --security-opt=no-new-privileges <image>
```

**Kubernetes:**
```yaml
securityContext:
  allowPrivilegeEscalation: false
```

### RULE #5 - Inter-Container Connectivity (icc)
- Default: containers comunicam entre si via docker0 bridge
- Alternativa: criar redes específicas para grupos de containers
- Kubernetes: usar Network Policies

### RULE #6 - Use Linux Security Modules
Não desativar perfil de segurança default!

**Seccomp:**
- Restringe syscalls ao mínimo necessário
- Docker tem perfil default

**AppArmor:**
- Mandatory Access Controls per-container
- `docker run --security-opt apparmor=<profile>`

**SELinux:**
- Habilitar no host e label containers corretamente

**Runtime Security Tools:**
- Falco, Tetragon, Cilium eBPF
- Monitoramento comportamental

### RULE #7 - Limit resources
Previnir DoS com limits:

```bash
docker run \
  --memory="512m" \
  --cpus="1.5" \
  --restart=on-failure:5 \
  --ulimit nofile=1024 \
  --ulimit nproc=100 \
  <image>
```

### RULE #8 - Read-only filesystem and volumes
```bash
docker run --read-only --tmpfs /tmp alpine
```

**Docker Compose:**
```yaml
services:
  alpine:
    image: alpine
    read_only: true
```

**Volumes read-only:**
```bash
docker run -v volume-name:/path:ro alpine
docker run --mount source=vol,destination=/path,readonly alpine
```

**Kubernetes:**
```yaml
securityContext:
  readOnlyRootFilesystem: true
```

### RULE #9 - Container scanning in CI/CD
Issues comuns detectadas:
- USER directive especificada
- Base image version pinned
- OS packages versions pinned
- COPY ao invés de ADD
- Sem curl bashing em RUN

### RULE #10 - Use trusted base images
- Verificar proveniência
- Usar imagens oficiais ou assinadas
- Docker Content Trust

### RULE #11 - Run Docker in rootless mode
- Docker daemon roda como usuário não-root
- Mitiga riscos de container breakout
- `dockerd-rootless.sh` script

---

## Checklist de Segurança

- [ ] Host e Docker atualizados
- [ ] Daemon socket não exposto
- [ ] Containers rodam como non-root user
- [ ] Capabilities limitadas (--cap-drop all --cap-add)
- [ ] no-new-privileges habilitado
- [ ] Resources limits configurados
- [ ] Filesystem read-only
- [ ] Volumes montados como read-only
- [ ] Container scanning no CI/CD
- [ ] Base images de fontes confiáveis
- [ ] Seccomp/AppArmor/SELinux configurados

## Próximos Passos
- [ ] Estudar Docker Content Trust
- [ ] Configurar rootless mode
- [ ] Implementar container scanning no CI