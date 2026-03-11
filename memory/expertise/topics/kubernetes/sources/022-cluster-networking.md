# Kubernetes Cluster Networking

**Source:** https://kubernetes.io/docs/concepts/cluster-administration/networking/
**Type:** Official Documentation
**Category:** Networking/CNI
**Read:** 2026-03-11

---

## Resumo

### 4 Problemas de Networking

| Problema | Solução |
|----------|---------|
| **Container-to-Container** | Pods e localhost |
| **Pod-to-Pod** | CNI plugins (este documento) |
| **Pod-to-Service** | Services |
| **External-to-Service** | Services (Ingress, NodePort, LoadBalancer) |

### Kubernetes Networking Model

O modelo de rede do Kubernetes exige:
1. **Todos os Pods podem se comunicar** com todos os outros Pods sem NAT
2. **Todos os Nodes podem se comunicar** com todos os Pods sem NAT
3. **O IP que um Pod vê** é o mesmo que os outros Pods veem

### IP Address Ranges

| Componente | Atribuição |
|------------|------------|
| **Network Plugin (CNI)** | IPs para Pods |
| **kube-apiserver** | IPs para Services (ClusterIP) |
| **kubelet/cloud-controller** | IPs para Nodes |

### Cluster Networking Types

| Tipo | Configuração |
|------|---------------|
| **IPv4 only** | Apenas IPv4 |
| **IPv6 only** | Apenas IPv6 |
| **Dual-stack** | IPv4 e IPv6 (ordem importa: IPv4/IPv6 ou IPv6/IPv4) |

---

## CNI (Container Network Interface)

### O que é CNI?
- Especificação para plugins de rede
- Gerencia network e security capabilities
- Implementado pelo container runtime em cada node

### Funções do CNI Plugin
1. Atribuir IPs aos Pods
2. Configurar rotas
3. Implementar políticas de rede
4. DNS para Pods

### CNI Plugins Populares

| Plugin | Características |
|--------|-----------------|
| **Calico** | Network Policy, BGP, escalável |
| **Cilium** | eBPF, observabilidade, security |
| **Flannel** | Simples, overlay network |
| **Weave Net** | Fácil de usar, multicast |
| **Canal** | Calico policies + Flannel networking |

---

## Network Model Requirements

```
┌─────────────────────────────────────────────────────────────┐
│                    KUBERNETES NETWORK MODEL                  │
│                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐                │
│  │  Pod A  │───▶│  Pod B  │───▶│  Pod C  │                │
│  │ 10.1.1.1│    │ 10.1.2.1│    │ 10.1.3.1│                │
│  └─────────┘    └─────────┘    └─────────┘                │
│       │              │              │                      │
│       └──────────────┴──────────────┘                      │
│                    │                                        │
│                    ▼                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            CNI Plugin (em cada Node)                  │  │
│  │  - IPAM (IP Allocation)                               │  │
│  │  - Routing                                            │  │
│  │  - Network Policies                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Regras Fundamentais
1. **Sem NAT** entre Pods na mesma cluster network
2. **IP consistente**: O IP que o Pod vê de si mesmo = IP que outros veem
3. **Portabilidade**: Não requer coordenação de portas entre containers

---

## Conceitos-Chave

1. **Flat Network**: Todos os Pods no mesmo IP space
2. **CNI abstrai complexidade**: Administrador configura, Pods usam
3. **Dual-stack**: Suporte a IPv4 e IPv6 simultaneamente
4. **IPAM**: IP Address Management pelo CNI
5. **Overlay vs Underlay**: Diferentes abordagens de implementação

---

## Próximos Passos
- Estudar Network Policies
- Ver CNI implementations específicos (Calico, Cilium)
- Entender kube-proxy vs CNI proxy