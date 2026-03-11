# Kubernetes Scheduler (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

O kube-scheduler é o scheduler padrão do Kubernetes, responsável por encontrar o melhor Node para executar Pods não agendados, considerando requisitos de recursos, constraints e políticas.

---

## O que é Scheduling?

### Definição
Processo de matching Pods com Nodes para que o kubelet possa executá-los.

### Responsabilidade do Scheduler
- Observa Pods não agendados
- Encontra Nodes adequados
- Toma decisão de placement
- Notifica API server (binding)

---

## kube-scheduler

### Função
Componente do control plane que:
- Seleciona Node ótimo para novos Pods
- Considera requisitos individuais e coletivos
- Aplica affinity, anti-affinity, taints, tolerations

### Fatores de Decisão
- Resource requirements (CPU, memória)
- Hardware/software constraints
- Affinity/anti-affinity
- Data locality
- Inter-workload interference
- Taints and tolerations

---

## Processo de Scheduling

### 1. Filtering
Encontra Nodes onde é possível agendar o Pod:

| Filter | Descrição |
|--------|-----------|
| PodFitsResources | Recursos disponíveis |
| PodFitsHost | Node name match |
| PodFitsHostPorts | Portas disponíveis |
| PodMatchNodeSelector | Labels match |
| PodToleratesNodeTaints | Tolerations |
| CheckNodeCondition | Node Ready |

**Resultado:** Lista de feasible nodes

### 2. Scoring
Rankeia feasible nodes para escolher o melhor:

| Score | Fatores |
|-------|---------|
| LeastRequestedPriority | Menos recursos usados |
| BalancedResourceAllocation | Balanceamento CPU/memória |
| NodeAffinityPriority | Affinity match |
| InterPodAffinityPriority | Pod affinity |
| TaintTolerationPriority | Taints tolerados |
| ImageLocalityPriority | Imagens já presentes |

**Resultado:** Node com maior score

### 3. Binding
Notifica API server da decisão:
```yaml
apiVersion: v1
kind: Binding
metadata:
  name: my-pod
target:
  apiVersion: v1
  kind: Node
  name: node-1
```

---

## Configuração

### Scheduling Policies (Legacy)
Configura Predicates (filtering) e Priorities (scoring):
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: Policy
predicates:
- name: PodFitsResources
- name: PodMatchNodeSelector
priorities:
- name: LeastRequestedPriority
  weight: 1
```

### Scheduling Profiles (v1.18+)
Configura Plugins para diferentes estágios:

```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: default-scheduler
  plugins:
    queueSort:
      enabled:
      - name: PrioritySort
    filter:
      enabled:
      - name: NodeResourcesFit
      - name: NodeName
    score:
      enabled:
      - name: NodeResourcesBalancedAllocation
        weight: 1
    bind:
      enabled:
      - name: DefaultBinder
```

### Plugin Types
| Estágio | Plugins |
|---------|----------|
| QueueSort | Ordena Pods |
| PreFilter | Pré-processamento |
| Filter | Filtra Nodes |
| PreScore | Pré-scoring |
| Score | Rankeia Nodes |
| Bind | Atribui Pod ao Node |
| Reserve | Reserva recursos |
| Permit | Aprova binding |

---

## Múltiplos Schedulers

### Scheduler Customizado
```yaml
apiVersion: kubescheduler.config.k8s.io/v1
kind: KubeSchedulerConfiguration
profiles:
- schedulerName: my-scheduler
  plugins:
    score:
      enabled:
      - name: MyCustomPlugin
```

### Usar Scheduler Customizado
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  schedulerName: my-scheduler
  containers:
  - name: app
    image: myapp
```

---

## Scheduling Features

### Node Selection
```yaml
spec:
  nodeSelector:
    disktype: ssd
```

### Node Affinity
```yaml
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: disktype
            operator: In
            values:
            - ssd
```

### Pod Affinity/Anti-Affinity
```yaml
spec:
  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchLabels:
            app: myapp
        topologyKey: kubernetes.io/hostname
```

### Taints and Tolerations
```yaml
spec:
  tolerations:
  - key: "key"
    operator: "Equal"
    value: "value"
    effect: "NoSchedule"
```

---

## Topology Spread Constraints

```yaml
spec:
  topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: myapp
```

---

## Scheduler Performance Tuning

### Parâmetros
| Parâmetro | Descrição |
|-----------|-----------|
| `percentageOfNodesToScore` | % de nodes a considerar |
| `bindTimeoutSeconds` | Timeout para binding |
| `podMaxBackoffSeconds` | Max backoff para retry |

### Performance vs Accuracy
- `percentageOfNodesToScore < 100%`: Mais rápido, menos preciso
- Default: Calculado automaticamente

---

## Pod Overhead

```yaml
spec:
  overhead:
    podFixed:
      memory: "100Mi"
      cpu: "100m"
```

- Reserva recursos para o Pod (não containers)
- Útil para sandbox overhead

---

## Volume Scheduling

### Volume Binding Modes
- **Immediate**: Bind PV imediatamente
- **WaitForFirstConsumer**: Aguardar primeiro Pod

### Topology Support
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/gce-pd
volumeBindingMode: WaitForFirstConsumer
allowedTopologies:
- matchLabelExpressions:
  - key: failure-domain.beta.kubernetes.io/zone
    values:
    - us-central1-a
    - us-central1-b
```

---

## Conceitos-Chave

1. **Filtering**: Encontra feasible nodes
2. **Scoring**: Rankeia nodes
3. **Binding**: Atribui Pod ao Node
4. **Scheduling Profile**: Configura plugins
5. **Predicate/Priority**: Termos legados

---

## Best Practices

1. **Labels**: Usar labels consistentes para scheduling
2. **Affinity**: Usar para co-location e anti-affinity
3. **Taints**: Isolar nodes especiais
4. **Profiles**: Customizar para workloads específicos
5. **Monitoring**: Observar scheduling latency

---

## Próximos Passos de Estudo

- [ ] Custom Scheduler development
- [ ] Descheduling
- [ ] Preemption
- [ ] Pod Priority Classes

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/
- Scheduler Config: https://kubernetes.io/docs/reference/config-api/kube-scheduler-config.v1/
- Pod Priority: https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/