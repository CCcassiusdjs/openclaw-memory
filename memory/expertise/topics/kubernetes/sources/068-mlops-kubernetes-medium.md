# MLOps — Deploy Your First ML Model on Kubernetes

**Fonte:** Medium - https://medium.com/@iamvikramkumar5/mlops-deploy-your-first-ml-model-on-kubernetes-e9bfdb1d6136
**Data:** Julho 2025
**Tópico:** MLOps, Kubernetes, FastAPI, Docker
**Status:** Lido

---

## Resumo Executivo

Tutorial prático de MLOps demonstrando o ciclo completo de deploy de um modelo ML (predição de diabetes) em Kubernetes, incluindo containerização com Docker e serving com FastAPI.

---

## Conceitos-Chave

### O que é MLOps
- **MLOps (Machine Learning Operations)**: Disciplina que combina práticas de ML com DevOps
- **Objetivo**: Automatizar o ciclo de vida completo de modelos ML
- **Antes do MLOps**: 80-90% dos modelos ML nunca chegavam à produção
- **Estrutura**: Pipeline automatizado similar ao ciclo de desenvolvimento de software

### Ciclo de Vida MLOps
1. **Data Ingestion & Preparation**: Coleta, limpeza, normalização
2. **Model Training**: Treino com algoritmos (ex: Random Forest)
3. **Evaluation**: Validação com métricas (accuracy, precision, recall, ROC-AUC)
4. **Deployment**: Containerização, serving via API, deploy em K8s
5. **Monitoring & Retraining**: Monitoramento contínuo, detecção de drift

### Stack Tecnológico
- **Modelo**: Random Forest Classifier
- **Dataset**: Pima Indians Diabetes Dataset
- **API**: FastAPI para serving
- **Container**: Docker para empacotamento
- **Orquestração**: Kubernetes (Kind para local)

---

## Fluxo de Implementação

### 1. Preparação do Ambiente
```bash
# Clone do repo
git clone https://github.com/iamvikramkumar5/mlops
cd mlops

# Virtual environment
python -m venv .mlops
source .mlops/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Treinamento do Modelo
```bash
python train.py
# Gera modelo serializado (.pkl)
```

### 3. Serving Local (FastAPI)
```bash
uvicorn main:app --reload
# Acessível em http://localhost:8000/docs
```

### 4. Containerização Docker
```bash
# Build
docker build -t diabetes-model-demo .

# Run local
docker run -p 8000:8000 diabetes-model-demo

# Push para registry
docker tag <image-id> iamvikramkumar/diabetes-model-demo:v1
docker push iamvikramkumar/diabetes-model-demo:v1
```

### 5. Deploy em Kubernetes
```bash
# Criar cluster
kind create cluster --name demo-mlops

# Verificar contexto
kubectl config current-context
kubectl get nodes

# Aplicar manifesto
kubectl apply -f deploy.yaml

# Monitorar
kubectl get pods -w
kubectl get svc

# Port forward
kubectl port-forward svc/diabetes-api-service 1111:80 --address=0.0.0.0
```

---

## Benefícios de Docker + Kubernetes

### Docker
- **Consistência**: Ambiente reproduzível
- **Portabilidade**: Roda em qualquer lugar
- **Isolamento**: Dependências encapsuladas

### Kubernetes
- **Escalabilidade**: Auto-scaling de pods
- **Load Balancing**: Distribuição de carga
- **Self-healing**: Recuperação automática
- **Rolling Updates**: Deploy sem downtime

---

## Arquitetura de Produção

### CI/CD (Conceitual)
- Testes automáticos de modelo
- Build de imagens Docker
- Deploy automático em clusters
- Validação de mudanças

### Monitoramento (Conceitual)
- **Prometheus + Grafana**: Performance de API
- **Evidently AI**: Data drift, accuracy
- **WhyLogs**: Estabilidade de predições
- **Alertas**: Comportamento anômalo

---

## Insights para Kubernetes

1. **MLOps é essencial**: Sem automação, maioria dos modelos falha em produção
2. **Kubernetes é padrão**: Para deploy escalável de ML
3. **Pipeline completo**: Data prep → Train → Deploy → Monitor
4. **Containerização obrigatória**: Para consistência e portabilidade
5. **Monitoramento crítico**: Modelos degradam com tempo

---

## Palavras-Chave
`mlops` `kubernetes` `docker` `fastapi` `model-deployment` `machine-learning` `production` `pipeline` `monitoring`