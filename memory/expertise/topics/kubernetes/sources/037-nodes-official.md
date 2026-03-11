# Kubernetes Nodes (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/architecture/nodes/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Nodes são máquinas (virtuais ou físicas) que rodam workloads Kubernetes, gerenciadas pelo control plane e contendo os serviços necessários para executar Pods.

---

## O que é um Node?

### Definição
- Máquina virtual ou física no cluster
- Gerenciada pelo control plane
- Contém serviços para rodar Pods
- Tipicamente múltiplos nodes por cluster

### Componentes do Node
- **kubelet**: Agente que gerencia Pods
- **container runtime**: Roda containers
- **kube-proxy**: Proxy de rede

---

## Gerenciamento de Nodes

### Self-Registration (Padrão)
```bash
kubelet --register-node=true
```

**Flags:**
- `--kubeconfig`: Credenciais para API server
- `--cloud-provider`: Metadata do cloud provider
- `--register-node`: Auto-registro (default: true)
- `--register-with-taints`: Taints iniciais
- `--node-ip`: IPs do node
- `--node-labels`: Labels iniciais
- `--node-status-update-frequency`: Frequência de updates

### Manual Administration
```bash
# Criar Node manualmente
kubectl create -f node.yaml

# Cordorn (marcar como unschedulable)
kubectl cordon $NODENAME

# Uncordon
kubectl uncordon $NODENAME

# Drain (evacuar Pods)
kubectl drain $NODENAME
```

---

## Node Status

### Informações Disponíveis
1. **Addresses**: IPs e hostnames
2. **Conditions**: Status de saúde (Ready, MemoryPressure, etc.)
3. **Capacity and Allocatable**: Recursos disponíveis
4. **Info**: Versões, OS, kernel, etc.

### Ver Status
```bash
kubectl describe node <node-name>
kubectl get nodes -o wide
```

---

## Node Conditions

| Condição | Descrição |
|----------|-----------|
| **Ready** | Node está saudável e pode aceitar Pods |
| **MemoryPressure** | Memória baixa |
| **DiskPressure** | Disco baixo |
| **PIDPressure** | Muitos processos |
| **NetworkUnavailable** | Rede não configurada |

### Ready Condition Values
- **True**: Node saudável
- **False**: Node não saudável
- **Unknown**: Node controller não recebeu heartbeat

---

## Node Controller

### Responsabilidades
1. Sincronizar lista de nodes com cloud provider
2. Monitorar saúde dos nodes
3. Atualizar conditions quando node unreachable
4. Evict Pods de nodes unreachable

### Parâmetros
- `--node-monitor-period`: Intervalo de checks (default: 5s)
- `--node-eviction-rate`: Taxa de eviction (default: 0.1/s)
- `--unhealthy-zone-threshold`: Threshold para reduzir eviction

### Rate Limits
- Normal: 1 node a cada 10 segundos
- Zona unhealthy: Reduz para 0.01/s
- Cluster pequeno (<50 nodes): Pausa evictions

---

## Node Heartbeats

### Formas de Heartbeat
1. **Node status updates**: Atualiza .status periodicamente
2. **Lease objects**: Objeto no namespace kube-node-lease

### Lease Objects
- Mais eficiente que status updates
- Reduz carga no API server
- Um Lease por Node

---

## Node Capacity

### Recursos Rastreados
- CPU
- Memória
- Armazenamento
- Pods máximos

### Requests vs Capacity
```bash
# Ver capacity
kubectl describe node <name> | grep -A 5 Capacity

# Ver allocatable
kubectl describe node <name> | grep -A 5 Allocatable
```

### Allocatable
- Capacity menos system-reserved e kube-reserved
- Valor real disponível para Pods

---

## Node Topology

### TopologyManager
- Feature gate (v1.27+ stable)
- Otimiza colocação de recursos
- Hints para melhor performance

### Políticas
- **none**: Sem política
- **best-effort**: Tenta otimizar, não bloqueia
- **restricted**: Otimiza ou falha
- **single-numa-node**: NUMA único

---

## Taints e Tolerations

### Node Taints
```bash
# Adicionar taint
kubectl taint nodes node1 key=value:NoSchedule

# Remover taint
kubectl taint nodes node1 key:NoSchedule-
```

### Effects
- **NoSchedule**: Não agenda Pods sem toleration
- **PreferNoSchedule**: Evita (soft)
- **NoExecute**: Evict Pods existentes

### Node Problem Taints
- `node.kubernetes.io/not-ready`
- `node.kubernetes.io/unreachable`
- `node.kubernetes.io/memory-pressure`
- `node.kubernetes.io/disk-pressure`

---

## Best Practices

1. **Self-registration**: Usar auto-registro
2. **Labels**: Usar labels para scheduling
3. **Taints**: Isolar nodes especiais
4. **Monitoring**: Monitorar conditions
5. **Drain**: Sempre drain antes de manutenção

---

## Conceitos-Chave

1. **Node**: Máquina física ou virtual
2. **kubelet**: Agente no node
3. **Self-registration**: Registro automático
4. **Conditions**: Status de saúde
5. **Capacity/Allocatable**: Recursos disponíveis

---

## Próximos Passos de Estudo

- [ ] Node autoscaling
- [ ] Cluster autoscaler
- [ ] Node problem detector
- [ ] Graceful node shutdown

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/architecture/nodes/
- Node Status: https://kubernetes.io/docs/reference/node/node-status/
- Taints and Tolerations: https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/