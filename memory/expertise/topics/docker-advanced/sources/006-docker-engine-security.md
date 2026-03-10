# Docker Engine Security

**Fonte:** https://docs.docker.com/engine/security/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Quatro Áreas de Segurança Docker

1. **Kernel security** - Namespaces e cgroups
2. **Daemon attack surface** - Superfície de ataque do Docker daemon
3. **Container configuration** - Configuração de containers (default ou custom)
4. **Kernel hardening** - Interação com features de segurança do kernel

---

## 1. Kernel Namespaces

### Isolamento
- Processos em containers não veem/afetam processos de outros containers
- Cada container tem seu próprio network stack
- Containers são como máquinas físicas conectadas via switch Ethernet

### Maturidade
- Namespaces: introduzidos entre kernel 2.6.15 e 2.6.26 (2008)
- Baseado em OpenVZ (lançado em 2005)
- Código maduro e testado em produção

---

## 2. Control Groups (cgroups)

### Função
- Resource accounting e limiting
- Memória, CPU, disk I/O justos para cada container
- Previnir DoS por exaustão de recursos

### Importância
- Essencial em multi-tenant platforms (PaaS)
- Garante uptime consistente mesmo com aplicações mal-comportadas

### Histórico
- Código iniciado em 2006
- Merged em kernel 2.6.24

---

## 3. Docker Daemon Attack Surface

### Riscos do Docker Daemon
- Requer root privileges (a menos que rootless mode)
- Acesso ao daemon = acesso root ao host

### Perigos Comuns
1. **Compartilhar diretórios sem limitação**
   ```bash
   # PERIGOSO - container pode alterar host
   docker run -v /:/host alpine
   ```

2. **Expor REST API via TCP**
   - NUNCA: `-H tcp://0.0.0.0:2375`
   - Se necessário: usar HTTPS + certificados

3. **Montar docker.sock em container**
   ```bash
   # PERIGOSO - acesso root irrestrito
   docker run -v /var/run/docker.sock:/var/run/docker.sock ...
   ```

### Proteções
- Desde Docker 0.5.2: Unix socket (não TCP)
- Desde Docker 1.3.2: chroot para extração de imagens
- Desde Docker 1.10.0: imagens por checksum criptográfico

### Recomendações
- Apenas usuários confiáveis controlam o daemon
- Usar SSH ou TLS para acesso remoto
- Servidor dedicado para Docker (apenas SSH + monitoring)

---

## 4. Linux Kernel Capabilities

### O que são
- Transformam binário root/non-root em fine-grained access control
- Processos podem ter capacidades específicas sem precisar de root completo

### Capacidades Comuns
| Capability | Função |
|------------|--------|
| CAP_NET_BIND_SERVICE | Bind portas < 1024 |
| CAP_NET_RAW | Raw sockets |
| CAP_SYS_ADMIN | Operações admin |
| CAP_CHOWN | Mudar ownership |
| CAP_DAC_OVERRIDE | Bypass DAC |

### Docker Default
- **Allowlist approach** - apenas capacidades necessárias são permitidas
- Default: capacidades limitadas, não root completo

### Capabilities vs Root
Containers rodam como "root" mas com menos privilégios que root real:
- Sem mount operations
- Sem raw sockets (previne spoofing)
- Sem criar device nodes
- Sem alterar file attributes
- Sem module loading

### Gerenciamento de Capabilities
```bash
# Remover todas e adicionar específicas
docker run --cap-drop all --cap-add NET_BIND_SERVICE ...

# Ver lista completa
man 7 capabilities
```

---

## 5. Docker Content Trust

### Assinatura de Imagens
- Engine pode ser configurado para rodar apenas imagens assinadas
- Configurado em `daemon.json`

```json
{
  "trustpinning": {
    "pinning": {
      "base-image": "trust"
    }
  }
}
```

---

## 6. Outras Features de Segurança

### User Namespaces
- Root dentro do container = non-root fora
- Mitiga container breakout
- Disponível mas não habilitado por default
- `--userns-remap=default`

### LSM (Linux Security Modules)
| Sistema | Descrição |
|---------|-----------|
| **AppArmor** | Profiles per-container, default em Ubuntu |
| **SELinux** | Labels em containers, default em RHEL |
| **GRSEC/PAX** | Hardening kernel-wide |
| **Seccomp** | Filtra syscalls |

### Ferramentas de Runtime Security
- **Falco** - Monitoramento de comportamento
- **Tetragon** - eBPF security
- **Cilium** - Network security + observability

---

## Checklist de Segurança

- [ ] Docker e kernel atualizados
- [ ] Daemon socket protegido (não exposto via TCP)
- [ ] Containers rodam como non-root
- [ ] Capabilities limitadas
- [ ] Resource limits configurados
- [ ] Read-only filesystem quando possível
- [ ] Seccomp/AppArmor/SELinux habilitados
- [ ] Content Trust para imagens
- [ ] Container scanning no CI/CD
- [ ] User namespaces habilitados
- [ ] API protegida com TLS/HTTPS

---

## Próximos Passos
- [ ] Estudar User Namespaces em detalhes
- [ ] Configurar Seccomp profiles
- [ ] Implementar Falco para runtime security