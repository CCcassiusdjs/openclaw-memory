# Service Mesh: Istio vs Linkerd Setup Guide

**Fonte:** OneUptime Blog - https://oneuptime.com/blog/post/2026-01-06-kubernetes-service-mesh-istio-linkerd/view
**Data:** Janeiro 2026
**Tópico:** Service Mesh, Istio, Linkerd, mTLS, Traffic Management, Sidecars
**Status:** Lido

---

## Resumo Executivo

Guia completo de setup de Service Mesh com Istio e Linkerd, incluindo instalação, sidecar injection, traffic splitting, mTLS, e observabilidade.

---

## O que é Service Mesh

### Definição
- Infraestrutura para comunicação service-to-service
- Sidecar proxies interceptam todo tráfego
- Aplica políticas consistentemente sem mudanças no código

### Arquitetura
```
Pod A                    Pod B
┌─────────────┐         ┌─────────────┐
│   App A     │────────▶│   App B     │
│     │       │         │     ▲       │
│  Proxy A    │──mTLS──▶│  Proxy B    │
└─────────────┘         └─────────────┘
      ▲                       ▲
      │       Control Plane    │
      └───────────────────────┘
```

### Quando Usar
- mTLS sem mudanças na aplicação
- Traffic splitting para canary deployments
- Retries e circuit breakers automáticos
- Distributed tracing
- Políticas de tráfego fine-grained

### Quando NÃO Usar
- Aplicações simples com poucos serviços
- Times não preparados para complexidade
- Resource constraints (sidecars adicionam overhead)

---

## Istio vs Linkerd

| Feature | Istio | Linkerd |
|---------|-------|---------|
| **Resource footprint** | ~100MB per sidecar | ~20MB per sidecar |
| **Complexity** | Higher | Lower |
| **Features** | Everything | Essential features |
| **Learning curve** | Steep | Gentle |
| **mTLS** | Yes | Yes |
| **Traffic management** | Advanced | Basic |
| **Multi-cluster** | Yes | Yes |
| **CNCF status** | Graduated | Graduated |

---

## Linkerd Setup

### Install CLI
```bash
# macOS
brew install linkerd

# Linux
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$HOME/.linkerd2/bin:$PATH

# Verify
linkerd version
```

### Pre-Installation Check
```bash
linkerd check --pre
```

### Install Control Plane
```bash
# Install CRDs
linkerd install --crds | kubectl apply -f -

# Install control plane
linkerd install | kubectl apply -f -

# Verify
linkerd check
```

### Install Viz Extension
```bash
linkerd viz install | kubectl apply -f -
linkerd viz check
linkerd viz dashboard &
```

### Inject Sidecars
```bash
# Inject into existing deployments
kubectl get deploy -n production -o yaml | linkerd inject - | kubectl apply -f -

# Or annotate namespace for auto-injection
kubectl annotate namespace production linkerd.io/inject=enabled
```

### Verify Mesh Traffic
```bash
# Check meshed pods status
linkerd viz stat deploy -n production

# Watch live traffic
linkerd viz top deploy/api -n production

# View traffic routes
linkerd viz routes deploy/api -n production
```

---

## Linkerd Traffic Split (Canary)

```yaml
apiVersion: split.smi-spec.io/v1alpha1
kind: TrafficSplit
metadata:
  name: api-canary
  namespace: production
spec:
  service: api
  backends:
  - service: api-stable
    weight: 900m  # 90%
  - service: api-canary
    weight: 100m  # 10%
```

---

## Linkerd Service Profiles (Retries & Timeouts)

```yaml
apiVersion: linkerd.io/v1alpha2
kind: ServiceProfile
metadata:
  name: api.production.svc.cluster.local
  namespace: production
spec:
  routes:
  - name: GET /api/v1/users
    condition:
      method: GET
      pathRegex: /api/v1/users
    responseClasses:
    - condition:
        status:
          min: 500
          max: 599
      isFailure: true
    timeout: 30s
    retries:
      isRetryable: true
      maxRetries: 3
```

---

## Istio Setup

### Install istioctl
```bash
# macOS
brew install istioctl

# Linux
curl -L https://istio.io/downloadIstio | sh -
cd istio-*
export PATH=$PWD/bin:$PATH

# Verify
istioctl version
```

### Pre-Installation Check
```bash
istioctl x precheck
```

### Install Istio
```bash
# Demo profile (includes observability)
istioctl install --set profile=demo -y

# Or minimal profile (production)
istioctl install --set profile=minimal -y

# Verify
istioctl verify-install
kubectl get pods -n istio-system
```

### Enable Sidecar Injection
```bash
# Label namespace for auto-injection
kubectl label namespace production istio-injection=enabled

# Restart existing pods
kubectl rollout restart deployment -n production
```

### Install Observability Add-ons
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/prometheus.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/grafana.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/jaeger.yaml
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.24/samples/addons/kiali.yaml

# Access Kiali dashboard
istioctl dashboard kiali
```

---

## Istio Virtual Service (Traffic Routing)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routing
  namespace: production
spec:
  hosts:
  - api
  http:
  # Header-based routing
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: api
        subset: canary
  # Weighted routing (canary)
  - route:
    - destination:
        host: api
        subset: stable
      weight: 90
    - destination:
        host: api
        subset: canary
      weight: 10
```

---

## Istio Destination Rule (Load Balancing & Subsets)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-destination
  namespace: production
spec:
  host: api
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: UPGRADE
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000
    loadBalancer:
      simple: LEAST_REQUEST
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
  subsets:
  - name: stable
    labels:
      version: stable
  - name: canary
    labels:
      version: canary
```

---

## Istio Circuit Breaker

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-circuit-breaker
  namespace: production
spec:
  host: api
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
      minHealthPercent: 30
```

---

## Istio Retry Policy

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-retries
  namespace: production
spec:
  hosts:
  - api
  http:
  - route:
    - destination:
        host: api
    retries:
      attempts: 3
      perTryTimeout: 10s
      retryOn: 5xx,reset,connect-failure,retriable-4xx
```

---

## Istio Timeout Policy

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-timeout
  namespace: production
spec:
  hosts:
  - api
  http:
  - route:
    - destination:
        host: api
    timeout: 30s
```

---

## mTLS Configuration

### Linkerd mTLS
- **Zero-config**: Habilitado automaticamente para todo tráfego meshed
- Verificar: `linkerd viz edges deployment -n production`

### Istio mTLS
```yaml
# Strict mTLS por namespace
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT

---
# Cluster-wide mTLS
apiVersion: security.istio.io/v1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
```

---

## Istio Authorization Policy

```yaml
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: api-authz
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/production/sa/frontend
    to:
    - operation:
        methods: ["GET", "POST"]
        paths: ["/api/v1/*"]
```

---

## Observability

### Distributed Tracing
- Ambos propagam trace headers automaticamente (B3, W3C)
- Jaeger para visualização

### Linkerd com Jaeger
```bash
linkerd jaeger install | kubectl apply -f -
```

### Istio com Jaeger
- Já incluído no demo profile
- Acessar: `istioctl dashboard jaeger`

---

## Insights para Kubernetes

1. **Linkerd é mais simples**: ~20MB vs ~100MB, learning curve gentil
2. **Istio é mais feature-rich**: Traffic management avançado
3. **mTLS automático**: Linkerd por padrão, Istio requer configuração
4. **Traffic splitting**: Ambos suportam canary deployments
5. **Observabilidade incluída**: Dashboards, tracing, metrics

---

## Palavras-Chave
`service-mesh` `istio` `linkerd` `mtls` `traffic-management` `sidecars` `circuit-breaker` `kubernetes`