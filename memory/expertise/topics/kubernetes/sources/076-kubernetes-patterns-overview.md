# Kubernetes Patterns

**Source:** https://k8spatterns.com/
**Type:** Book Reference
**Category:** Patterns
**Read:** 2026-03-11

---

## Resumo

### Livro de Referência

**Título:** Kubernetes Patterns: Reusable Elements for Designing Cloud Native Applications

**Autores:** Bilgin Ibryam, Roland Huß

**Editora:** O'Reilly Media

**Links:**
- [O'Reilly](https://www.oreilly.com/library/view/kubernetes-patterns-2nd/9781098131678/)
- [Amazon](https://www.amazon.com/_/dp/1098131681?tag=oreilly20-20)
- [Examples (GitHub)](https://github.com/k8spatterns/examples)
- [PDF Download (Red Hat)](https://developers.redhat.com/e-books/kubernetes-patterns-2nd-edition)

---

## Categorias de Patterns

Baseado no livro e documentação complementar:

### Foundational Patterns
Patterns fundamentais para entender Kubernetes:

| Pattern | Descrição |
|---------|-----------|
| **Predictable Demands** | Declarar requisitos explicitamente |
| **Immutable Infrastructure** | Containers imutáveis |
| **Self-Healing** | Recuperação automática |
| **Health Probe** | Liveness/Readiness probes |

### Behavioral Patterns
Patterns que definem comportamento:

| Pattern | Descrição |
|---------|-----------|
| **Batch Job** | Execução única |
| **Periodic Job** | CronJob para execução periódica |
| **Daemon Service** | Um pod por node (DaemonSet) |
| **Singleton Service** | Apenas uma instância |
| **Stateful Service** | StatefulSet para estado |

### Structural Patterns
Patterns de estrutura:

| Pattern | Descrição |
|---------|-----------|
| **Init Container** | Containers de inicialização |
| **Sidecar** | Container auxiliar |
| **Adapter** | Adaptar interfaces |
| **Ambassador** | Proxy para serviços externos |

### Configuration Patterns
Patterns de configuração:

| Pattern | Descrição |
|---------|-----------|
| **EnvVar Configuration** | Config via environment |
| **ConfigMap** | Configuração externa |
| **Secret** | Dados sensíveis |
| **Immutable ConfigMap/Secret** | Config imutável |

### Lifecycle Patterns
Patterns de ciclo de vida:

| Pattern | Descrição |
|---------|-----------|
| **Pod Lifecycle** | Hooks de lifecycle |
| **Graceful Shutdown** | Terminação controlada |
| **Phase Handlers** | PreStop, PostStart |

### Observability Patterns
Patterns de observabilidade:

| Pattern | Descrição |
|---------|-----------|
| **Log Stream** | Logs como streams |
| **Event Record** | Kubernetes Events |
| **Metrics** | Prometheus metrics |
| **Tracing** | Distributed tracing |

### Scalability Patterns
Patterns de escalabilidade:

| Pattern | Descrição |
|---------|-----------|
| **Horizontal Pod Autoscaler** | Auto-scaling por métricas |
| **Vertical Pod Autoscaler** | Resize de recursos |
| **Cluster Autoscaler** | Adicionar nodes |

### Security Patterns
Patterns de segurança:

| Pattern | Descrição |
|---------|-----------|
| **Service Account** | Identity para pods |
| **Network Policy** | Firewall entre pods |
| **Pod Security Standard** | Restrições de segurança |

---

## Pattern Details (Resumo)

### Sidecar Pattern
```
┌─────────────────────────────────────┐
│              POD                     │
│  ┌──────────────┐ ┌──────────────┐  │
│  │   Main       │ │   Sidecar    │  │
│  │  Container   │ │  Container   │  │
│  │              │ │              │  │
│  │  Application │ │  Logging,    │  │
│  │  Logic       │ │  Proxy, etc  │  │
│  └──────────────┘ └──────────────┘  │
│         │                │           │
│         └────────┬───────┘           │
│                  ▼                   │
│           Shared Volume             │
└─────────────────────────────────────┘
```

### Init Container Pattern
```
┌─────────────────────────────────────┐
│              POD                     │
│                                     │
│  ┌──────────────┐                   │
│  │ Init Container│ ──▶ Complete    │
│  │ (setup, wait) │                 │
│  └──────────────┘                   │
│         ▼                           │
│  ┌──────────────┐                   │
│  │   Main       │                   │
│  │  Container   │                   │
│  └──────────────┘                   │
└─────────────────────────────────────┘
```

### Ambassador Pattern
```
┌─────────────────────────────────────┐
│              POD                     │
│  ┌──────────────┐ ┌──────────────┐  │
│  │   Main       │ │  Ambassador  │  │
│  │  Container   │ │  (Proxy)     │  │
│  └──────────────┘ └──────────────┘  │
│                           │         │
│                           ▼         │
│              External Service       │
└─────────────────────────────────────┘
```

---

## Conceitos-Chave

1. **Patterns são reutilizáveis**: Aplicar repetidamente
2. **Cloud Native**: Design para Kubernetes
3. **Declarative**: Especificar estado desejado
4. **Composable**: Combinar patterns
5. **Observable**: Design para observabilidade

---

## Recursos Adicionais

- Livro completo no GitHub examples
- Red Hat Developer ebook gratuito
- Blog posts com detalhes de cada pattern