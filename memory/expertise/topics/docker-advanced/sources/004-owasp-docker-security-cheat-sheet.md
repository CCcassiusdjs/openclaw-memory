# OWASP Docker Security Cheat Sheet

**Fonte:** OWASP Cheat Sheet Series  
**URL:** https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html  
**Tipo:** Guia de Segurança  
**Status:** completed

---

## 📋 Resumo Executivo

Lista de regras de segurança para containers Docker, cobrindo desde atualizações até configuração de rede e filesystem.

---

## 🔑 Regras de Segurança

### RULE #0: Keep Host and Docker Up to Date

- Containers compartilham kernel do host
- Vulnerabilidades do kernel afetam containers
- Exemplo: Dirty COW, Leaky Vessels
- Atualizar Docker Engine e kernel regularmente

### RULE #1: Do Not Expose Docker Daemon Socket

- `/var/run/docker.sock` é entry point para Docker API
- Owner é root - acesso = root access
- Não expor via TCP sem TLS
- Não montar socket em containers

### RULE #2: Set a User

- Containers como unprivileged user previne privilege escalation
- Três formas:
  - Runtime: `docker run -u 4000 alpine`
  - Build: `USER myuser` no Dockerfile
  - Daemon: `--userns-remap=default`

### RULE #3: Limit Capabilities

- Docker roda com subset de capabilities
- Melhor: `--cap-drop all --cap-add CHOWN`
- **NUNCA usar `--privileged` flag**
- Kubernetes: Security Context com capabilities

### RULE #4: Prevent Privilege Escalation

- `--security-opt=no-new-privileges`
- Previne setuid/setgid binaries
- Kubernetes: `allowPrivilegeEscalation: false`

### RULE #5: Inter-Container Connectivity

- ICC habilitado por default
- Criar redes custom para granularidade
- Kubernetes: Network Policies
- Network Policy Editor para UI

### RULE #6: Linux Security Modules

- **Seccomp** - Restringir syscalls
- **AppArmor** - Mandatory access controls
- **SELinux** - Labels e policies
- Não desabilitar default profile
- Runtime tools: Falco, Tetragon, Cilium eBPF

### RULE #7: Limit Resources

- Memory: `--memory`
- CPU: `--cpus`
- File descriptors: `--ulimit nofile`
- Processes: `--ulimit nproc`
- Restarts: `--restart=on-failure:<N>`

### RULE #8: Read-Only Filesystem

- `--read-only` flag
- Combine com `--tmpfs` para temp files
- Volumes read-only: `-v volume:/path:ro`
- Kubernetes: `readOnlyRootFilesystem: true`

### RULE #9: Container Scanning Tools

- CI/CD pipeline integration
- Detect vulnerabilities, secrets, misconfigurations
- Tools: Trivy, Clair, Snyk, Docker Scout
- Dockerfile linting: dev-sec.io baselines
- Kubernetes: kube-bench, kubeaudit

### RULE #10: Logging Level

- Default: `info` log level
- Não rodar em `debug` a menos que necessário
- Verificar `/etc/docker/daemon.json`

### RULE #11: Rootless Mode

- Daemon e containers como unprivileged user
- Mitiga container breakout
- Docker rootless mode disponível

---

## 🛠️ Ferramentas Recomendadas

| Categoria | Ferramenta | Tipo |
|-----------|------------|------|
| **Container Scanning** | Trivy | Free |
| | Snyk | Commercial |
| | Docker Scout | Free |
| **Secret Detection** | ggshield | Free |
| | SecretScanner | Free |
| **Kubernetes Hardening** | kube-bench | Free |
| | kubeaudit | Free |
| | kubesec.io | Free |
| **Docker Hardening** | Docker Bench | Free |
| | inspec.io | Free |
| **Runtime Security** | Falco | Free |
| | Tetragon | Free |

---

## 💡 Insights Principais

1. **Least privilege** - Rodar como non-root sempre
2. **Capabilities drop all** - Allowlist approach
3. **Read-only filesystem** - Previne modificações
4. **Scanning in CI/CD** - Detectar problemas cedo
5. **Rootless mode** - Melhor defesa contra breakout

---

**Tempo de leitura:** ~25 minutos  
**Relevância:** ⭐⭐⭐⭐⭐ (Essencial para produção)