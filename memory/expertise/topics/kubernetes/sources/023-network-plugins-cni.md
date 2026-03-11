# Kubernetes Network Plugins (CNI)

**Source:** https://kubernetes.io/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/
**Type:** Official Documentation
**Category:** Networking/CNI
**Read:** 2026-03-11

---

## Resumo

### O que são Network Plugins?

CNI (Container Network Interface) plugins implementam o [Kubernetes network model](/docs/concepts/services-networking/#the-kubernetes-network-model):
- Comunicação Pod-to-Pod sem NAT
- Comunicação Node-to-Pod sem NAT
- IP consistente

### Requisitos

- Compatível com CNI spec **v0.4.0+** (mínimo)
- Recomendado: **v1.0.0** compatível
- Gerenciado pelo **Container Runtime** (não kubelet)

---

## Instalação

### Antes do Kubernetes 1.24
- kubelet gerenciava CNI via `cni-bin-dir` e `network-plugin`
- **REMOVIDO em v1.24**

### Kubernetes 1.24+
- Container Runtime gerencia CNI
- Documentação por runtime:
  - [containerd](https://github.com/containerd/containerd/blob/main/script/setup/install-cni)
  - [CRI-O](https://github.com/cri-o/cri-o/blob/main/contrib/cni/README.md)

---

## Requisitos de Plugin

### Loopback CNI

**Obrigatório:** Interface loopback `lo` para cada sandbox (Pod, VM)

**Opções:**
1. CNI loopback plugin oficial
2. Implementação própria (veja [CRI-O example](https://github.com/cri-o/ocicni/blob/release-1.24/pkg/ocicni/util_linux.go#L91))

### HostPort Support

**Plugin:** [portmap](https://github.com/containernetworking/plugins/tree/master/plugins/meta/portmap)

**Configuração:**
```json
{
  "name": "k8s-pod-network",
  "cniVersion": "0.4.0",
  "plugins": [
    {
      "type": "calico",
      "ipam": { "type": "host-local", "subnet": "usePodCidr" }
    },
    {
      "type": "portmap",
      "capabilities": { "portMappings": true },
      "externalSetMarkChain": "KUBE-MARK-MASQ"
    }
  ]
}
```

### Traffic Shaping (Experimental)

**Plugin:** [bandwidth](https://github.com/containernetworking/plugins/tree/master/plugins/meta/bandwidth)

**Configuração:**
```json
{
  "name": "k8s-pod-network",
  "cniVersion": "0.4.0",
  "plugins": [
    {
      "type": "calico",
      "ipam": { "type": "host-local", "subnet": "usePodCidr" }
    },
    {
      "type": "bandwidth",
      "capabilities": { "bandwidth": true }
    }
  ]
}
```

**Uso no Pod:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubernetes.io/ingress-bandwidth: 1M
    kubernetes.io/egress-bandwidth: 1M
```

---

## Arquitetura CNI

```
┌─────────────────────────────────────────────────────────────┐
│                    KUBERNETES NODE                           │
│                                                             │
│  ┌──────────────┐                                           │
│  │   kubelet    │                                           │
│  └──────┬───────┘                                           │
│         │ Pod creation request                               │
│         ▼                                                    │
│  ┌──────────────┐     ┌──────────────────────────────────┐ │
│  │ Container    │────▶│ CNI Plugin                        │ │
│  │ Runtime      │     │                                   │ │
│  │ (containerd) │     │ 1. Create network namespace       │ │
│  └──────────────┘     │ 2. Allocate IP (IPAM)            │ │
│                       │ 3. Configure interfaces           │ │
│                       │ 4. Set up routes                 │ │
│                       │ 5. Return result                  │ │
│                       └──────────────────────────────────┘ │
│                                 │                           │
│                                 ▼                           │
│                       ┌──────────────────────────────────┐ │
│                       │       /etc/cni/net.d/            │ │
│                       │       (CNI config files)         │ │
│                       └──────────────────────────────────┘ │
│                                 │                           │
│                                 ▼                           │
│                       ┌──────────────────────────────────┐ │
│                       │       /opt/cni/bin/              │ │
│                       │       (CNI plugin binaries)      │ │
│                       └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Plugins Populares

| Plugin | Características |
|--------|-----------------|
| **Calico** | Policy, BGP, VXLAN, IP-in-IP |
| **Cilium** | eBPF, observabilidade, security |
| **Flannel** | Simple overlay (VXLAN, UDP) |
| **Weave Net** | Simple, multicast |
| **Canal** | Calico policies + Flannel network |

---

## CNI Config Structure

```json
{
  "cniVersion": "1.0.0",
  "name": "my-network",
  "plugins": [
    {
      "type": "main-plugin",
      "ipam": {
        "type": "host-local",
        "subnet": "10.244.0.0/16"
      }
    },
    {
      "type": "portmap",
      "capabilities": { "portMappings": true }
    },
    {
      "type": "bandwidth",
      "capabilities": { "bandwidth": true }
    }
  ]
}
```

---

## Conceitos-Chave

1. **CNI v0.4.0+ Required**: Kubernetes 1.24+
2. **Container Runtime Manages**: Não mais kubelet
3. **Loopback Required**: Para cada sandbox
4. **HostPort via portmap**: Plugin adicional
5. **Traffic Shaping via bandwidth**: Experimental
6. **Chained Plugins**: Múltiplos plugins em sequência
7. **IPAM**: Address management separado

---

## Links

- [CNI Specification](https://github.com/containernetworking/cni)
- [CNI Plugins](https://github.com/containernetworking/plugins)
- [Troubleshooting CNI](/docs/tasks/administer-cluster/migrating-from-dockershim/troubleshooting-cni-plugin-related-errors/)
- [Cluster Networking](/docs/concepts/cluster-administration/networking/)
- [Network Policies](/docs/concepts/services-networking/network-policies/)