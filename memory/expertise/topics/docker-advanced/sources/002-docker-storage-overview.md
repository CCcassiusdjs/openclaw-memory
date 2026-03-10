# Docker Storage Overview

**Fonte:** https://docs.docker.com/engine/storage/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. Dois Conceitos de Storage

| Conceito | Descrição | Documentação |
|----------|-----------|--------------|
| **Container Data Persistence** | Armazenar dados fora dos containers (volumes, bind mounts, tmpfs) | Esta página |
| **Daemon Storage Backends** | Como o daemon armazena image layers e container layers | containerd image store, storage drivers |

### 2. Container Layer Basics
- Arquivos criados dentro do container → writable layer (topo das image layers)
- Dados no writable layer **não persistem** quando container é destruído
- Cada container tem seu próprio writable layer
- Difícil extrair dados do writable layer

### 3. Tipos de Storage Mounts

| Tipo | Descrição | Use Case |
|------|-----------|----------|
| **Volume Mounts** | Gerenciados pelo Docker daemon, persistem após container removido | Produção, dados críticos, performance |
| **Bind Mounts** | Link direto host ↔ container, acessível de ambos | Desenvolvimento, config files |
| **tmpfs Mounts** | Armazenados em memória RAM, não escritos em disco | Dados sensíveis, cache temporário |
| **Named Pipes** | Comunicação host ↔ container (Windows) | IPC, Docker Engine API |

### 4. Volume Mounts vs Bind Mounts

**Volumes:**
- Gerenciados pelo Docker (`/var/lib/docker/volumes/`)
- Isolados do host
- Podem ser compartilhados entre containers
- Funcionam em Linux e Windows
- Mais fáceis de backup/migrate
- Performance: direto no filesystem do host

**Bind Mounts:**
- Dependem da estrutura de diretórios do host
- Acessíveis de dentro e fora do container
- Não isolados pelo Docker
- Processos Docker e não-Docker podem modificar

### 5. tmpfs Mounts
- Dados em memória RAM
- Não persistem (container stop/restart/host reboot)
- Não escritos em disco
- Use cases:
  - Cache de dados intermediários
  - Informações sensíveis (credenciais)
  - Reduzir disk I/O

## Comparação Visual

```
┌─────────────────────────────────────────────────────────────┐
│                     DOCKER STORAGE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐                                        │
│  │   Volume Mount  │ → Gerenciado pelo Docker              │
│  │   /var/lib/     │   Persiste após container removal     │
│  │   docker/volumes│   Ideal para produção                 │
│  └─────────────────┘                                        │
│                                                             │
│  ┌─────────────────┐                                        │
│  │   Bind Mount    │ → Link direto host ↔ container        │
│  │   /host/path    │   Acessível de ambos lados            │
│  │                 │   Ideal para desenvolvimento          │
│  └─────────────────┘                                        │
│                                                             │
│  ┌─────────────────┐                                        │
│  │   tmpfs Mount   │ → Memória RAM apenas                  │
│  │   (memory only) │   Não persiste, não vai ao disco      │
│  │                 │   Ideal para dados sensíveis/cache    │
│  └─────────────────┘                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Boas Práticas

1. **Volumes para produção** - Gerenciados, isolados, persistentes
2. **Bind mounts para desenvolvimento** - Hot reload, config files
3. **tmpfs para dados sensíveis** - Credenciais, tokens em memória
4. **Evitar writable layer** - Performance e persistência

## Próximos Passos
- [ ] Estudar volumes em detalhes
- [ ] Estudar storage drivers (overlay2, etc.)
- [ ] Entender containerd image store