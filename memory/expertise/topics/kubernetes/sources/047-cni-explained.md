# Kubernetes CNI Explained

**Source:** https://www.tigera.io/learn/guides/kubernetes-networking/kubernetes-cni/
**Type:** Guide
**Category:** Networking/CNI
**Read:** 2026-03-11

---

## Resumo

### O que é CNI?

**Container Network Interface (CNI)** = Framework para configurar rede de containers dinamicamente.

**Especificações:**
- Libraries + specifications escritas em Go
- Plugin specification para configuração de rede
- Provisioning de IP addresses
- Conectividade entre hosts

---

## Como Funciona

### Fluxo de Criação de Interface

```
┌─────────────────┐
│ Container        │
│ Runtime          │
│ (Docker/containerd)│
└────────┬────────┘
         │
         ▼ ADD command + JSON payload
┌─────────────────┐
│ CNI Plugin      │
│                 │
│ 1. Create iface │
│ 2. IPAM allocate│
│ 3. Configure    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Network         │
│ Namespace       │
│ (veth pair)     │
└─────────────────┘
```

### Comandos CNI

| Comando | Função |
|---------|--------|
| **ADD** | Adiciona container à rede |
| **DEL** | Remove container da rede |
| **CHECK** | Verifica estado da rede |

---

## Network Models

### Encapsulated Networks (Overlay)

```
┌─────────────────────────────────────────────────────────────┐
│              ENCAPSULATED NETWORK (VXLAN)                    │
│                                                             │
│  ┌───────────┐                    ┌───────────┐            │
│  │  Pod A    │                    │  Pod B    │            │
│  │ 10.1.1.1  │                    │ 10.1.2.1  │            │
│  └─────┬─────┘                    └─────┬─────┘            │
│        │                                │                   │
│        ▼                                ▼                   │
│  ┌───────────┐                    ┌───────────┐            │
│  │  veth    │                    │  veth     │            │
│  └─────┬─────┘                    └─────┬─────┘            │
│        │                                │                   │
│        ▼                                ▼                   │
│  ┌───────────────────────────────────────────────────┐      │
│  │         VXLAN Tunnel (UDP)                        │      │
│  │  ┌───────────────────────────────────────────┐   │      │
│  │  │ Original Packet + VXLAN Header            │   │      │
│  │  │ Encapsulated in UDP                        │   │      │
│  │  └───────────────────────────────────────────┘   │      │
│  └───────────────────────────────────────────────────┘      │
│        │                                │                   │
│        ▼                                ▼                   │
│  ┌───────────┐                    ┌───────────┐            │
│  │ Node 1    │ ─────────────────▶│ Node 2    │            │
│  │ (L3)      │    VXLAN over L3  │ (L3)      │            │
│  └───────────┘                    └───────────┘            │
└─────────────────────────────────────────────────────────────┘
```

**Características:**
- Isolamento L2 sobre L3
- Não precisa de routing distribution
- Overhead: IP header adicional
- Usa VXLAN, IPsec
- Sensível à latência

**Exemplos:** Canal, Flannel, Weave

### Unencapsulated Networks (Routed)

```
┌─────────────────────────────────────────────────────────────┐
│              UNENCAPSULATED NETWORK (BGP)                   │
│                                                             │
│  ┌───────────┐                    ┌───────────┐            │
│  │  Pod A    │                    │  Pod B    │            │
│  │ 10.1.1.1  │                    │ 10.1.2.1  │            │
│  └─────┬─────┘                    └─────┬─────┘            │
│        │                                │                   │
│        ▼                                ▼                   │
│  ┌───────────┐                    ┌───────────┐            │
│  │  veth    │                    │  veth     │            │
│  └─────┬─────┘                    └─────┬─────┘            │
│        │                                │                   │
│        ▼                                ▼                   │
│  ┌───────────────────────────────────────────────────┐      │
│  │         L3 Routing (BGP)                          │      │
│  │  Routes distributed to each node                 │      │
│  │  Node knows how to reach Pod B                   │      │
│  └───────────────────────────────────────────────────┘      │
│        │                                │                   │
│        ▼                                ▼                   │
│  ┌───────────┐                    ┌───────────┐            │
│  │ Node 1    │ ─────────────────▶│ Node 2    │            │
│  │ BGP routes│    Direct L3      │ BGP routes│            │
│  └───────────┘                    └───────────┘            │
└─────────────────────────────────────────────────────────────┘
```

**Características:**
- L3 routing direto
- Sem overhead de encapsulação
- Requer route distribution
- Usa BGP
- Menor latência

**Exemplos:** Romana, Calico

---

## Comparação

| Aspecto | Encapsulated | Unencapsulated |
|---------|-------------|----------------|
| Isolation | L2 isolated | L3 routing |
| Overhead | IP header extra | None |
| Route Distribution | Not needed | Required |
| Latency | Higher | Lower |
| Complexity | Simpler config | More complex |
| Use Case | Multi-datacenter | High performance |

---

## Calico CNI

### Arquitetura Modular

| Componente | Função |
|------------|--------|
| **Calico CNI Plugin** | Conecta pods via veth pair ao host namespace |
| **Calico IPAM Plugin** | Aloca IPs dinamicamente por node |
| **Overlay Modes** | VXLAN ou IP-in-IP |
| **Non-overlay Modes** | L2 network, L3 com BGP, ou cloud integration |
| **Network Policy** | Full Kubernetes + Calico extended policies |

### Integrações

- Amazon VPC CNI
- Azure CNI
- Google cloud provider
- Host local IPAM
- Flannel

---

## CNI Plugins Populares

| Plugin | Tipo | Características |
|--------|------|-----------------|
| **Calico** | Unencapsulated/Overlay | Network Policy, BGP, flexível |
| **Cilium** | eBPF | Observabilidade, security, high performance |
| **Flannel** | Overlay | Simples, VXLAN |
| **Weave Net** | Overlay | Fácil, multicast |
| **Canal** | Hybrid | Calico policies + Flannel networking |

---

## Conceitos-Chave

1. **CNI = Interface Standard**: Plugins conform to spec
2. **Overlay vs Underlay**: Escolha depende de requirements
3. **IPAM**: IP Address Management pelo plugin
4. **Calico = Enterprise-ready**: Modular, policy-enforcing
5. **VXLAN**: Encapsulation para L2 over L3
6. **BGP**: Routing protocol para unencapsulated

---

## Quando Usar Cada Modelo

### Encapsulated (Overlay)
- Multi-datacenter com L3 connectivity
- Simplicidade de configuração
- Latência não é crítica

### Unencapsulated (Routed)
- Alta performance necessária
- Latência baixa
- Controle de routing