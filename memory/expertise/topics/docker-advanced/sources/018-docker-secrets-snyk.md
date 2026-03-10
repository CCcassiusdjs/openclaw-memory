# Keeping Docker Secrets Secure (Snyk)

**Fonte:** https://snyk.io/blog/keeping-docker-secrets-secure/
**Tipo:** Blog Post (Security)
**Lido em:** 2026-03-10
**Status:** completed

---

## Problemas com Secrets em Docker

### ❌ Más Práticas

| Prática | Problema |
|---------|----------|
| **Hard-code secrets** | Rebuild imagem quando mudar, exposto no código |
| **Arquivos locais** | Programas não-autorizados podem ler |
| **Environment variables** | Vulnerável via linked containers, docker inspect, child processes, logs |

### Por que Environment Variables são ruins

```bash
docker inspect [container_id]  # Mostra env vars
```

- Linked containers podem acessar
- Docker inspect revela
- Child processes herdam
- Logs podem conter valores

---

## Docker Swarm Secrets

### Como Funciona

```
┌──────────────────────────────────────────────┐
│              DOCKER SWARM                     │
├──────────────────────────────────────────────┤
│                                              │
│  ┌────────────┐    Raft     ┌────────────┐   │
│  │  Manager   │ ←─────────→ │  Manager   │   │
│  │   Node     │  Encrypted  │   Node     │   │
│  └────────────┘             └────────────┘   │
│        │                           │         │
│        │ Distribute secrets        │         │
│        ▼                           ▼         │
│  ┌────────────┐             ┌────────────┐   │
│  │  Worker    │             │  Worker    │   │
│  │  Node      │             │  Node      │   │
│  └────────────┘             └────────────┘   │
│        │                           │         │
│        ▼                           ▼         │
│  ┌────────────┐             ┌────────────┐   │
│  │ Container  │             │ Container  │   │
│  │ /run/secrets│            │ /run/secrets│  │
│  │ (tmpfs)    │             │ (tmpfs)    │   │
│  └────────────┘             └────────────┘   │
│                                              │
└──────────────────────────────────────────────┘
```

### Características

- **Encrypted in transit and at rest**
- **Raft consensus** para consistência
- **In-memory filesystem (tmpfs)** - não escreve em disco
- **Auto-cleanup** quando container para
- **Fine-grained access** - apenas serviços autorizados

---

## Comandos Docker Secrets

### Criar Secret

```bash
# De arquivo
echo "this-is-a-mysql-password" > password.txt
docker secret create mysql-password password.txt

# De stdin
printf "my_password" | docker secret create my_secret -

# Com nome específico
echo "password123" | docker secret create another-mysql-secret -
```

### Listar Secrets

```bash
docker secret ls
```

### Criar Serviço com Secret

```bash
docker service create \
  --name mysql-service \
  --secret another-mysql-secret \
  mysql:latest
```

### Adicionar/Remover Secret de Serviço

```bash
# Adicionar
docker service update --secret-add my_secret my_service

# Remover
docker service update --secret-rm my_secret my_service
```

### Localização no Container

```
/run/secrets/<secret_name>
```

Montado em tmpfs (memória).

---

## Alternativas Externas

Se já usa uma solução externa, continue usando:

| Solução | Tipo |
|---------|------|
| HashiCorp Vault | Open Source / Enterprise |
| CyberArk Conjour | Enterprise |
| Bitwarden | Open Source / Premium |
| AWS Secrets Manager | Cloud |
| GCP Secret Manager | Cloud |

**Recomendação:** Usar o que a organização já conhece.

---

## Best Practices

1. **Nunca hard-code secrets** em código ou Dockerfile
2. **Não usar env vars** para dados sensíveis
3. **Usar Docker Secrets** (Swarm) ou secret manager externo
4. **Rotation regular** de secrets
5. **Least privilege** - apenas serviços que precisam
6. **Monitor access** com logging

---

## Limitações

- **Apenas Swarm Services** - containers standalone não suportados
- **Tamanho máximo** não especificado (mas pequeno)
- **Não pode atualizar** - criar novo e migrar

---

## Comparação: Secrets vs Alternatives

| Método | Encrypted | In Memory | Rotation | Audit |
|--------|-----------|-----------|----------|-------|
| Docker Secrets | Sim | Sim | Manual | Parcial |
| Env Vars | Não | Depende | Manual | Não |
| Files | Depende | Não | Manual | Não |
| Vault | Sim | Sim | Automático | Sim |
| AWS Secrets | Sim | Sim | Automático | Sim |

## Próximos Passos
- [ ] Migrar env vars para secrets
- [ ] Implementar rotation policy
- [ ] Avaliar HashiCorp Vault