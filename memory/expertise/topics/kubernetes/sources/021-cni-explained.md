# Kubernetes CNI Explained

**Fonte:** https://www.tigera.io/learn/guides/kubernetes-networking/kubernetes-cni/
**Tipo:** Networking Deep Dive
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

CNI (Container Network Interface) é o framework padrão para configurar rede em Kubernetes, permitindo que pods se comuniquem entre si e com serviços externos.

---

## O que é CNI?

### Definição
Container Network Interface (CNI) é um framework para configurar dinamicamente recursos de rede:
- Bibliotecas e especificações em Go
- Interface para configurar rede
- Provisionamento de IPs
- Conectividade multi-host

### Integração com Kubernetes
- Integrado com kubelet
- Configura rede entre pods automaticamente
- Overlay ou underlay networks
- Suporta OpenShift e outras plataformas

---

## Como Funciona

### Fluxo de Criação de Interface
1. Container runtime envia comando ADD ao CNI plugin
2. CNI plugin cria interface de rede no namespace do container
3. IPAM plugin aloca IP e rotas
4. Network configurada

### Comandos CNI
- **ADD**: Adicionar interface de rede
- **DEL**: Remover interface
- **CHECK**: Verificar configuração

### JSON Payload
Passa detalhes de configuração:
- Network type
- IPAM configuration
- DNS settings
- CNI version

---

## Modelos de Rede CNI

### 1. Encapsulated Networks (Overlay)

**Como funciona:**
- Encapsula Layer 2 sobre Layer 3 existente
- VXLAN ou IPsec para encapsulamento
- IP header adicional (overhead)
- Isola rede L2

**Exemplos:**
- VXLAN
- IPsec
- Flannel (VXLAN mode)
- Weave
- Canal

**Vantagens:**
- Fácil setup
- Não requer infraestrutura específica
- Works over any L3 network

**Desvantagens:**
- Overhead de encapsulamento
- Latência adicional
- MTU reduction

### 2. Unencapsulated Networks (Routed)

**Como funciona:**
- Layer 3 routing entre containers
- Sem overlay, sem overhead
- BGP para distribuição de rotas
- Routes dinamicamente atualizadas no OS

**Exemplos:**
- Calico (BGP)
- Romana

**Vantagens:**
- Sem overhead de encapsulamento
- Baixa latência
- Visibilidade total

**Desvantagens:**
- Requer BGP-capable network
- Mais complexo de setup
- Roteamento no kernel

---

## Principais CNI Plugins

### Calico
**Características:**
- L3 routing com BGP
- Network Policy enforcement
- Não-overlay ou overlay (VXLAN/IPIP)
- IPAM próprio
- Performance superior

**Componentes:**
- Calico CNI network plugin
- Calico CNI IPAM plugin
- BGP daemon (bird)
- Felix (policy enforcement)

### Flannel
**Características:**
- Overlay network (VXLAN)
- Simple setup
- Backend: etcd ou API server
- IPAM: host-local ou dhcp

### Weave Net
**Características:**
- Overlay network
- Automatic peer discovery
- DNS-based service discovery
- No external DB needed

### Cilium
**Características:**
- eBPF-based
- Layer 3-7 visibility
- Advanced network policies
- Kernel-level enforcement

### Canal
**Características:**
- Calico para policy
- Flannel para networking
- Best of both worlds

---

## Calico Deep Dive

### Arquitetura
```
Pod → veth pair → Host namespace → BGP routes → Other nodes
```

### Componentes

**CNI Plugin:**
- Cria veth pair
- Conecta pod ao host namespace
- Configura routing

**IPAM Plugin:**
- Aloca IPs para pods
- Dynamic IP blocks per node
- Efficient IP utilization

**Felix:**
- Policy enforcement
- iptables rules
- Route programming

**BGP Daemon:**
- Distributes routes
- Peers with other nodes/routers
- Converges network state

### Network Modes

**Non-Overlay:**
- Pure L3 routing
- BGP peering
- Best performance

**Overlay (VXLAN/IPIP):**
- Works over any network
- No BGP required
- Slight overhead

---

## Network Policy Enforcement

### Kubernetes Network Policy
**Features:**
- PodSelector (target pods)
- Ingress rules
- Egress rules
- Namespace-based

**Limitations:**
- Only ingress/egress
- No L7 rules
- No deny rules

### Calico Network Policy (Extended)
**Features adicionais:**
- Deny rules
- L7 rules (HTTP)
- Order/priority
- Global policies
- Namespace isolation

**Example:**
```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-frontend
spec:
  selector: app == 'frontend'
  ingress:
  - action: Allow
    protocol: TCP
    destination:
      ports:
      - 80
    source:
      selector: app == 'backend'
```

---

## Escolhendo um CNI

### Critérios
1. **Performance**: Latência, throughput
2. **Features**: Network policies, encryption
3. **Complexity**: Setup, maintenance
4. **Integration**: Cloud provider, legacy network
5. **Scale**: Number of nodes/pods

### Recomendações

| Cenário | CNI Recomendado |
|---------|----------------|
| Alta performance | Calico (BGP) |
| Simple setup | Flannel, Weave |
| Advanced policies | Calico, Cilium |
| Cloud native | AWS VPC CNI, Azure CNI |
| Security focus | Cilium, Calico |

---

## Troubleshooting CNI

### Problemas Comuns

**Pod não obtém IP:**
- Verificar CNI config
- Checar IPAM allocation
- Logs do kubelet

**Pod não comunica:**
- Network Policies bloqueando
- Iptables rules
- BGP peering issues

**Performance baixa:**
- MTU configuration
- Overlay overhead
- CPU limits (Felix)

### Debug Commands
```bash
# CNI config location
ls /etc/cni/net.d/

# Calico pods
kubectl get pods -n kube-system -l k8s-app=calico-node

# IP allocation
calicoctl ipam show

# Network policies
calicoctl get networkpolicy -A
```

---

## Conceitos-Chave

1. **CNI**: Interface padrão para networking de containers
2. **Overlay**: Encapsula rede virtual sobre física
3. **Underlay/Routed**: Usa rede física diretamente
4. **IPAM**: IP Address Management
5. **Network Policy**: Firewall entre pods

---

## Próximos Passos de Estudo

- [ ] Cilium eBPF deep dive
- [ ] Calico BGP configuration
- [ ] Network Policy patterns
- [ ] Service mesh (Istio) integration
- [ ] Multi-cluster networking

---

## Referências

- Tigera CNI Guide: https://www.tigera.io/learn/guides/kubernetes-networking/kubernetes-cni/
- CNI Spec: https://github.com/containernetworking/cni
- Calico Docs: https://docs.projectcalico.org/
- Kubernetes Networking: https://kubernetes.io/docs/concepts/services-networking/