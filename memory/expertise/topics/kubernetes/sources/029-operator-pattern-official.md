# Kubernetes Operator Pattern (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

Operators são extensões de software que usam Custom Resources para gerenciar aplicações e seus componentes, seguindo princípios do Kubernetes, notadamente o control loop.

---

## Motivação

O padrão Operator captura o objetivo de um **operador humano** que gerencia um serviço:
- Conhecimento profundo do sistema
- Como deve se comportar
- Como deployar
- Como reagir a problemas

### Automação
- Automatizar tarefas além do que Kubernetes fornece nativamente
- Capturar conhecimento operacional em código
- Gerenciar ciclo de vida completo da aplicação

---

## O que são Operators?

### Definição
- Extensões de software para Kubernetes
- Usam Custom Resources para definir estado desejado
- Implementam control loops para reconciliar estado
- Agem como controllers para Custom Resources

### Relação com Controllers
Operators são **clients of the Kubernetes API** que agem como controllers para Custom Resources.

---

## Exemplo de Operator

### SampleDB Operator
Um operator para gerenciar um banco de dados customizado:

```
SampleDB (Custom Resource)
    ↓
Operator (Controller)
    ├── Cria PersistentVolumeClaims
    ├── Cria StatefulSet
    ├── Cria Job para configuração inicial
    ├── Gerencia backups regulares
    └── Monitora versão e executa upgrades
```

### Componentes
1. **Custom Resource Definition (CRD)**: Define SampleDB
2. **Deployment**: Roda o controller do operator
3. **Container Image**: Código do operator
4. **Controller Code**: Lógica de reconciliação

### Funcionalidades Automatizadas
- Deploy de aplicação sob demanda
- Backup e restore
- Upgrades (incluindo schema changes)
- Service discovery
- Failure simulation
- Leader election

---

## Deployando Operators

### Método Comum
1. Adicionar CRD ao cluster
2. Adicionar Controller (como Deployment)
3. Controller roda fora do control plane

### Operação
```bash
# Ver databases configurados
kubectl get SampleDB

# Editar configuração
kubectl edit SampleDB/example-database

# Operator aplica mudanças automaticamente
```

---

## Operator Frameworks

### SDKs Populares

| Framework | Linguagem | Status |
|-----------|-----------|--------|
| Kubebuilder | Go | CNCF |
| Operator Framework | Go | Red Hat |
| Java Operator SDK | Java | Ativo |
| Kopf | Python | Ativo |
| Kube-rs | Rust | Ativo |
| KubeOps | .NET | Ativo |
| Shell-operator | Shell | Ativo |
| Metacontroller | Any | WebHooks |

### Kubebuilder
- Framework mais popular para Go
- Gera CRDs e controllers
- Integração com kubectl
- Scaffold completo

### Operator SDK
- Red Hat
- Suporta Go, Ansible, Helm
- Operator Lifecycle Manager (OLM) integration
- OperatorHub integration

---

## Operator Capability Levels

### Níveis de Maturidade

| Nível | Nome | Descrição |
|-------|------|-----------|
| **1** | Basic Install | Instala e configura |
| **2** | Seamless Upgrades | Upgrades sem downtime |
| **3** | Full Lifecycle | Backup, restore, failover |
| **4** | Deep Insights | Metrics, alerts, debugging |
| **5** | Auto Pilot | Auto-tuning, scaling, healing |

---

## Exemplos de Operators do Mundo Real

### Banco de Dados
- **PostgreSQL**: CrunchyData, Zalando
- **MySQL**: Oracle, Presslabs
- **MongoDB**: MongoDB Inc
- **Redis**: Spotahome, Redis Labs

### Observabilidade
- **Prometheus**: prometheus-operator
- **Grafana**: grafana-operator
- **Jaeger**: jaeger-operator

### Service Mesh
- **Istio**: istio-operator
- **Linkerd**: linkerd-operator

---

## Best Practices

1. **Single Purpose**: Um operator por aplicação
2. **Idempotency**: Operações devem ser idempotentes
3. **Graceful Degradation**: Falhas não devem corromper estado
4. **Observability**: Logs, metrics, events
5. **Testing**: Unit, integration, e2e tests

---

## Conceitos-Chave

1. **Custom Resource Definition (CRD)**: Define novo tipo de recurso
2. **Controller**: Loop que reconcilia estado desejado com atual
3. **Reconciliation**: Processo de tornar estado atual = estado desejado
4. **Operator Pattern**: Automatização de conhecimento operacional

---

## Casos de Uso Comuns

| Caso | Benefício |
|------|-----------|
| Databases | Backup automático, upgrades |
| Messaging | Clustering, configuração |
| Monitoring | Provisionamento, descoberta |
| CI/CD | Pipelines como código |
| Security | Policy enforcement |

---

## Próximos Passos de Estudo

- [ ] Kubebuilder tutorial
- [ ] Operator SDK
- [ ] CRD validation
- [ ] Webhook admission controllers
- [ ] Operator Lifecycle Manager (OLM)

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
- OperatorHub: https://operatorhub.io/
- CNCF Operator White Paper: https://github.com/cncf/tag-app-delivery/blob/main/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md
- Kubebuilder Book: https://book.kubebuilder.io/