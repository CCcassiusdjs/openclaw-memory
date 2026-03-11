# docker stack - Docker CLI Reference

**URL:** https://docs.docker.com/reference/cli/docker/stack/
**Lido em:** 2026-03-11
**Categoria:** Orchestration
**Prioridade:** Média

---

## Resumo

Referência do comando `docker stack` para gerenciar stacks Swarm.

---

## Descrição

Gerencia stacks no Docker Swarm.

**Nota:** Apenas Swarm, não funciona com standalone containers.

---

## Subcomandos

| Comando | Descrição |
|---------|-----------|
| `docker stack config` | Output do config file final (merge + interpolation) |
| `docker stack deploy` | Deploy de novo stack ou update existente |
| `docker stack ls` | Listar stacks |
| `docker stack ps` | Listar tasks do stack |
| `docker stack rm` | Remover um ou mais stacks |
| `docker stack services` | Listar serviços do stack |

---

## docker stack deploy

### Uso:

```bash
docker stack deploy [OPTIONS] STACK
```

### Opções:

| Flag | Descrição |
|------|-----------|
| `-c, --compose-file` | Arquivo Compose (pode ser múltiplos) |
| `--prune` | Remover serviços não definidos |
| `--resolve-image` | Resolver image digests (always/changed/never) |
| `--with-registry-auth` | Enviar registry auth |

### Exemplos:

```bash
# Deploy básico
docker stack deploy -c docker-compose.yml mystack

# Múltiplos compose files
docker stack deploy -c base.yml -c override.yml mystack

# Com registry auth
docker stack deploy --with-registry-auth -c compose.yml mystack

# Com prune
docker stack deploy --prune -c compose.yml mystack
```

---

## docker stack ls

```bash
docker stack ls
```

Output:
```
NAME        SERVICES   ORCHESTRATOR
mystack     3          Swarm
webapp      2          Swarm
```

---

## docker stack ps

```bash
# Listar tasks
docker stack ps mystack

# Com filtros
docker stack ps --filter "desired-state=running" mystack
```

---

## docker stack services

```bash
# Listar serviços
docker stack services mystack

# Com filtros
docker stack services --filter "mode=replicated" mystack
```

---

## docker stack rm

```bash
# Remover stack
docker stack rm mystack
```

---

## docker stack config

```bash
# Ver config final (merge + interpolation)
docker stack config -c docker-compose.yml mystack
```

Útil para debug de configuração final.

---

## Stacks vs Services

| Aspecto | Service | Stack |
|---------|---------|-------|
| **Definição** | CLI flags | Compose file |
| **Escopo** | Um serviço | Múltiplos serviços |
| **Configuração** | Imperativo | Declarativo |
| **Versionamento** | Manual | Compose file |

---

## Key Takeaways

1. **Stack:** Conjunto de serviços definidos em Compose file
2. **deploy:** Cria ou atualiza stack
3. **--prune:** Remove serviços não definidos
4. **config:** Útil para debug
5. **Swarm only:** Não funciona sem Swarm