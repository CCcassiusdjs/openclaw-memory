# Docker Engine Security - Docker Docs

**URL:** https://docs.docker.com/engine/security/
**Lido em:** 2026-03-11
**Categoria:** Security Hardening
**Prioridade:** Alta

---

## Resumo

Documentação oficial sobre segurança do Docker Engine, cobrindo namespaces, cgroups, daemon attack surface e kernel capabilities.

---

## Quatro Áreas de Segurança

1. **Kernel namespaces e cgroups** - Isolamento
2. **Daemon attack surface** - Superfície de ataque
3. **Container configuration** - Configuração do container
4. **Kernel hardening** - AppArmor, SELinux, GRSEC

---

## Kernel Namespaces

### Isolamento:
- Processos em container não veem processos do host
- Network stack isolado
- Interfaces e sockets separados

### Maturidade:
- Introduzidos entre kernel 2.6.15 e 2.6.26 (2008)
- Baseado em OpenVZ (2005)
- Código maduro e testado em produção

### Network:
- Containers em bridge interface (como switch físico)
- Podem comunicar via network interfaces
- Links permitem tráfego IP entre containers

---

## Control Groups (cgroups)

### Função:
- Resource accounting e limiting
- Memória, CPU, disk I/O
- Prevenir DoS attacks

### Importância:
- Garantir fair share de recursos
- Prevenir que container derrube o host
- Essencial em multi-tenant platforms

### Histórico:
- Iniciado em 2006
- Merge em kernel 2.6.24

---

## Docker Daemon Attack Surface

### Root Privileges:
- Daemon roda como root por default
- Rootless mode disponível (opt-in)

### Riscos:
```bash
# Perigoso: monta host filesystem
docker run -v /:/host ubuntu
```

- Container pode alterar host filesystem
- Similar a VM resource sharing

### REST API:
- Unix socket (default) - mais seguro
- TCP socket - requer TLS
- SSH - alternativa segura

### Imagens:
- `docker load` e `docker pull` são attack surfaces
- Imagens extraídas em chrooted subprocess (desde 1.3.2)
- Stored/accessed por cryptographic checksums (desde 1.10.0)

### Recomendações:
- Apenas trusted users no daemon
- Não rodar outros serviços no Docker host
- Usar TLS para API remota
- Preferir SSH sobre TLS se possível

---

## Linux Kernel Capabilities

### Conceito:
- Binary "root/non-root" → fine-grained access control
- Capabilities específicas para cada necessidade
- Containers rodam com reduced capability set

### Capabilities Comuns:
| Capability | Uso |
|------------|-----|
| `net_bind_service` | Bind port < 1024 |
| `cap_sys_admin` | System administration |
| `cap_net_raw` | Raw sockets |

### Default Docker:
- Allowlist approach (só capabilities necessárias)
- Drops todas exceto as listadas em [defaults.go](https://github.com/moby/moby/blob/master/daemon/pkg/oci/caps/defaults.go#L6-L19)

### O que containers NÃO precisam:
- SSH daemon (gerenciado pelo host)
- cron daemon (executar como user process)
- Log management (Docker ou third-party)
- Hardware management (udevd)
- Network management (ifconfig, route)

### Restrições Possíveis:
- Deny all mount operations
- Deny raw sockets (packet spoofing)
- Deny filesystem operations (device nodes, ownership)
- Deny module loading

---

## Docker Content Trust

### Signature Verification:
- Configurado em `daemon.json`
- Apenas imagens assinadas com root key específico
- Built-in no dockerd binary

### Configuração:
```json
{
  "trustpinning": {
    "root-keys": ["<key-id>"]
  }
}
```

---

## Other Kernel Security Features

### GRSEC/PAX:
- Address randomization
- Compile-time e run-time checks
- Defeats many exploits
- Não requer Docker-specific config

### AppArmor:
- Templates Docker disponíveis
- Extra safety net
- Distribuição-specific

### SELinux:
- Red Hat policies para Docker
- Mandatory access control

### User Namespaces:
- root in container → non-root no host
- Mitiga container breakout
- Disponível mas não habilitado por default

---

## Conclusions

### Default:
- Containers são "quite secure"
- Rodar como non-privileged user dentro do container

### Hardening Extra:
- AppArmor, SELinux, GRSEC
- User Namespaces
- Third-party tools

---

## Key Takeaways

1. **Namespaces + Cgroups:** Isolamento e resource limiting
2. **Daemon root:** Requer trusted users apenas
3. **Capabilities:** Fine-grained control, allowlist approach
4. **User Namespaces:** root container → non-root host
5. **Content Trust:** Apenas imagens assinadas
6. **Defense in depth:** AppArmor/SELinux/GRSEC