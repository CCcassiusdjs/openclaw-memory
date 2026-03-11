# Kubernetes MLOps Tutorial

**Source:** https://github.com/AlexIoannides/kubernetes-mlops
**Type:** Tutorial/GitHub
**Category:** MLOps
**Read:** 2026-03-11

---

## Resumo

### Objetivo
Tutorial de MLOps usando:
- Python (Flask) para ML model scoring API
- Docker para containerização
- Kubernetes para orquestração

### Padrão de Deploy ML
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  ML Model    │───▶│  Docker      │───▶│  Kubernetes  │
│  (Python)    │    │  Container   │    │  Cluster     │
│              │    │              │    │              │
│ - Scikit     │    │ - REST API   │    │ - Scaling    │
│ - Keras      │    │ - Flask      │    │ - LB         │
│ - TensorFlow │    │ - Gunicorn   │    │ - Rolling    │
└──────────────┘    └──────────────┘    └──────────────┘
```

---

## Estrutura do Projeto

```
py-flask-ml-score-api/
├── Dockerfile
├── Pipfile
├── Pipfile.lock
└── api.py
```

### API Simples (api.py)
```python
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

@app.route('/score', methods=['POST'])
def score():
    features = request.json['X']
    return make_response(jsonify({'score': features}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Dockerfile
```dockerfile
FROM python:3.6-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install pipenv
RUN pipenv install
EXPOSE 5000
CMD ["pipenv", "run", "python", "api.py"]
```

---

## Docker Commands

```bash
# Build
docker build --tag alexioannides/test-ml-score-api py-flask-ml-score-api

# Run local
docker run --rm --name test-api -p 5000:5000 -d alexioannides/test-ml-score-api

# Test
curl http://localhost:5000/score \
  --request POST \
  --header "Content-Type: application/json" \
  --data '{"X": [1, 2]}'

# Push to registry
docker push alexioannides/test-ml-score-api
```

---

## Kubernetes Deployment

### Setup Local

| Opção | Descrição |
|-------|-----------|
| **Docker Desktop** | Enable Kubernetes in Preferences |
| **Minikube** | `minikube start --memory 4096` |

### Commands

```bash
# Check cluster
kubectl cluster-info

# Deploy
kubectl create deployment test-ml-score-api \
  --image=alexioannides/test-ml-score-api:latest

# Check status
kubectl rollout status deployment test-ml-score-api
kubectl get pods

# Port forward (testing)
kubectl port-forward test-ml-score-api-xxxx 5000:5000

# Expose as service
kubectl expose deployment test-ml-score-api \
  --port 5000 \
  --type=LoadBalancer \
  --name test-ml-score-api-lb
```

---

## Conceitos Kubernetes para ML

### Deployment
- Gerencia rollout de Pods
- Cria ReplicaSet para garantir réplicas
- Rolling updates automáticos

### Pod
- Unidade mínima deployável
- Contém container(s) da aplicação
- IP efêmero

### Service
- Expõe Pods como serviço de rede
- Load balancing entre Pods
- IP estável

---

## Seldon-Core

### O que é?
Framework Kubernetes-native para deploy de ML:
- Simplifica deploy de modelos complexos
- Monitoramento integrado
- A/B testing, canary deployments
- Model explainability

### Benefícios sobre Manual
1. **Less boilerplate**: Menos YAML manual
2. **Inference graphs**: Pipelines de modelos
3. **Autoscaling**: HPA integrado
4. **Metrics**: Prometheus/Grafana ready
5. **Explainability**: SHAP values

---

## Bodywork Framework

### Referência
Este projeto formou a base do **Bodywork**:
- Open-source MLOps tool
- Deploy ML projects developed in Python
- Automatiza muitos passos manuais
- Documentação: https://bodywork.readthedocs.io/

---

## Conceitos-Chave

1. **Container-first**: ML models como containers
2. **Microservices**: ML APIs como serviços independentes
3. **Declarative**: YAML specs para tudo
4. **Scaling**: Kubernetes gerencia réplicas
5. **Cloud-agnostic**: Mesmo spec para qualquer cloud

---

## Lessons Learned

### Production Considerations
- **Use Gunicorn** em produção (não Flask dev server)
- **Health checks**: liveness/readiness probes
- **Resource limits**: CPU/memória
- **Secrets**: não hardcode credenciais
- **Logging**: structured logging

### Testing Strategy
1. **Local**: Docker run + curl
2. **Kubernetes local**: kubectl port-forward
3. **Kubernetes cluster**: Service LoadBalancer

---

## Próximos Passos
- Estudar Seldon-Core para ML específico
- Ver Kubeflow para ML pipelines completos
- Implementar health checks e probes