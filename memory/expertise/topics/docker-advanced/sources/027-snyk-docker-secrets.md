# Keeping Docker Secrets Secure (Snyk)

**Fonte:** https://snyk.io/blog/keeping-docker-secrets-secure/
**Data:** 2026-03-11
**Status:** Lido

---

## Resumo

Guia sobre gerenciamento de secrets em Docker Swarm, incluindo melhores práticas e alternativas para não-Kubernetes.

## O Problema dos Secrets

Sistemas containerizados precisam de:
- Chaves de usuário
- Senhas
- API keys
- Certificados

**Más Práticas:**
1. Hard-coding no source code
2. Abordagem "manual" (arquivos em disco local)
3. Environment variables (menos seguro que arquivos)

**Riscos de Environment Variables:**
- Expostas em containers linkados
- Visíveis em `docker inspect`
- Acessíveis por child processes
- Podem aparecer em logs

## Docker Secrets (Swarm)

### Arquitetura
```
┌─────────────────────────────────────────┐
│             Docker Swarm                 │
│  ┌─────────────────────────────────┐    │
│  │   Raft Consensus Algorithm      │    │
│  │   (Encrypted in transit/store)  │    │
│  └─────────────────────────────────┘    │
│                                         │
│  ┌─────────────┐    ┌─────────────┐    │
│  │ Manager     │    │ Manager     │    │
│  │ Nodes       │    │ Nodes       │    │
│  └──────┬──────┘    └──────┬──────┘    │
│         │                  │           │
│  ┌──────▼──────┐    ┌──────▼──────┐    │
│  │ Worker      │    │ Worker      │    │
│  │ Nodes       │    │ Nodes       │    │
│  │ Containers  │    │ Containers  │    │
│  └─────────────┘    └─────────────┘    │
└─────────────────────────────────────────┘
```

### Características
- **Encrypt at rest e in transit**
- Distribuído via Raft para todos manager nodes
- Acessível apenas a serviços autorizados
- Montado em in-memory filesystem (`/run/secrets/`)
- Flush automático da memória quando container para

### Comandos CLI

**Inicializar Swarm:**
```bash
docker swarm init
# Ou join: docker swarm join --token <token> <manager-ip>
```

**Criar Secret:**
```bash
# Método 1: De arquivo
echo "this-is-a-mysql-password" > password.txt
docker secret create my_mysql_password password.txt
# Output: l1m5jvgcox1l96i6bjbz4dvnt (secret ID)

# Método 2: De stdin
echo "another-mysql-password" | docker secret create another-mysql-secret -
```

**Listar Secrets:**
```bash
docker secret ls
```

**Criar Serviço com Secret:**
```bash
docker service create --name mysql-service \
  --secret another-mysql-secret \
  mysql:latest
```

**Adicionar/Remover Secret de Serviço Existente:**
```bash
# Remover
docker service update --secret-rm my_mysql_password mysql-service

# Adicionar
docker service update --secret-add my_mysql_password mysql-service
```

**Localização no Container:**
- Default: `/run/secrets/<secret-name>`
- TMPFS (in-memory)
- Disponível para todos containers do serviço

## Alternativas Externas

### Quando usar externos?
- Organização já tem expertise/investimento em plataforma específica
- Integração já existe com aplicações

### Opções Populares

| Solução | Tipo | Features |
|---------|------|----------|
| **HashiCorp Vault** | On-prem/Cloud | Enterprise, rotation, dynamic secrets |
| **CyberArk Conjur** | Enterprise | RBAC, audit, compliance |
| **Bitwarden** | SaaS/Self-hosted | Open source, easy setup |
| **AWS Secrets Manager** | Cloud | Auto-rotation, IAM integration |
| **GCP Secret Manager** | Cloud | KMS integration, versioning |
| **Azure Key Vault** | Cloud | HSM-backed, certificates |

## Comparação de Abordagens

| Método | Segurança | Complexidade | Use Case |
|--------|-----------|--------------|----------|
| Hard-coded | ❌ Péssima | Baixa | Nunca |
| Env vars | ⚠️ Baixa | Baixa | Dev apenas |
| Arquivos locais | ⚠️ Baixa | Baixa | Não recomendado |
| Docker Secrets | ✅ Alta | Média | Docker Swarm |
| Vault/Cloud | ✅ Alta | Alta | Enterprise |

## Conclusão

Docker Secrets + Docker Swarm = solução sólida para gerenciamento de secrets em ambientes não-Kubernetes:

1. **Não hard-code secrets** em imagens ou código
2. **Evite environment variables** para dados sensíveis
3. **Use secret managers** (Docker Swarm ou externos)
4. **In-memory filesystem** para montar secrets
5. **Auto-cleanup** quando container para

---
*Snyk oferece ferramentas para detectar secrets hard-coded em código, imagens e IaC*