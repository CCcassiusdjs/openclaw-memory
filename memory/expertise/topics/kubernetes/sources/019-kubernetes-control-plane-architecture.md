# Kubernetes Control Plane: Ultimate Guide

**Fonte:** https://www.plural.sh/blog/kubernetes-control-plane-architecture/
**Tipo:** Architecture Deep Dive
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

O control plane é o "cérebro" do cluster Kubernetes, responsável por gerenciar e orquestrar todos os recursos. Este guia cobre arquitetura, componentes, segurança e alta disponibilidade.

---

## Componentes do Control Plane

### 1. API Server (kube-apiserver)
**Função:** "Porta de entrada" do cluster
- Ponto central de comunicação
- Valida e autoriza todas as requisições
- Expõe a Kubernetes API
- Interface para kubectl, CI/CD, e outros componentes

**Características:**
- Stateless (estado em etcd)
- Alta disponibilidade via múltiplas réplicas
- Load balancer na frente
- Autenticação + autorização + admission control

**Porta:** 6443 (HTTPS)

### 2. etcd
**Função:** Banco de dados do cluster
- Key-value store distribuído
- Armazena TODO o estado do cluster
- Configurações, secrets, state de workloads
- Strong consistency (Raft consensus)

**Características:**
- Crítico para funcionamento
- Requer backup regular
- Performance impacta cluster inteiro
- Requer TLS + autenticação

**Porta:** 2379-2380

### 3. Scheduler (kube-scheduler)
**Função:** "Matchmaker" de workloads
- Decide onde Pods rodam
- Considera recursos, constraints, policies
- Avalia affinity/anti-affinity
- Taints e tolerations

**Características:**
- Watch por Pods não agendados
- Algoritmo de scoring de nodes
- Configurável via scheduling policies
- Extensível via schedulers customizados

**Porta:** 10259

### 4. Controller Manager (kube-controller-manager)
**Função:** Mantém estado desejado
- Controladores que reconciliam estado
- Exemplos: Node Controller, Replication Controller, Endpoints Controller
- Loop contínuo de monitoramento

**Características:**
- Single binary com múltiplos controllers
- Self-healing do cluster
- Leader election para HA
- Configurável via flags

**Porta:** 10257

### 5. Cloud Controller Manager (opcional)
**Função:** Integração com cloud provider
- Gerencia recursos cloud-specific
- Load balancers, storage volumes, network interfaces
- Separa lógica cloud da lógica core

**Exemplos de Controllers:**
- Node Controller (cloud)
- Route Controller
- Service Controller
- Cloud-specific controllers

---

## Worker Node Components

### kubelet
**Função:** Agente no node
- Comunica com API Server
- Gerencia lifecycle dos Pods
- Reporta status do node
- Executa container runtime

**Porta:** 10250

### kube-proxy
**Função:** Proxy de rede
- Implementa Services (VIP)
- Regras iptables/IPVS
- Load balancing interno
- Network routing

**Portas:** 10249 (metrics), 10256 (healthz)

### Container Runtime
**Função:** Roda containers
- containerd, CRI-O, Docker (via cri-dockerd)
- Implementa CRI (Container Runtime Interface)
- Pull images, create/start/stop containers

---

## Fluxo de Comunicação

```
User Request → API Server → Validation → etcd
                    ↓
            Controller Manager (watch)
                    ↓
            Scheduler (watch)
                    ↓
            kubelet (no node)
                    ↓
            Container Runtime
                    ↓
            Pod Running
```

---

## Alta Disponibilidade (HA)

### Multi-Master Setup
- Múltiplos API Servers (load balanced)
- etcd em cluster (3 ou 5 nodes)
- Leader election para controllers
- HAProxy/keepalived na frente

### Backup e Recovery
- Backup regular do etcd
- Configurações do control plane
- Certificados PKI
- Manifestos estáticos

---

## Segurança do Control Plane

### RBAC (Role-Based Access Control)
- Princípio do menor privilégio
- Roles + RoleBindings
- ClusterRoles vs Namespaced Roles
- ServiceAccount permissions

### Network Policies
- Segmentação de rede
- Firewall entre pods
- Ingress/Egress rules
- CNI plugin support

### Encryption
- TLS em todos os componentes
- Encryption at rest (etcd)
- mTLS entre componentes
- Certificate rotation

### Audit Logging
- API Server audit log
- Request/Response logging
- Policy violations detection
- Compliance requirements

---

## Monitoramento

### Métricas Críticas
- API Server latency
- etcd request latency
- Scheduler scheduling latency
- Controller manager queue depth
- kubelet node status

### Ferramentas
- Prometheus + Grafana
- Metrics Server
- Kubernetes Dashboard
- Third-party solutions (Datadog, New Relic)

---

## Conceitos-Chave

1. **Declarative State**: Estado desejado vs estado atual
2. **Reconciliation Loop**: Controladores reconciliam continuamente
3. **Watch Pattern**: Componentes "observam" mudanças no API server
4. **Eventual Consistency**: Sistema converge para estado desejado

---

## Troubleshooting Comum

| Problema | Causa | Solução |
|----------|-------|---------|
| API Server lento | Sobrecarga/rede | Scale out, otimize queries |
| etcd lento | Disco/redimensionamento | SSD, compact, defrag |
| Pods não agendam | Recursos insuficientes | Adicionar nodes, ajustar requests |
| Controllers falhando | RBAC/config | Verificar logs, permissions |

---

## Próximos Passos de Estudo

- [ ] Profundar em etcd (Raft, backup, performance)
- [ ] Scheduler customizado
- [ ] Admission Controllers avançados
- [ ] mTLS entre componentes
- [ ] Audit logging avançado

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/architecture/
- etcd Docs: https://etcd.io/docs/
- Plural Blog: https://www.plural.sh/blog/kubernetes-control-plane-architecture/