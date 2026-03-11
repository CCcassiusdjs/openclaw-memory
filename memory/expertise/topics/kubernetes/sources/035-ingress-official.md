# Kubernetes Ingress (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/services-networking/ingress/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Ingress expõe rotas HTTP e HTTPS de fora do cluster para serviços dentro do cluster, controlando o roteamento de tráfego através de regras definidas.

---

## ⚠️ Nota Importante

**O Kubernetes recomenda usar Gateway API em vez de Ingress.**
- Ingress API está "frozen" (sem novos desenvolvimentos)
- Gateway API é o futuro para configuração de rede

---

## O que é Ingress?

### Definição
- API object que gerencia acesso externo HTTP(S)
- Load balancing, SSL termination, name-based virtual hosting
- Não expõe portas arbitrárias (apenas HTTP/HTTPS)
- Requer Ingress Controller

### Componentes
1. **Ingress Resource**: Regras de roteamento
2. **Ingress Controller**: Implementação (nginx, traefik, etc.)
3. **IngressClass**: Define qual controller usar

---

## Ingress Resource

### Exemplo Mínimo
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
spec:
  ingressClassName: nginx-example
  rules:
  - http:
      paths:
      - path: /testpath
        pathType: Prefix
        backend:
          service:
            name: test
            port:
              number: 80
```

### Campos Obrigatórios
- `apiVersion`, `kind`, `metadata`
- `spec.rules` ou `spec.defaultBackend`

---

## Path Types

### ImplementationSpecific
- Matching depende do IngressClass
- Implementação específica

### Exact
- Match exato do path
- Case-sensitive

### Prefix
- Match por prefixo de path
- Case-sensitive
- Element-wise (separado por /)

### Exemplos
| Kind | Path | Request | Match? |
|------|------|---------|--------|
| Prefix | / | /foo | Yes |
| Exact | /foo | /foo | Yes |
| Exact | /foo | /bar | No |
| Prefix | /foo | /foo/bar | Yes |
| Prefix | /aaa/bbb | /aaa/bbbxyz | No |

---

## Hostname Wildcards

```yaml
spec:
  rules:
  - host: "*.foo.com"
    http:
      paths:
      - path: /foo
        pathType: Prefix
```

**Notas:**
- `*.foo.com` match um label DNS
- `bar.foo.com` ✓
- `baz.bar.foo.com` ✗ (dois labels)

---

## IngressClass

### Definição
```yaml
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  name: external-lb
spec:
  controller: example.com/ingress-controller
  parameters:
    apiGroup: k8s.example.com
    kind: IngressParameters
    name: external-lb
```

### Default IngressClass
```yaml
metadata:
  annotations:
    ingressclass.kubernetes.io/is-default-class: "true"
```

**Nota:** Apenas uma IngressClass pode ser default.

---

## Tipos de Ingress

### 1. Single Service
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: test-ingress
spec:
  defaultBackend:
    service:
      name: test
      port:
        number: 80
```

### 2. Simple Fanout
```yaml
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - path: /foo
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 4200
      - path: /bar
        pathType: Prefix
        backend:
          service:
            name: service2
            port:
              number: 8080
```

### 3. Name-Based Virtual Hosting
```yaml
spec:
  rules:
  - host: foo.bar.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: service1
            port:
              number: 80
  - host: bar.foo.com
    http:
      paths:
      - pathType: Prefix
        path: "/"
        backend:
          service:
            name: service2
            port:
              number: 80
```

---

## TLS

### TLS Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: testsecret-tls
data:
  tls.crt: base64-encoded-cert
  tls.key: base64-encoded-key
type: kubernetes.io/tls
```

### Ingress com TLS
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tls-example-ingress
spec:
  tls:
  - hosts:
    - https-example.foo.com
    secretName: testsecret-tls
  rules:
  - host: https-example.foo.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: service1
            port:
              number: 80
```

**Nota:** TLS termina no Ingress (tráfego interno é plaintext).

---

## Resource Backends

Backend para recursos externos (ex: storage):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-resource-backend
spec:
  defaultBackend:
    resource:
      apiGroup: k8s.example.com
      kind: StorageBucket
      name: static-assets
  rules:
  - http:
      paths:
      - path: /icons
        pathType: ImplementationSpecific
        backend:
          resource:
            apiGroup: k8s.example.com
            kind: StorageBucket
            name: icon-assets
```

---

## Ingress Controllers

### Requisitos
- Ingress resource sozinho não faz nada
- Precisa de um Ingress Controller

### Populares
| Controller | Descrição |
|------------|-----------|
| **NGINX** | Mais popular, open source |
| **Traefik** | Cloud native, features avançadas |
| **HAProxy** | High performance |
| **Contour** | Envoy-based |
| **Istio Gateway** | Service mesh |
| **GCE/ALB** | Cloud providers |

---

## Load Balancing

### Features do Controller
- Load balancing algorithm
- Backend weight scheme
- Health checks

### Limitações
- Persistent sessions: via Service
- Dynamic weights: via Service
- Advanced features: via Service Mesh

---

## Alternatives

Para expor serviços não-HTTP:
- **Service.Type=LoadBalancer**: Expõe qualquer porta
- **Service.Type=NodePort**: Expõe em portas dos nodes

---

## Conceitos-Chave

1. **Ingress Resource**: Regras de roteamento HTTP(S)
2. **Ingress Controller**: Implementação (nginx, traefik, etc.)
3. **IngressClass**: Define controller específico
4. **Path Types**: Exact, Prefix, ImplementationSpecific
5. **TLS Termination**: Certificados no Ingress

---

## Best Practices

1. **Default Backend**: Sempre configurar
2. **IngressClass**: Especificar explicitamente
3. **TLS**: Usar certificados válidos
4. **Health Checks**: Configurar no controller
5. **Annotations**: Usar para features específicas do controller

---

## Próximos Passos de Estudo

- [ ] Gateway API (sucessor do Ingress)
- [ ] NGINX Ingress Controller
- [ ] Traefik Ingress
- [ ] Istio Gateway
- [ ] Cert-manager para TLS automático

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/services-networking/ingress/
- Gateway API: https://gateway-api.sigs.k8s.io/
- Ingress Controllers: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/