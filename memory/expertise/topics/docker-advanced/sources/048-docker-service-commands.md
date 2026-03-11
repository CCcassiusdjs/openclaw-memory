# Docker Service Commands - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/service/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Uso

```bash
docker service [COMMAND]
```

---

## Orquestrador

**Swarm** - Este comando gerencia serviços em Swarm mode.

---

## Pré-requisitos

- Deve ser executado em um **swarm manager node**
- Requer Swarm mode habilitado

---

## Subcomandos

| Comando | Descrição |
|---------|-----------|
| `docker service create` | Criar novo serviço |
| `docker service inspect` | Exibir informações detalhadas |
| `docker service logs` | Buscar logs do serviço |
| `docker service ls` | Listar serviços |
| `docker service ps` | Listar tasks de serviços |
| `docker service rm` | Remover serviços |
| `docker service rollback` | Reverter mudanças na configuração |
| `docker service scale` | Escalar serviços replicados |
| `docker service update` | Atualizar serviço |

---

## Fluxo Comum

1. **Criar serviço**: `docker service create --name web nginx`
2. **Listar serviços**: `docker service ls`
3. **Escalar**: `docker service scale web=5`
4. **Ver tasks**: `docker service ps web`
5. **Ver logs**: `docker service logs web`
6. **Atualizar**: `docker service update --image nginx:alpine web`
7. **Remover**: `docker service rm web`

---

## Diferenças vs docker run

| Aspecto | docker run | docker service |
|---------|-----------|----------------|
| Orquestração | Standalone | Swarm |
| Escalabilidade | Manual | Automática |
| Load balancing | Manual | Routing mesh |
| Atualização | Container único | Rolling update |
| Logs | Container único | Agregado |

---

## Conceitos Aprendidos

1. **Swarm services** - Gerenciamento declarativo de containers
2. **Manager node required** - Comandos só em managers
3. **Rolling updates** - Atualização gradual
4. **Scaling** - Escalar replicas facilmente
5. **Rollback** - Reverter mudanças

---

## Aplicações Práticas

1. **Microserviços** - Orquestração de serviços
2. **High availability** - Replicas em múltiplos nodes
3. **Load balancing** - Routing mesh automático
4. **Rolling deployment** - Atualização sem downtime
5. **Scaling** - Escalar sob demanda

---

## Referências Cruzadas

- Ver: `049-swarm-nodes.md`
- Ver: `001-docker-networking-overview.md`
- Relacionado: Swarm mode, services, tasks