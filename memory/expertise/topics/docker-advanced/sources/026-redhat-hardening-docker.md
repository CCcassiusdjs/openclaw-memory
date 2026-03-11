# Hardening Docker Containers, Images, and Host - Security Toolkit

**Fonte:** https://www.redhat.com/en/blog/hardening-docker-containers-images-and-host-security-toolkit
**Data:** 2026-03-11
**Status:** Lido

---

## Resumo

Guia abrangente de hardening para containers Docker, cobrindo host OS, container runtime e práticas de segurança.

## Segurança do Host OS

### Módulos de Segurança Linux

| Módulo | Tipo | Abordagem |
|--------|------|-----------|
| **SELinux** | MAC (Mandatory Access Control) | Baseado em type enforcement |
| **AppArmor** | MAC | Baseado em paths de filesystem |
| **seccomp** | Syscall filtering | Restringe system calls |

### SELinux
```policy
policy_module(localpolicy, 1.0)
gen_require(`
 type user_t;
 type var_log_t;
')
allow user_t var_log_t:dir { getattr search open read };
```
- Baseado em tipos e privilégios
- Política complexa, curva de aprendizado íngreme

### AppArmor
```apparmor
#include <tunables/global>
/usr/sbin/nginx {
 #include <abstractions/apache2-common>
 #include <abstractions/base>
 capability net_bind_service,
 /data/www/safe/* r,
 deny /data/www/unsafe/* r,
}
```
- Baseado em paths de arquivos
- Mais intuitivo que SELinux
- Bom para restringir acesso de aplicações

### Seccomp
```json
{
 "defaultAction": "SCMP_ACT_ALLOW",
 "syscalls": [
   { "name": "mkdir", "action": "SCMP_ACT_ERRNO" },
   { "name": "chown", "action": "SCMP_ACT_ERRNO" }
 ]
}
```
- Restringe system calls
- Ações: allow, kill, err, trap
- Requer conhecimento extensivo de Linux

### Capabilities
- Grupos de permissões para processos filhos
- Processos não podem adquirir novas capabilities
- **Cuidado com:**
  - `SYS_ADMIN`: privilégios de root
  - `SETUID`: pode ser substituído por capabilities mais granulares

## Práticas de Segurança no Container Runtime

### 1. Unix Socket (/var/run/docker.sock)
**Risco:** Container com socket montado pode controlar Docker daemon
**Solução:** SELinux/AppArmor profiles para limitar montagem

### 2. Volume Mounts
**Risco:** Diretórios sensíveis do host (/etc/, /usr/) podem ser modificados
**Solução:** Montar como read-only

### 3. Privileged Containers
**Risco:** Containers privilegiados têm todas as capabilities
**Solução:** Usar capabilities granulares em vez de `--privileged`

### 4. SSH dentro do Container
**Risco:** Dificulta gestão de chaves e políticas de acesso
**Solução:**
- Não rodar SSH dentro do container
- Usar `docker exec` ou `docker attach` do host

### 5. Binding Privileged Ports
**Risco:** Portas < 1024 expostas indevidamente
**Solução:** Verificar mapeamentos:
```bash
docker ps --quiet | xargs docker inspect --format '{{ .Id }}: Ports={{ .NetworkSettings.Ports }}'
```

### 6. Exposing Ports
**Risco:** Portas desnecessárias expostas
**Solução:** Auditar portas expostas regularmente

### 7. Desabilitar AppArmor/SELinux/seccomp
**Risco:** `--unconfined` remove proteções padrão
**Solução:** Nunca desabilitar perfis padrão do Docker

### 8. Sharing Host Namespaces
**Risco:** `--pid` e `--net` permitem ver/matar processos do host
**Solução:** Evitar compartilhar namespaces

### 9. TLS no Docker Daemon
**Risco:** Daemon em TCP sem TLS = comunicação não criptografada
**Solução:** Habilitar TLS seguindo docs.docker.com/engine/security/https/

### 10. Mount Propagation Mode
**Risco:** Modo `shared` permite outros containers montarem e modificar volumes
**Solução:**
```bash
# Verificar propagação
docker ps --quiet --all | xargs docker inspect --format '{{ .Id }}: Propagation={{range $mnt := .Mounts}} {{json $mnt.Propagation}} {{end}}'

# Não usar shared mode
# docker run --volume=/hostPath:/containerPath:shared  # EVITAR
```

### 11. no_new_privileges
**Risco:** Processos podem ganhar privilégios via setuid/sgid
**Solução:**
```bash
# Verificar
docker ps --quiet --all | xargs docker inspect --format '{{ .Id }}: SecurityOpt={{.HostConfig.SecurityOpt }}'

# Habilitar
docker run --security-opt=no-new-privileges
```

## Checklist de Segurança

| Área | Prática |
|------|---------|
| Host OS | SELinux/AppArmor/seccomp configurados |
| Docker Socket | Restringir montagem |
| Volumes | Montar sensíveis como read-only |
| Containers | Não usar `--privileged` |
| SSH | Não rodar dentro do container |
| Ports | Auditar mapeamentos |
| Namespaces | Não compartilhar com host |
| TLS | Habilitar no daemon TCP |
| Mount Propagation | Evitar modo `shared` |
| Privileges | Usar `no_new_privileges` |

## Conclusão

O hardening de containers é multi-camada:
1. **Host OS**: SELinux/AppArmor/seccomp
2. **Runtime**: Práticas específicas do Docker
3. **Monitoramento**: Plataforma de segurança para runtime phase

---
*Referência: CIS Docker Benchmark*