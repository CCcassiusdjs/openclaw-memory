# HorizontalPodAutoscaler Walkthrough - Kubernetes Official

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/
**Data:** Novembro 2025
**Tópico:** HPA, Autoscaling, Custom Metrics, Resource Metrics
**Status:** Lido

---

## Resumo Executivo

Walkthrough oficial de HorizontalPodAutoscaler (HPA), demonstrando autoscaling baseado em CPU e métricas customizadas com exemplos práticos.

---

## O que é HPA

### Definição
- **HorizontalPodAutoscaler**: Escala workloads automaticamente
- **Target**: Deployment, StatefulSet, ReplicaSet
- **Métricas**: CPU, memória, métricas customizadas
- **Ação**: Aumenta/diminui réplicas conforme demanda

### Horizontal vs Vertical
- **Horizontal**: Mais Pods (HPA)
- **Vertical**: Mais recursos por Pod (VPA)

---

## Pré-requisitos

### Cluster
- Kubernetes >= 1.23
- Mínimo 2 nodes (não control plane)

### Metrics Server
```bash
# Minikube
minikube addons enable metrics-server

# Verificar
kubectl get deployment metrics-server -n kube-system
```

---

## Demo: php-apache

### Deployment e Service
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: php-apache
spec:
  selector:
    matchLabels:
      run: php-apache
  template:
    metadata:
      labels:
        run: php-apache
    spec:
      containers:
      - name: php-apache
        image: registry.k8s.io/hpa-example
        ports:
        - containerPort: 80
        resources:
          limits:
            cpu: 500m
          requests:
            cpu: 200m
---
apiVersion: v1
kind: Service
metadata:
  name: php-apache
  labels:
    run: php-apache
spec:
  ports:
  - port: 80
  selector:
    run: php-apache
```

### Aplicar
```bash
kubectl apply -f https://k8s.io/examples/application/php-apache.yaml
```

---

## Criar HorizontalPodAutoscaler

### Comando kubectl
```bash
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
```

### HPA YAML
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
```

### Verificar Status
```bash
kubectl get hpa

# Output
NAME         REFERENCE                     TARGET   MINPODS MAXPODS REPLICAS AGE
php-apache   Deployment/php-apache/scale   0%/50%   1       10      1        18s
```

---

## Testar Autoscaling

### Gerar Carga
```bash
# Terminal separado
kubectl run -i --tty load-generator --rm --image=busybox:1.28 \
  --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

### Observar Scaling
```bash
kubectl get hpa php-apache --watch

# Output (após ~1 min)
NAME         REFERENCE                     TARGET    MINPODS MAXPODS REPLICAS AGE
php-apache   Deployment/php-apache/scale   305%/50%  1       10      7        3m

# Pods escalaram para 7
kubectl get deployment php-apache
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
php-apache   7/7     7            7           19m
```

### Parar Carga
```bash
# Ctrl+C no terminal do load generator

# Aguardar ~1 min
kubectl get hpa php-apache

# Output
NAME         REFERENCE                     TARGET   MINPODS MAXPODS REPLICAS AGE
php-apache   Deployment/php-apache/scale   0%/50%   1       10      1        11m
```

---

## Métricas Múltiplas e Customizadas

### Resource Metrics
```yaml
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 50
- type: Resource
  resource:
    name: memory
    target:
      type: AverageValue
      averageValue: 500Mi
```

### Pod Metrics (Custom)
```yaml
metrics:
- type: Pods
  pods:
    metric:
      name: packets-per-second
    target:
      type: AverageValue
      averageValue: 1k
```

### Object Metrics (Custom)
```yaml
metrics:
- type: Object
  object:
    metric:
      name: requests-per-second
    describedObject:
      apiVersion: networking.k8s.io/v1
      kind: Ingress
      name: main-route
    target:
      type: Value
      value: 10k
```

---

## Múltiplas Métricas

### Exemplo Completo
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Pods
    pods:
      metric:
        name: packets-per-second
      target:
        type: AverageValue
        averageValue: 1k
  - type: Object
    object:
      metric:
        name: requests-per-second
      describedObject:
        apiVersion: networking.k8s.io/v1
        kind: Ingress
        name: main-route
      target:
        type: Value
        value: 10k
```

### Comportamento
- HPA avalia cada métrica
- Escolhe a contagem de réplicas com valor **mais alto**
- Garante todos os targets sejam atendidos

---

## Label Selectors para Métricas

### Métricas com Labels
```yaml
metrics:
- type: Object
  object:
    metric:
      name: http_requests
      selector:
        matchLabels:
          verb: GET
```

### Comportamento
- Seletor é aditivo
- Pipeline de monitoramento decide como agregar múltiplas séries
- Não pode selecionar métricas de objetos diferentes do target

---

## External Metrics

### Definição
- Métricas que não têm relação direta com objetos Kubernetes
- Exemplo: métricas de serviço hospedado externamente

### Configuração
```yaml
metrics:
- type: External
  external:
    metric:
      name: queue_messages_ready
      selector:
        matchLabels:
          queue: "myqueue"
    target:
      type: AverageValue
      averageValue: 30
```

### Pré-requisitos
- Custom Metrics API configurada
- Adaptador (ex: Prometheus Adapter) instalado
- Métricas expostas corretamente

---

## Algorithm Details

### Fórmula
```
desiredReplicas = ceil[currentReplicas * (currentMetricValue / desiredMetricValue)]
```

### Exemplo
- currentReplicas: 10
- currentMetricValue: 200m
- desiredMetricValue: 100m
- desiredReplicas = ceil[10 * (200/100)] = 20

### Comportamento
- Scale up: Imediato se métrica excede target
- Scale down: Gradual com stabilization window (default 5 min)

---

## Insights para Kubernetes

1. **Metrics Server é obrigatório**: Para resource metrics (CPU, memória)
2. **Custom Metrics requer adapter**: Prometheus Adapter ou similar
3. **Métricas múltiplas = max replicas**: HPA escolhe o valor mais alto
4. **Scale down é gradual**: 5 min stabilization window padrão
5. **Label selectors são aditivos**: Filtram métricas específicas

---

## Palavras-Chave
`hpa` `horizontal-pod-autoscaler` `autoscaling` `custom-metrics` `resource-metrics` `scaling` `kubernetes`