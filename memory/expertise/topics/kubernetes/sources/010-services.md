# Kubernetes Services

**Source:** https://kubernetes.io/docs/concepts/services-networking/service/
**Type:** Official Documentation
**Category:** Fundamentos/Networking
**Read:** 2026-03-11

---

## Resumo

### O que é Service?
Abstração para expor aplicação rodando como um ou mais **Pods**:
- Endpoint único para clientes
- Descoberta automática de backends
- Load balancing entre Pods

### Problema que Resolve
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │ ──▶ │   Backend   │ ──▶ │  Pods?      │
│             │     │   Service   │     │  IP dinâmica│
│  "Qual IP?" │     │  (estável)  │     │  Qual Pod?  │
└─────────────┘     └─────────────┘     └─────────────┘
```
- Pods são efêmeros (IP muda)
- Clientes não sabem quais Pods estão saudáveis
- Service fornece IP estável e descoberta automática

---

## Service Types

| Tipo | Descrição | Use Case |
|------|-----------|----------|
| **ClusterIP** | IP interno do cluster (default) | Comunicação interna |
| **NodePort** | Expõe em cada Node IP:porta | Acesso externo simples |
| **LoadBalancer** | Cloud provider load balancer | Produção cloud |
| **ExternalName** | DNS externo (CNAME) | Integração externa |

---

## Definindo um Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app.kubernetes.io/name: MyApp
  ports:
  - protocol: TCP
    port: 80        # Porta do Service
    targetPort: 9376  # Porta do Pod
```

### Port Definition
- `port`: Porta que o Service expõe
- `targetPort`: Porta do container (default = port)
- `name`: Nome da porta (útil para multi-port)
- `protocol`: TCP (default), UDP, SCTP

---

## Service Discovery

### DNS
- Nome: `<service-name>.<namespace>.svc.cluster.local`
- DNS automático via CoreDNS

### Environment Variables
- `SERVICE_NAME_SERVICE_HOST`
- `SERVICE_NAME_SERVICE_PORT`

### EndpointSlices
- Substituto do antigo Endpoints API
- Escalável para muitos endpoints
- Suporta dual-stack (IPv4/IPv6)

---

## Headless Services

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-headless-service
spec:
  clusterIP: None    # Headless!
  selector:
    app: myapp
```

**Características:**
- Sem ClusterIP
- DNS retorna IPs de todos os Pods
- Útil para:
  - StatefulSets
  - Client-side load balancing
  - Descoberta direta de Pods

---

## Services Without Selectors

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-service
spec:
  ports:
  - name: http
    protocol: TCP
    port: 80
    targetPort: 9376
  # Sem selector!
---
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: external-service-1
  labels:
    kubernetes.io/service-name: external-service
addressType: IPv4
ports:
- name: http
  protocol: TCP
  port: 9376
endpoints:
- addresses:
  - "10.4.5.6"    # IP externo
  - "10.1.2.3"    # IP externo
```

**Use Cases:**
- Banco de dados externo
- Serviços em outro namespace/cluster
- Migração gradual para Kubernetes

---

## Service Types Detalhado

### ClusterIP (Default)
```
┌──────────────────────────────────────┐
│              CLUSTER                  │
│  ┌───────────┐                        │
│  │ Service   │ (ClusterIP: 10.0.0.1)  │
│  │ (ClusterIP)                        │
│  └─────┬─────┘                        │
│        │                              │
│   ┌────┼────┬─────────┐              │
│   ▼    ▼    ▼         ▼              │
│ [Pod] [Pod] [Pod]                    │
└──────────────────────────────────────┘
        │
        ▼
   Apenas interno
```

### NodePort
```
┌──────────────────────────────────────┐
│              CLUSTER                  │
│  ┌───────────┐                        │
│  │ Service   │ (NodePort: 30001)     │
│  │           │ ◄── Externo acessa     │
│  └─────┬─────┘     NodeIP:30001       │
│        │                              │
│   ┌────┼────┬─────────┐              │
│   ▼    ▼    ▼         ▼              │
│ [Pod] [Pod] [Pod]                    │
└──────────────────────────────────────┘
        │
        ▼
   NodeIP:NodePort
```

### LoadBalancer
```
┌──────────────────────────────────────┐
│              CLOUD                    │
│  ┌───────────────────┐              │
│  │   Load Balancer   │              │
│  │  (Cloud Provider) │              │
│  └─────────┬─────────┘              │
│            │                         │
│            ▼                         │
│  ┌──────────────────────────────┐   │
│  │         CLUSTER              │   │
│  │  ┌───────────┐               │   │
│  │  │ Service   │               │   │
│  │  └─────┬─────┘               │   │
│  │        │                      │   │
│  │   [Pod] [Pod] [Pod]          │   │
│  └──────────────────────────────┘   │
└──────────────────────────────────────┘
```

---

## Conceitos-Chave

1. **Abstraction**: Service esconde complexidade de Pods efêmeros
2. **Selector**: Automaticamente encontra Pods matching
3. **ClusterIP**: IP estável dentro do cluster
4. **NodePort**: Expõe em porta alta em cada Node
5. **LoadBalancer**: Integra com cloud provider
6. **Headless**: Sem IP, útil para StatefulSets
7. **EndpointSlices**: API moderna para endpoints

---

## Links Relacionados
- `/docs/concepts/services-networking/ingress/` - Ingress
- `/docs/concepts/services-networking/endpoint-slices/` - EndpointSlices
- `/docs/concepts/services-networking/dual-stack/` - Dual-stack