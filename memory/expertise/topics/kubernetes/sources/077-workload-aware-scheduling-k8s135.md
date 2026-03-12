# Kubernetes v1.35: Workload Aware Scheduling

**Fonte:** Kubernetes Blog - https://kubernetes.io/blog/2025/12/29/kubernetes-v1-35-introducing-workload-aware-scheduling/
**Data:** Dezembro 2025
**Tópico:** Workload API, Gang Scheduling, Opportunistic Batching
**Status:** Lido

---

## Resumo Executivo

Kubernetes v1.35 introduz o Workload API e melhorias de scheduling para workloads de larga escala, incluindo gang scheduling nativo e opportunistic batching para pods idênticos.

---

## Conceitos-Chave

### O Problema do Scheduling Tradicional

- **Pods individuais**: Scheduler tradicional considera cada pod isoladamente
- **Workloads grandes**: ML batch jobs precisam de todos os pods juntos
- **Eficiência**: Colocação inteligente (same rack, NUMA affinity)
- **Fragilidade**: Scheduling parcial causa deadlocks e desperdício

---

## Workload API

### Definição
- **API group**: `scheduling.k8s.io/v1alpha1`
- **Função**: Descrever scheduling requirements de multi-Pod applications
- **Separação**: Jobs definem *what to run*, Workload define *how to schedule*

### Estrutura
```yaml
apiVersion: scheduling.k8s.io/v1alpha1
kind: Workload
metadata:
  name: training-job-workload
  namespace: some-ns
spec:
  podGroups:
  - name: workers
    policy:
      gang:
        # minCount = pods mínimos para iniciar
        minCount: 4
```

### Linking Pods to Workload
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: worker-0
  namespace: some-ns
spec:
  workloadRef:
    name: training-job-workload
    podGroup: workers
  # ... pod spec
```

---

## Gang Scheduling

### Como Funciona

1. **Criação de Pods**: Pods são criados (ou por controller)
2. **Bloqueio**: Scheduler bloqueia scheduling até:
   - Workload object existir
   - PodGroup existir no Workload
   - Número de pending Pods ≥ minCount
3. **Permit Gate**: Pods esperam no Permit gate
4. **Verificação**: Scheduler verifica se todos pods têm placement válido
5. **Binding**: Se há recursos para todos, bind de uma vez
6. **Rejeição**: Se timeout (5 min), todos rejeitados, voltam para queue

### Benefícios
- **All-or-nothing**: Evita scheduling parcial
- **Sem deadlocks**: Recursos não ficam presos
- **Eficiência**: Libera recursos se não consegue schedulear todos

### Casos de Uso
- **ML training jobs**: Distributed training
- **Batch processing**: Todos workers precisam rodar juntos
- **MPI jobs**: Message Passing Interface

---

## Opportunistic Batching

### Definição
- **Feature**: Beta em v1.35 (habilitado por padrão)
- **Função**: Acelera scheduling de pods idênticos
- **Semântica**: Transparente ao usuário

### Como Funciona
1. Scheduler processa primeiro pod
2. Identifica pods subsequentes com requirements idênticos
3. Reutiliza cálculos de feasibility
4. Significativamente mais rápido que processar cada pod

### Restrições
- Todos os campos de scheduling devem ser idênticos
- Alguns features desabilitam batching para corretude
- Verificar configuração do kube-scheduler

---

## North Star Vision

### Roadmap Futuro
1. **Workload scheduling phase**: Fase dedicada para workloads
2. **Multi-node DRA**: Dynamic Resource Allocation multi-node
3. **Topology aware scheduling**: Otimização de topologia
4. **Workload-level preemption**: Preempção coordenada
5. **Autoscaling integration**: Melhor integração
6. **External scheduler interaction**: APIs para schedulers externos
7. **Lifecycle management**: Gerenciamento completo do ciclo de vida
8. **Multi-workload simulations**: Simulações de placement

---

## Feature Gates

### Habilitação
```bash
# Workload API
--feature-gates=GenericWorkload=true

# Gang Scheduling
--feature-gates=GangScheduling=true

# Opportunistic Batching (Beta, habilitado por padrão)
--feature-gates=OpportunisticBatching=true
```

### Requisitos
- GenericWorkload em kube-apiserver E kube-scheduler
- GangScheduling requer Workload API habilitado
- OpportunisticBatching é Beta (default on)

---

## Arquitetura

```
┌─────────────────────────────────────────────────┐
│            Workload Controller                   │
│  (Creates Pods with workloadRef)                │
├─────────────────────────────────────────────────┤
│            Workload API                          │
│  scheduling.k8s.io/v1alpha1                    │
│  - PodGroups                                     │
│  - Gang Policies                                 │
├─────────────────────────────────────────────────┤
│            kube-scheduler                        │
│  ┌───────────────┐ ┌───────────────┐           │
│  │ GangScheduling│ │ Opportunistic │           │
│  │ Plugin        │ │ Batching      │           │
│  └───────────────┘ └───────────────┘           │
│  ┌───────────────┐ ┌───────────────┐           │
│  │ Permit Gate   │ │ Queue         │           │
│  └───────────────┘ └───────────────┘           │
├─────────────────────────────────────────────────┤
│            Nodes                                 │
│  (Binding happens all at once)                   │
└─────────────────────────────────────────────────┘
```

---

## Insights para Kubernetes

1. **Workload como cidadão de primeira classe**: API dedicada para grupos de pods
2. **Gang scheduling nativo**: Sem dependência de schedulers externos (Volcano, Kueue)
3. **Performance via batching**: Pods idênticos são processados em lote
4. **Roadmap claro**: Múltiplas melhorias planejadas
5. **Beta features habilitadas**: Opportunistic batching on por padrão

---

## Palavras-Chave
`workload-api` `gang-scheduling` `opportunistic-batching` `kubernetes-v135` `scheduling` `batch-jobs` `ml-workloads`