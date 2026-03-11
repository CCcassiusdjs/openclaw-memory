# Kubernetes Components Overview

**Source:** https://kubernetes.io/docs/concepts/overview/components/
**Type:** Official Documentation
**Category:** Fundamentos
**Read:** 2026-03-11

---

## Resumo

Kubernetes cluster = Control Plane + Worker Nodes

### Control Plane Components
| Component | Função |
|-----------|--------|
| **kube-apiserver** | Expõe a Kubernetes HTTP API (front end do control plane). Escala horizontalmente. |
| **etcd** | Key-value store consistente e altamente disponível. Armazena TODOS os dados do cluster. Backup crítico! |
| **kube-scheduler** | Seleciona node para Pods não vinculados. Considera: recursos, constraints, affinity, data locality. |
| **kube-controller-manager** | Executa controllers (Node, Job, EndpointSlice, ServiceAccount). Compilados em único binário. |
| **cloud-controller-manager** | Integração com cloud provider. Controllers: Node, Route, Service (load balancers). |

### Node Components
| Component | Função |
|-----------|--------|
| **kubelet** | Agente em cada node. Garante que containers dos Pods estejam rodando e saudáveis. |
| **kube-proxy** (opcional) | Mantém regras de rede para implementar Services. Pode usar iptables/IPVS. |
| **Container runtime** | Executa containers (containerd, CRI-O, qualquer CRI). |

### Addons
- **DNS**: Cluster DNS (obrigatório para maioria dos exemplos)
- **Web UI (Dashboard)**: Interface web para gerenciamento
- **Container Resource Monitoring**: Métricas de containers (Prometheus, etc.)
- **Cluster-level Logging**: Logs centralizados (ELK, etc.)

---

## Conceitos-Chave

1. **Control Plane vs Worker Nodes**: Separação clara entre gerenciamento e execução
2. **Escalabilidade Horizontal**: API server pode ter múltiplas instâncias
3. **etcd**: Ponto único de verdade - CRÍTICO fazer backup
4. **kubelet**: Não gerencia containers não-Kubernetes
5. **kube-proxy**: Pode ser substituído por CNI plugins que implementam proxy próprio

---

## Próximos Passos
- Ler arquitetura detalhada de nodes
- Estudar etcd backup/restore
- Entender scheduler em profundidade