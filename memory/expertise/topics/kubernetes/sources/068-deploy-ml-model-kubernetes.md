# Deploy ML Model on Kubernetes - MLOps Tutorial

**Fonte:** https://medium.com/@iamvikramkumar5/mlops-deploy-your-first-ml-model-on-kubernetes-e9bfdb1d6136
**Tipo:** Tutorial
**Data:** 2026-03-12

---

## Resumo

Tutorial prático de MLOps completo: desde treinamento até deploy em Kubernetes. Demonstra o ciclo de vida completo com um modelo de predição de diabetes usando Random Forest.

---

## Conceitos Principais

### MLOps Workflow
- **Data Ingestion & Preparation:** Coleta, limpeza e estruturação de dados
- **Model Training:** Algoritmos ML (Random Forest, etc.)
- **Evaluation:** Métricas (accuracy, precision, recall, ROC-AUC)
- **Deployment:** Containerização (Docker) + orquestração (Kubernetes)
- **Monitoring & Retraining:** Prometheus, Grafana, MLflow

### Stack Tecnológica
- **FastAPI:** API REST para servir modelos
- **Docker:** Containerização
- **Kind (Kubernetes in Docker):** Cluster local para desenvolvimento
- **kubectl:** CLI para Kubernetes

### Pipeline Implementation
```yaml
# Deploy.yaml structure
- Deployment: replicas, image, ports, resources
- Service: ClusterIP/NodePort/LoadBalancer
- ConfigMap: configurações não-sensíveis
- Secret: dados sensíveis
- HPA: autoscaling baseado em métricas
```

### MLOps Pipeline Stages
1. **Desenvolvimento:** Jupyter notebooks, experimentação
2. **Containerização:** Dockerfile, requirements.txt
3. **Orquestração:** Kubernetes manifests, Services, Deployments
4. **CI/CD:** GitHub Actions (futuro)
5. **Monitoring:** Prometheus + Grafana + Evidently AI

---

## Insights

### Por que Docker + Kubernetes?
- **Docker:** Consistência de ambiente
- **Kubernetes:** Escalabilidade, load balancing, self-healing

### Problemas Comuns MLOps
- 80-90% dos modelos nunca chegavam em produção
- Falta de automação e processos estruturados
- Complexidade de deployment

### Ferramentas de Monitoring
- **Prometheus + Grafana:** Performance de API
- **Evidently AI / WhyLogs:** Data drift, accuracy, prediction stability
- **Alerts:** Comportamento inesperado

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| MLOps Lifecycle | Data → Training → Evaluation → Deployment → Monitoring |
| Model Serialization | .pkl files para reutilização |
| FastAPI Serving | REST API para inferência |
| Kind Cluster | Kubernetes local para desenvolvimento |
| Port Forwarding | Acesso a Services via kubectl port-forward |

---

## Próximos Passos

- Implementar CI/CD com GitHub Actions
- Adicionar monitoring com Prometheus/Grafana
- Implementar data drift detection
- Configurar retraining automático