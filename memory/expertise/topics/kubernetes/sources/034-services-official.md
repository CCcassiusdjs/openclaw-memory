# Kubernetes Services (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/services-networking/service/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Service é uma abstração que expõe uma aplicação rodando em um conjunto de Pods como um serviço de rede, fornecendo descoberta e balanceamento de carga.

---

## O que é Service?

### Problema
- Pods são efêmeros (criados/destruídos)
- IPs mudam quando Pods recriam
- Descoberta automática necessária

### Solução
- Service fornece IP estável (ou DNS name)
- Load balancing automático
- Service discovery

---

## Definição de Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
```

### Campos Obrigatórios
- **selector**: Seleciona Pods para o Service
- **ports**: Portas expostas
- **port**: Porta do Service
- **targetPort**: Porta do Pod (padrão: mesma que port)

---

## Tipos de Service

### ClusterIP (Default)
- IP interno do cluster
- Acessível apenas dentro do cluster
- Útil para serviços internos

```yaml
spec:
  type: ClusterIP
```

### NodePort
- Expõe em cada node em uma porta estática
- Acessível de fora do cluster
- Porta: 30000-32767

```yaml
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30007
```

### LoadBalancer
- Expõe externamente via cloud load balancer
- Cria NodePort e ClusterIP automaticamente

```yaml
spec:
  type: LoadBalancer
```

### ExternalName
- Mapeia para DNS externo
- Não cria proxy

```yaml
spec:
  type: ExternalName
  externalName: my.external.service.com
```

---

## Port Definitions

```yaml
ports:
- name: http          # Opcional
  protocol: TCP       # TCP, UDP, SCTP
  port: 80            # Porta do Service
  targetPort: 8080    # Porta do Pod
  nodePort: 30007     # NodePort (tipo NodePort)
```

### Múltiplas Portas
```yaml
ports:
- name: http
  port: 80
  targetPort: 8080
- name: https
  port: 443
  targetPort: 8443
```

---

## Selector-less Services

Services sem selector para endpoints customizados:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  ports:
  - protocol: TCP
    port: 80
    targetPort: 9376
---
apiVersion: discovery.k8s.io/v1
kind: Endpoints
metadata:
  name: my-service
subsets:
- addresses:
  - ip: 192.168.1.1
  - ip: 192.168.1.2
  ports:
  - port: 9376
```

---

## Headless Services

Para quando não precisa de load balancing:

```yaml
spec:
  clusterIP: None  # Headless
  selector:
    app: MyApp
```

**Uso:**
- StatefulSets
- Service discovery via DNS
- DNS SRV records

---

## Endpoints e EndpointSlices

### Endpoints (v1)
- Limitado a 1000 addresses
- API obsoleta

### EndpointSlices (discovery.k8s.io/v1)
- Suporta múltiplos slices
- Mais eficiente
- Escala melhor

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: example-abc
  labels:
    kubernetes.io/service-name: example
addressType: IPv4
ports:
- name: http
  port: 80
endpoints:
- addresses:
  - "10.1.2.3"
```

---

## Traffic Policies

### Internal Traffic Policy
```yaml
spec:
  internalTrafficPolicy: Local
```
- Tráfego interno roteado apenas para Pods locais
- Reduz hops de rede

### External Traffic Policy
```yaml
spec:
  type: LoadBalancer
  externalTrafficPolicy: Local
```
- Preserva source IP
- Apenas Pods no node recebem tráfego

---

## Session Affinity

### ClientIP
```yaml
spec:
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800  # 3 hours
```

### None (Default)
- Sem affinity
- Random distribution

---

## DNS Records

### ClusterIP Service
```
my-service.my-namespace.svc.cluster.local
```

### Headless Service
```
my-service.my-namespace.svc.cluster.local
→ aponta para todos os Pod IPs
```

### SRV Records (Headless com named ports)
```
_my-port-name._my-port-protocol.my-service.my-namespace.svc.cluster.local
```

---

## External IPs

```yaml
spec:
  externalIPs:
  - 80.11.12.10
  ports:
  - port: 80
    targetPort: 8080
```

- Rotearia tráfego externo para o Service
- **Risco:** Security implications

---

## Conceitos-Chave

1. **ClusterIP**: IP interno do cluster
2. **NodePort**: Expõe em porta fixa em cada node
3. **LoadBalancer**: Cloud provider load balancer
4. **Headless**: Sem IP cluster (DNS discovery)
5. **EndpointSlice**: Escalabilidade para endpoints

---

## Best Practices

1. **Named ports**: Usar nomes em vez de números
2. **Readiness probes**: Services respeitam readiness
3. **Session affinity**: Usar com cuidado
4. **ExternalTrafficPolicy**: Local para preservar source IP
5. **DNS**: Usar nomes de serviço em vez de IPs

---

## Próximos Passos de Estudo

- [ ] Service Mesh integration
- [ ] Topology Aware Routing
- [ ] Service with Ingress
- [ ] Multi-cluster Services

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/services-networking/service/
- EndpointSlices: https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/
- DNS: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/