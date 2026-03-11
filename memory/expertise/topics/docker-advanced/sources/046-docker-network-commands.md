# Docker Network Commands - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/network/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Uso

```bash
docker network [COMMAND]
```

---

## Subcomandos

| Comando | Descrição |
|---------|-----------|
| `docker network connect` | Conectar container a uma rede |
| `docker network create` | Criar uma rede |
| `docker network disconnect` | Desconectar container de uma rede |
| `docker network inspect` | Exibir informações detalhadas |
| `docker network ls` | Listar redes |
| `docker network prune` | Remover redes não usadas |
| `docker network rm` | Remover uma ou mais redes |

---

## Tipos de Rede

| Tipo | Descrição |
|------|-----------|
| **bridge** | Default, rede local no host |
| **host** | Compartilha network namespace do host |
| **none** | Sem rede |
| **overlay** | Rede multi-host (Swarm) |
| **macvlan** | Acesso direto à rede física |

---

## Fluxo Comum

1. **Criar rede**: `docker network create mynet`
2. **Conectar container**: `docker run --network mynet myapp`
3. **Listar redes**: `docker network ls`
4. **Inspecionar**: `docker network inspect mynet`
5. **Limpar**: `docker network prune`

---

## Conceitos Aprendidos

1. **Network management** - Gerenciamento centralizado de redes
2. **Subcomandos** - Operações granulares por comando
3. **Tipos de rede** - bridge, host, none, overlay, macvlan

---

## Aplicações Práticas

1. **Isolamento** - Redes separadas para diferentes apps
2. **Microserviços** - Comunicação entre serviços
3. **Security** - Isolamento de rede
4. **Multi-host** - Overlay para Swarm

---

## Referências Cruzadas

- Ver: `047-docker-network-create.md`
- Ver: `001-docker-networking-overview.md`
- Relacionado: Docker Compose networks, Swarm networking