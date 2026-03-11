# docker service rollback - Docker CLI Reference

**URL:** https://docs.docker.com/reference/cli/docker/service/rollback/
**Lido em:** 2026-03-11
**Categoria:** Orchestration
**Prioridade:** Média

---

## Resumo

Referência do comando `docker service rollback` para reverter serviços Swarm.

---

## Uso

```bash
docker service rollback [OPTIONS] SERVICE
```

Reverte um serviço para a versão anterior.

---

## Opções

| Flag | Descrição |
|------|-----------|
| `-d, --detach` | Exit imediatamente (não esperar converge) |
| `-q, --quiet` | Suprimir progress output |

---

## Comportamento

### O que é revertido:
- Configuração antes do último `docker service update`
- Inclui: image, replicas, ports, networks, etc.

### Não é rollback de dados:
- Volumes permanecem inalterados
- Secrets/configs não são revertidos

---

## Exemplos

### Rollback Simples:

```bash
# Criar serviço com 1 replica
docker service create --name my-service -p 8080:80 nginx:alpine

# Verificar
docker service ls
# REPLICAS: 1/1

# Atualizar para 3 replicas
docker service update --replicas=3 my-service

# Verificar
docker service ls
# REPLICAS: 3/3

# Rollback
docker service rollback my-service

# Verificar
docker service ls
# REPLICAS: 1/1
```

### Rollback com Detach:

```bash
# Não esperar converge
docker service rollback -d my-service
```

### Rollback Quiet:

```bash
# Sem output
docker service rollback -q my-service
```

---

## Fluxo de Rollback

```
Estado Inicial (1 replica)
        │
        ▼
docker service update --replicas=3
        │
        ▼
Estado Atualizado (3 replicas)
        │
        ▼
docker service rollback
        │
        ▼
Estado Anterior (1 replica)
```

---

## Comparação: Rollback vs Update --rollback

| Comando | Comportamento |
|---------|---------------|
| `docker service rollback` | Comando dedicado |
| `docker service update --rollback` | Flag no update |

Ambos fazem a mesma coisa. `rollback` é mais explícito.

---

## Auto-Rollback

### Configurar para rollback automático:

```bash
docker service create \
  --update-failure-action=rollback \
  --update-max-failure-ratio=0.3 \
  nginx:alpine
```

### Comportamento:
- Se 30% das tasks falharem no update
- Rollback automático é disparado

---

## Limitações

1. **Apenas um nível:** Rollback vai para o estado anterior imediato
2. **Não é histórico:** Não mantém múltiplas versões
3. **Dados persistem:** Volumes e secrets não são revertidos

---

## Key Takeaways

1. **Simples:** `docker service rollback SERVICE`
2. **Único nível:** Apenas versão anterior
3. **Detach:** Não esperar converge
4. **Auto-rollback:** Configurável com `--update-failure-action`
5. **Não afeta dados:** Volumes permanecem