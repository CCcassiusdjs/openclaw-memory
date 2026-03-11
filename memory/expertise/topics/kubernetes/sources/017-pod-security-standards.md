# Pod Security Standards

**Source:** https://kubernetes.io/docs/concepts/security/pod-security-standards/
**Type:** Official Documentation
**Category:** Security
**Read:** 2026-03-11

---

## Resumo

### Três Níveis de Política

| Profile | Descrição | Use Case |
|---------|-----------|----------|
| **Privileged** | Sem restrições | System/infra workloads, trusted users |
| **Baseline** | Minimamente restritivo | Common workloads, non-critical apps |
| **Restricted** | Altamente restritivo | Security-critical apps, low-trust users |

---

## Privileged Policy

**Características:** Sem restrições

- Permite privilege escalations
- Host namespaces permitidos
- Acesso completo ao host
- Usado para: system-level, infrastructure workloads

---

## Baseline Policy

### Controles Obrigatórios

| Control | Restrição |
|---------|-----------|
| **HostProcess** | Windows HostProcess containers não permitidos |
| **Host Namespaces** | hostNetwork, hostPID, hostIPC = false |
| **Privileged Containers** | privileged = false |
| **Capabilities** | Lista restrita de capabilities permitidas |
| **HostPath Volumes** | Proibido |
| **Host Ports** | Disallow ou lista conhecida |
| **Host Probes** | host field em probes/lifecycle = "" |
| **AppArmor** | RuntimeDefault, Localhost, ou undefined |
| **SELinux** | Tipos restritos (container_t, container_init_t, etc.) |
| **/proc Mount** | Default proc masks obrigatório |
| **Seccomp** | Não pode ser Unconfined |
| **Sysctls** | Apenas "safe" subset permitido |

### Capabilities Permitidas (Baseline)

```
AUDIT_WRITE, CHOWN, DAC_OVERRIDE, FOWNER, FSETID, KILL,
MKNOD, NET_BIND_SERVICE, SETFCAP, SETGID, SETPCAP, SETUID, SYS_CHROOT
```

### Sysctls Permitidos (Baseline)

```
kernel.shm_rmid_forced
net.ipv4.ip_local_port_range
net.ipv4.ip_unprivileged_port_start
net.ipv4.tcp_syncookies
net.ipv4.ping_group_range
net.ipv4.ip_local_reserved_ports (v1.27+)
net.ipv4.tcp_keepalive_time (v1.29+)
net.ipv4.tcp_fin_timeout (v1.29+)
net.ipv4.tcp_keepalive_intvl (v1.29+)
net.ipv4.tcp_keepalive_probes (v1.29+)
```

---

## Restricted Policy

**Herdar:** Todos os controles Baseline +

### Controles Adicionais

| Control | Restrição |
|---------|-----------|
| **Volume Types** | Apenas configMap, csi, downwardAPI, emptyDir, ephemeral, persistentVolumeClaim, projected, secret |
| **Privilege Escalation** | allowPrivilegeEscalation = false |
| **Run as Non-root** | runAsNonRoot = true |
| **Run as Non-root User** | runAsUser != 0 |
| **Seccomp** | RuntimeDefault ou Localhost (obrigatório) |
| **Capabilities** | drop ALL, add apenas NET_BIND_SERVICE |

### Volume Types Permitidos

```yaml
# Exemplo de volumes permitidos
volumes:
- name: config
  configMap: {...}
- name: data
  persistentVolumeClaim: {...}
- name: tmp
  emptyDir: {...}
- name: secret
  secret: {...}
# hostPath NÃO permitido
```

---

## Exemplos de Aplicação

### Namespace Labels

```yaml
# Privileged
apiVersion: v1
kind: Namespace
metadata:
  name: privileged-ns
  labels:
    pod-security.kubernetes.io/enforce: privileged
    pod-security.kubernetes.io/enforce-version: latest
```

```yaml
# Baseline
apiVersion: v1
kind: Namespace
metadata:
  name: baseline-ns
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/enforce-version: latest
```

```yaml
# Restricted
apiVersion: v1
kind: Namespace
metadata:
  name: restricted-ns
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
```

---

## Modos de Aplicação

| Mode | Comportamento |
|------|--------------|
| **enforce** | Bloqueia Pods que violam a política |
| **audit** | Registra violações no audit log |
| **warn** | Avisa o usuário sobre violações |

### Labels

```yaml
pod-security.kubernetes.io/<MODE>: <PROFILE>
pod-security.kubernetes.io/<MODE>-version: <VERSION>
```

---

## Alternativas de Enforcement

| Ferramenta | Tipo |
|------------|------|
| **Pod Security Admission** | Built-in (recomendado) |
| **Kyverno** | Policy engine |
| **OPA Gatekeeper** | Policy engine |
| **Kubewarden** | Policy engine |

---

## Conceitos-Chave

1. **Cumulative**: Restricted herda Baseline
2. **Privileged = Unrestricted**: Use apenas quando necessário
3. **Baseline = Minimal**: Prevenção de privilege escalations
4. **Restricted = Best Practices**: Pod hardening
5. **Enforcement via Labels**: Namespace-level
6. **Version Pinning**: Para compatibilidade

---

## Linux vs Windows

- **Linux**: Maioria dos controles é Linux-only
- **Windows**: Muitos securityContext fields sem efeito
- **Especificar OS**: `spec.os.name: linux` ou `windows`