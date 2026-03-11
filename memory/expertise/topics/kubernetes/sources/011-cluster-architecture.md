# Kubernetes Cluster Architecture

**Source:** https://kubernetes.io/docs/concepts/architecture/
**Type:** Official Documentation
**Category:** Fundamentos
**Read:** 2026-03-11

---

## Resumo

### Arquitetura Base
```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL PLANE                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ kube-apiserver│ │    etcd      │ │  kube-scheduler     │ │
│  └──────────────┘ └──────────────┘ └──────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┤
│  │ kube-controller-manager │ cloud-controller-manager     │ │
│  └──────────────────────────────────────────────────────────┤
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  Worker Node 1 │   │  Worker Node 2 │   │  Worker Node N │
│ ┌───────────┐  │   │ ┌───────────┐  │   │ ┌───────────┐  │
│ │  kubelet  │  │   │ │  kubelet  │  │   │ │  kubelet  │  │
│ ├───────────┤  │   │ ├───────────┤  │   │ ├───────────┤  │
│ │kube-proxy │  │   │ │kube-proxy │  │   │ │kube-proxy │  │
│ ├───────────┤  │   │ ├───────────┤  │   │ ├───────────┤  │
│ │ Container │  │   │ │ Container │  │   │ │ Container │  │
│ │  Runtime  │  │   │ │  Runtime  │  │   │ │  Runtime  │  │
│ └───────────┘  │   │ └───────────┘  │   │ └───────────┘  │
│    [Pods]      │   │    [Pods]      │   │    [Pods]      │
└───────────────┘   └───────────────┘   └───────────────┘
```

### Control Plane Components (Detalhado)

#### kube-apiserver
- Front end do control plane
- Expõe Kubernetes API
- Escala horizontalmente (múltiplas instâncias com load balancing)

#### etcd
- Backing store para TODOS os dados do cluster
- Key-value store consistente e altamente disponível
- **CRÍTICO**: Ter plano de backup

#### kube-scheduler
- Watch: Pods sem node assignado
- Decisões de scheduling baseadas em:
  - Resource requirements (CPU, memória)
  - Hardware/software/policy constraints
  - Affinity/anti-affinity
  - Data locality
  - Inter-workload interference
  - Deadlines

#### kube-controller-manager
Controllers embutidos:
- **Node controller**: Detecta nodes down
- **Job controller**: Cria Pods para Jobs
- **EndpointSlice controller**: Link Services ↔ Pods
- **ServiceAccount controller**: Default SAs para novos namespaces

#### cloud-controller-manager
Integração cloud-specific:
- Node controller: Detecta nodes deletados no cloud provider
- Route controller: Setup de rotas
- Service controller: Load balancers do cloud provider

### Node Components (Detalhado)

#### kubelet
- Agente em cada node
- Garante containers rodando nos Pods
- Usa PodSpecs de várias fontes
- **NÃO** gerencia containers não-Kubernetes

#### kube-proxy (opcional)
- Network proxy por node
- Implementa Services
- Usa iptables/IPVS ou forward próprio
- **Pode ser substituído** por CNI com proxy próprio

#### Container Runtime
- Executa containers
- Suporta: containerd, CRI-O, qualquer CRI implementation

### Addons

| Addon | Função |
|-------|--------|
| **DNS** | Obrigatório para maioria dos casos. Containers usam automaticamente. |
| **Dashboard** | UI web para gerenciamento |
| **Monitoring** | Métricas time-series (cAdvisor, Prometheus) |
| **Logging** | Logs centralizados |
| **Network plugins** | CNI: IPs para pods, comunicação entre pods |

### Architecture Variations

| Deployment | Descrição |
|------------|-----------|
| **Traditional** | Control plane em máquinas dedicadas, systemd services |
| **Static Pods** | Control plane como Pods estáticos (kubeadm usa isso) |
| **Self-hosted** | Control plane como Pods no próprio cluster |
| **Managed** | Cloud provider abstrai control plane (EKS, GKE, AKS) |

---

## Conceitos-Chave

1. **Separation of Concerns**: Control plane gerencia, nodes executam
2. **etcd é crítico**: Único ponto de verdade - backup obrigatório
3. **Scheduler é inteligente**: Considera múltiplos fatores além de recursos
4. **kube-proxy é opcional**: CNI pode substituir
5. **Addons são Resources**: Deployados como DaemonSets/Deployments

---

## Para Lembrar
- Control plane pode rodar em qualquer máquina
- Worker nodes precisam de pelo menos: kubelet + container runtime
- DNS é praticamente obrigatório
- Network plugins implementam CNI spec