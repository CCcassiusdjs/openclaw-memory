# Swarm Mode Key Concepts - Docker Docs

**URL:** https://docs.docker.com/engine/swarm/key-concepts/
**Lido em:** 2026-03-11
**Categoria:** Orchestration
**Prioridade:** Alta

---

## Resumo

Documentação oficial do Docker sobre conceitos fundamentais do Swarm mode.

---

## O que é um Swarm?

Swarm é um cluster de Docker hosts rodando em Swarm mode, usando **swarmkit** como orquestração layer.

### Componentes:
- **Managers:** Gerenciam membership e delegation
- **Workers:** Executam swarm services
- Um host pode ser manager, worker, ou ambos

---

## Nodes

### O que é um Node?
Instância do Docker Engine participando do swarm.

### Tipos de Nodes:

| Tipo | Função |
|------|--------|
| **Manager** | Orquestração, cluster management, dispatch tasks |
| **Worker** | Executa tasks designadas pelo manager |

### Comportamentos:
- Manager nodes selecionam um **leader** para orchestration
- Por default, managers também executam services
- Configurável: manager-only nodes
- Worker nodes reportam estado ao manager

---

## Services e Tasks

### Service
- Definição de tasks a executar nos nodes
- Estrutura central do swarm system
- Raiz da interação usuário-swarm

### Parâmetros do Service:
- Container image
- Commands a executar
- Número de replicas
- Networks e volumes
- Ports expostos

### Modelos de Service:

| Modelo | Descrição |
|--------|-----------|
| **Replicated** | N específico de replicas distribuídos |
| **Global** | 1 task por node no cluster |

### Task
- Unidade atômica de scheduling
- Container + commands
- Assinada a um node específico
- Não pode mover para outro node
- Pode apenas rodar no node ou falhar

### Fluxo:
```
User → Service Definition → Manager → Tasks → Worker Nodes
```

---

## Load Balancing

### Ingress Load Balancing
- Swarm manager expõe services externamente
- Porta pode ser auto-assinada (30000-32767) ou especificada
- Todos os nodes roteiam para running task

### Internal Load Balancing
- DNS component automático para cada service
- Requests distribuídos por DNS name

### Comportamento:
```
External Request
       │
       ▼
┌──────────────────┐
│  Published Port  │ ← Any node in cluster
│  (30000-32767)   │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│   Routing Mesh   │ ← All nodes route to tasks
└──────────────────┘
       │
       ▼
┌──────────────────┐
│  Running Task    │
└──────────────────┘
```

---

## Diferenças: Standalone vs Swarm Services

| Aspecto | Standalone Container | Swarm Service |
|---------|---------------------|---------------|
| Management | Qualquer daemon | Só manager |
| Updates | Manual restart | Automático |
| Scaling | Manual | Declarativo |
| Failover | Não | Sim |
| Config changes | Requer restart | Auto-update |

---

## Desired State

### Conceito:
- Swarm mantém o estado desejado declarado
- Se worker fica unavailable → reschedule tasks
- Se config muda → stop old tasks → create new tasks

### Exemplo:
```yaml
# docker-compose.yml para swarm
services:
  web:
    image: nginx
    deploy:
      replicas: 3
    ports:
      - "80:80"
```

---

## Arquitetura Swarm

```
┌─────────────────────────────────────────────────────┐
│                   Swarm Cluster                     │
│                                                     │
│  ┌─────────────────┐    ┌─────────────────┐       │
│  │  Manager Node   │    │  Manager Node   │       │
│  │  (Leader)       │    │  (Follower)     │       │
│  └─────────────────┘    └─────────────────┘       │
│         │                      │                    │
│         │    dispatch tasks    │                    │
│         ▼                      ▼                    │
│  ┌─────────────────┐    ┌─────────────────┐       │
│  │  Worker Node     │    │  Worker Node    │       │
│  │  (Task A, B)     │    │  (Task C)       │       │
│  └─────────────────┘    └─────────────────┘       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **Swarmkit:** Orquestração layer embutida no Docker Engine
2. **Services:** Abstração principal, declarativa
3. **Tasks:** Unidade atômica, não móvel
4. **Load Balancing:** Ingress + Internal DNS
5. **Desired State:** Swarm mantém automaticamente