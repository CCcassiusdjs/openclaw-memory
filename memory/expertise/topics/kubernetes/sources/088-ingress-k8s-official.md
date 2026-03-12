# Ingress - Kubernetes Official Documentation

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/services-networking/ingress/
**Data:** Janeiro 2026
**Tópico:** Ingress, Load Balancing, SSL Termination, Virtual Hosting
**Status:** Lido

---

## Resumo Executivo

Documentação oficial de Ingress, cobrindo conceitos, regras de roteamento, path types, hostname wildcards e IngressClass.

---

## O que é Ingress

### Definição
- API object que gerencia acesso externo a serviços no cluster
- Tipicamente HTTP/HTTPS
- Provê: load balancing, SSL termination, name-based virtual hosting

### Aviso Importante
- **Gateway API é recomendado sobre Ingress**
- Ingress API está "frozen" (sem novos desenvolvimentos)
- Ingress permanece disponível e suportado

### Terminologia
- **Node**: Worker machine no cluster
- **Cluster**: Conjunto de nodes executando apps containerizadas
- **Edge router**: Router que enforce firewall policy
- **Cluster network**: Links de comunicação dentro do cluster
- **Service**: Objeto que identifica Pods via label selectors

---

## Pré-requisitos

### Ingress Controller
- Ingress resource não tem efeito sem controller
- Necessário implantar um Ingress Controller
- Opções: NGINX, HAProxy, Traefik, Istio, Kong, etc.

---

## Ingress Resource

### Estrutura Mínima
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
- apiVersion
- kind
- metadata
- spec

### Campos Específicos
- **ingressClassName**: Referência ao IngressClass
- **rules**: Lista de regras HTTP
- **defaultBackend**: Backend para requests não matcheados

---

## Regras de Ingress

### Componentes
1. **Host** (opcional): Regras aplicam para host específico
2. **Paths**: Lista de paths com backend associado
3. **Backend**: Service + porta ou recurso customizado

### Exemplo com Host
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wildcard-host
spec:
  rules:
  - host: "foo.bar.com"
    http:
      paths:
      - pathType: Prefix
        path: "/bar"
        backend:
          service:
            name: service1
            port:
              number: 80
  - host: "*.foo.com"
    http:
      paths:
      - pathType: Prefix
        path: "/foo"
        backend:
          service:
            name: service2
            port:
              number: 80
```

---

## Path Types

### Tipos Suportados

| Path Type | Descrição |
|-----------|-----------|
| **ImplementationSpecific** | Matching depende do IngressClass |
| **Exact** | Match exato do URL path |
| **Prefix** | Match baseado em prefixo de URL |

### Regras de Prefix
- Matching é case-sensitive
- Dividido por `/` (path elements)
- `/foo/bar` matchea `/foo/bar/baz`
- `/foo/bar` NÃO matchea `/foo/barbaz`

### Exemplos

| Kind | Path(s) | Request path(s) | Matches? |
|------|---------|-----------------|----------|
| Prefix | / | (all paths) | Yes |
| Exact | /foo | /foo | Yes |
| Exact | /foo | /foo/bar | No |
| Prefix | /foo | /foo, /foo/ | Yes |
| Prefix | /aaa/bbb | /aaa/bbb/ccc | Yes |
| Prefix | /aaa/bbb | /aaa/bbbxyz | No |

### Multiple Matches
- Precedência para path mais longo
- Exact > Prefix em caso de empate

---

## Hostname Wildcards

### Regras
- Wildcards cobrem apenas **um DNS label**
- `*.foo.com` matchea `bar.foo.com`
- `*.foo.com` NÃO matchea `baz.bar.foo.com`
- `*.foo.com` NÃO matchea `foo.com`

---

## Default Backend

### Comportamento
- Ingress sem rules: todo tráfico vai para defaultBackend
- Ingress com rules mas sem match: tráfico vai para defaultBackend
- Configurado no Ingress controller, não no Ingress resource

---

## Resource Backends

### Definição
- Backend pode ser ObjectRef para outro recurso Kubernetes
- Mutuamente exclusivo com Service
- Exemplo: StorageBucket para assets estáticos

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

## IngressClass

### Definição
- Cada Ingress deve especificar uma classe
- Referência ao IngressClass com configuração adicional
- Inclui nome do controller que implementa a classe

### Exemplo
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

### Scope
- **Cluster-wide**: Parâmetros globais
- **Namespaced**: Parâmetros específicos por namespace

---

## Ingress Controller

### Necessidade
- Ingress resource não faz nada sozinho
- Necessário implantar um Ingress Controller
- Controller satisfaz o Ingress

### Opções Populares
- NGINX Ingress Controller
- HAProxy Ingress Controller
- Traefik
- Istio Gateway
- Kong Ingress Controller

---

## Insights para Kubernetes

1. **Gateway API é o futuro**: Ingress está frozen
2. **Ingress Controller obrigatório**: Resource sem controller não funciona
3. **Path types importam**: Exact vs Prefix vs ImplementationSpecific
4. **Wildcards limitados**: Apenas um DNS label
5. **Default backend**: Para requests sem match

---

## Palavras-Chave
`ingress` `load-balancing` `ssl-termination` `virtual-hosting` `path-routing` `ingressclass` `kubernetes`