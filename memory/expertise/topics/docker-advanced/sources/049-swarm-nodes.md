# How Swarm Nodes Work - Documentação Oficial

**Fonte:** https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Visão Geral

Swarm mode cria um cluster de Docker Engines chamado **swarm**. O swarm consiste em nodes (máquinas físicas ou virtuais rodando Docker Engine).

---

## Tipos de Nodes

### Manager Nodes

Responsáveis por:
- Manter estado do cluster
- Agendar serviços
- Servir HTTP API endpoints

### Worker Nodes

Responsáveis por:
- Executar containers
- Não participam do Raft
- Não tomam decisões de scheduling

---

## Diagrama

```
┌─────────────────────────────────────────────────────┐
│                    Swarm Cluster                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Manager  │  │ Manager  │  │ Manager  │           │
│  │  (Raft)  │  │  (Raft)  │  │  (Raft)  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
│       │             │             │                  │
│       └─────────────┼─────────────┘                  │
│                     │                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Worker   │  │ Worker   │  │ Worker   │           │
│  │(Containers)│ │(Containers)│ │(Containers)│        │
│  └──────────┘  └──────────┘  └──────────┘           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## Raft Consensus

### O que é
Managers usam **Raft** para manter estado consistente do swarm.

### Fault Tolerance

| Managers | Tolerância |
|----------|------------|
| 1 | 0 (não recomendado para produção) |
| 3 | 1 manager pode falhar |
| 5 | 2 managers podem falhar |
| 7 | 3 managers podem falhar |

### Fórmula
- N managers toleram `(N-1)/2` falhas
- **Recomendado**: Ímpar de managers
- **Máximo recomendado**: 7 managers

### Importante
> Mais managers ≠ mais escalabilidade. Geralmente o oposto é verdade.

---

## Single-Manager Swarm

- Funciona para testes
- Se o manager falha:
  - Services continuam rodando
  - Precisa criar novo cluster para recuperar

---

## Worker Nodes

### Características
- Executam containers
- Não participam do Raft
- Não tomam decisões de scheduling
- Não servem HTTP API swarm

### Disponibilidade

| Estado | Descrição |
|--------|-----------|
| `Active` | Aceita tasks |
| `Pause` | Não aceita novas tasks, mantém existentes |
| `Drain` | Para tasks e move para outros nodes |

### Prevenir Scheduling em Managers
```bash
docker node update --availability drain <manager-node>
```
- Scheduler não coloca tasks em nodes com `Drain`
- Útil para managers dedicados

---

## Mudança de Roles

### Promover Worker para Manager
```bash
docker node promote <worker-node>
```
- Útil para manutenção de managers
- Adiciona ao Raft

### Rebaixar Manager para Worker
```bash
docker node demote <manager-node>
```
- Útil para manutenção
- Remove do Raft

---

## Alta Disponibilidade

### Recomendações
1. **Ímpar de managers** - 3, 5 ou 7
2. **Sempre 3+ managers** - Para tolerância a falhas
3. **Managers dedicados** - Worker availability = Drain
4. **Backup regular** - Exportar swarm tokens

### Exemplo de Cluster
```
Managers (3): manager1, manager2, manager3
Workers (N): worker1, worker2, worker3, ...
```

---

## Conceitos Aprendidos

1. **Raft consensus** - Managers mantêm estado consistente
2. **Fault tolerance** - (N-1)/2 managers podem falhar
3. **Manager == Worker** - Por default, managers também executam containers
4. **Drain availability** - Prevenir scheduling em managers
5. **Role changes** - Promote/demote nodes

---

## Aplicações Práticas

1. **High availability** - 3+ managers
2. **Dedicated managers** - Managers sem containers
3. **Maintenance** - Demote managers temporariamente
4. **Scaling** - Adicionar workers conforme necessário
5. **Disaster recovery** - Tokens de swarm

---

## Referências Cruzadas

- Ver: `048-docker-service-commands.md`
- Ver: `047-docker-network-create.md`
- Relacionado: Swarm services, PKI, scheduling