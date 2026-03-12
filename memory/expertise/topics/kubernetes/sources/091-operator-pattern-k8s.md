# Operator Pattern - Kubernetes Official

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
**Data:** Janeiro 2026
**Tópico:** Operators, Custom Resources, Controllers, Automation
**Status:** Lido

---

## Resumo Executivo

Documentação oficial do padrão Operator, cobrindo motivação, conceitos, exemplos e como escrever operators customizados.

---

## O que é um Operator

### Definição
- Software extensions para Kubernetes
- Usam custom resources para gerenciar aplicações
- Seguem princípios do Kubernetes, especialmente o control loop
- Clients do Kubernetes API que agem como controllers

### Motivação
- Capturar conhecimento de operadores humanos
- Automatizar tarefas além do que Kubernetes fornece
- Gerenciar aplicações complexas (databases, brokers, etc.)

---

## O que Operators Automatizam

### Tarefas Comuns
- Deploy de aplicações sob demanda
- Backup e restore de estado
- Upgrades de código e schemas
- Publicar Services para discovery
- Simular falhas para testes de resiliência
- Leader election para aplicações distribuídas

---

## Exemplo: SampleDB Operator

### Componentes
1. **Custom Resource**: SampleDB
2. **Deployment**: Roda o controller
3. **Container Image**: Código do operator
4. **Controller Code**: Consulta API server

### Comportamento

#### Criação
- Novo SampleDB → Operator cria PVC, StatefulSet, Job
- Provisiona storage persistente
- Configura inicialização

#### Deleção
- Operator tira snapshot
- Remove StatefulSet e Volumes

#### Backup Contínuo
- Determina quando criar backup
- Cria Pod com scripts de backup
- Usa ConfigMap/Secret para credenciais

#### Upgrades
- Detecta versão antiga
- Cria Jobs de upgrade

---

## Deploy de Operators

### Método Comum
1. Adicionar Custom Resource Definition
2. Adicionar Controller associado
3. Controller roda fora do control plane

### Exemplo
```yaml
# Deployment do operator
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sampledb-operator
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: operator
        image: myrepo/sampledb-operator:v1
```

---

## Usando um Operator

### Fluxo
```bash
# Verificar recursos configurados
kubectl get SampleDB

# Editar configurações
kubectl edit SampleDB/example-database

# Operator aplica mudanças automaticamente
```

### Benefício
- Usuário não precisa saber criar StatefulSets, Jobs, etc.
- Operator gerencia complexidade automaticamente

---

## Escrevendo seu próprio Operator

### Linguagens/Runtimes Suportados
Qualquer linguagem que tenha client para Kubernetes API.

### Frameworks e Tools

| Framework | Linguagem |
|-----------|-----------|
| **Kubebuilder** | Go |
| **Operator Framework** | Go |
| **Kopf** | Python |
| **Java Operator SDK** | Java |
| **KubeOps** | .NET |
| **kube-rs** | Rust |
| **Charmed Operator Framework** | Python |
| **Metacontroller** | Webhooks |
| **shell-operator** | Shell |
| **Mast** | - |

### Kubebuilder (Go)
```go
// Exemplo de Reconciler
func (r *SampleDBReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch the SampleDB instance
    // 2. Check if StatefulSet exists, create if not
    // 3. Check if PVC exists, create if not
    // 4. Update status
    // 5. Return
}
```

### Kopf (Python)
```python
import kopf

@kopf.on.create('sampledb')
def create_fn(spec, **kwargs):
    # Create StatefulSet, PVC, etc.
    pass

@kopf.on.update('sampledb')
def update_fn(spec, **kwargs):
    # Update resources
    pass

@kopf.on.delete('sampledb')
def delete_fn(**kwargs):
    # Cleanup
    pass
```

---

## Reconciliation Loop

### Conceito
- Core de todo controller
- Compara estado desejado (CR) com estado atual (cluster)
- Faz ajustes para reconciliar

### Fluxo
```
1. Watch for CR events
2. Compare desired state vs actual state
3. Take action to reconcile
4. Update CR status
5. Wait for next event
```

---

## Best Practices

### Owner References
- Definir owner references em recursos filhos
- Garante cleanup automático quando CR é deletado

### Idempotência
- Lógica de reconciliation deve ser idempotente
- Mesmo resultado se rodar 1 ou 100 vezes

### Status Subresource
- Adicionar status ao CRD
- Usuários podem verificar estado com `kubectl get`

### Finalizers
- Usar para cleanup antes de deletar CR
- Garante tarefas necessárias são completadas

### Validação
- Adicionar validação ao schema do CRD
- Rejeita inputs inválidos na API

### Logging
- Logs claros para debugging
- Facilita troubleshooting

---

## Insights para Kubernetes

1. **Operators capturam conhecimento humano**: Automatizam operações complexas
2. **Reconciliation loop é core**: Compare desired vs actual, adjust
3. **Qualquer linguagem**: SDKs disponíveis para várias linguagens
4. **CRD define schema**: Custom Resource Definition cria novos tipos
5. **Best practices são críticas**: Owner references, idempotência, finalizers

---

## Palavras-Chave
`operators` `custom-resources` `controllers` `automation` `kubernetes` `reconciliation-loop` `crd`