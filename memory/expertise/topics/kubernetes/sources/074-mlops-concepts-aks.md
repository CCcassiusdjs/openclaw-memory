# MLOps Concepts for AI/ML Workflows - Azure AKS

**Fonte:** Microsoft Learn - https://learn.microsoft.com/en-us/azure/aks/concepts-machine-learning-ops
**Data:** Outubro 2024
**Tópico:** MLOps Concepts, DevOps Principles, CI/CD, IaC
**Status:** Lido

---

## Resumo Executivo

Conceitos fundamentais de MLOps para workflows de AI/ML no AKS, detalhando princípios DevOps aplicados (automação, CI/CD, source control, IaC) e o papel de diferentes times.

---

## O que é MLOps?

### Definição
- **Machine Learning Operations**: Práticas para colaboração entre data scientists, IT ops, e business stakeholders
- **Objetivo**: Desenvolver, deployar e manter modelos ML eficientemente
- **Origem**: Aplicação de princípios DevOps para ML

### Ciclo de Vida
```
Training → Packaging → Validating → Deploying → Monitoring → Retraining
     ↑                                                                  |
     └────────────────────────────────────────────────────────────────┘
```

### Inner Loop vs Outer Loop
- **Inner Loop**: Data scientists (training, experimentation)
- **Outer Loop**: ML engineers, IT ops (deployment, monitoring)
- **Feedback Loop**: Retraining quando necessário

---

## Pipeline de MLOps

### Componentes

1. **Unstructured data store**: Dados brutos chegando
2. **Vector database**: Dados processados/embeddings
3. **Data ingestion/indexing**: Framework de processamento
4. **Vector ingestion/retraining workflows**: Pipelines
5. **Metrics collection/alerting**: Monitoramento
6. **Lifecycle management**: Governança

---

## DevOps Principles para MLOps

### 1. Automação

#### Benefícios
- Reduz erros manuais
- Aumenta eficiência
- Garante consistência

#### Automações Possíveis
- Model tuning/retraining em intervalos regulares
- Performance degradation → retraining triggers
- CVE scanning em base images

### 2. Continuous Integration (CI)

#### Cobertura
- **Creating**: Código e modelo
- **Verifying**: Qualidade e performance

#### Atividades CI
- Refactoring Jupyter notebooks → Python scripts
- Validating new input data
- Unit testing e integration testing

#### Ferramentas
- Azure Pipelines
- GitHub Actions
- GitLab CI

### 3. Continuous Delivery (CD)

#### Processo
1. Package model → pre-production (dev/test)
2. Validação em environments
3. Aprovação → production

#### Considerações para LLMs
- Portabilidade de parameters/hyperparameters
- Model artifacts versionados
- Lightweight containers para updates

### 4. Source Control

#### Versionamento
- **Data versioning**: Datasets
- **Code versioning**: Código fonte
- **Model versioning**: Modelos treinados

#### Ferramentas
- Azure Repos
- GitHub repositories
- Git-based versioning

### 5. Agile Planning

#### Práticas
- Sprints curtos
- Tasks bem definidas
- Entregas incrementais

#### Ferramentas
- Azure Boards
- GitHub Issues

### 6. Infrastructure as Code (IaC)

#### Aplicações
- Definir recursos Azure em código
- Version control de infraestrutura
- Resource optimization
- Cost-effectiveness

#### Benefícios
- Reproducibility
- Consistency
- Audit trail

---

## Papéis e Responsabilidades

| Role | Inner Loop | Outer Loop |
|------|------------|------------|
| **Data Scientists** | EDA, Feature Engineering, Training | - |
| **ML Engineers** | - | Packaging, Validation |
| **IT Operations** | - | Deploying, Monitoring |

### Colaboração
- Cross-functional teams
- Git-based workflows
- Shared responsibility

---

## Arquitetura de MLOps no AKS

```
┌─────────────────────────────────────────────────────┐
│                  Source Control                      │
│  (Azure Repos, GitHub)                              │
├─────────────────────────────────────────────────────┤
│                  CI/CD Pipeline                      │
│  (Azure Pipelines, GitHub Actions)                 │
├─────────────────────────────────────────────────────┤
│                  Container Registry                 │
│  (Azure Container Registry, Docker Hub)            │
├─────────────────────────────────────────────────────┤
│                  AKS Cluster                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │ Dev Namespace│ │ Test Namespace│ │ Prod Namespace│ │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐   │
│  │ Model Pods  │ │ GPU Nodes   │ │ Storage     │   │
│  └─────────────┘ └─────────────┘ └─────────────┘   │
├─────────────────────────────────────────────────────┤
│                  Monitoring                         │
│  (Prometheus, Grafana, Azure Monitor)              │
└─────────────────────────────────────────────────────┘
```

---

## MLOps Pipeline Detalhado

### Data Stage
- Ingestion from multiple sources
- Validation e cleaning
- Feature engineering

### Training Stage
- Experiment tracking
- Hyperparameter tuning
- Model selection

### Validation Stage
- Unit tests
- Integration tests
- Performance benchmarks

### Deployment Stage
- Containerization
- Staging deployment
- Production rollout

### Monitoring Stage
- Model performance metrics
- Data drift detection
- Alerting

### Retraining Stage
- Triggered by metrics
- Automated pipelines
- Model updates

---

## Insights para Kubernetes

1. **DevOps + ML = MLOps**: Aplicação direta de princípios
2. **Inner/Outer Loop**: Separação clara de responsabilidades
3. **CI/CD é crítico**: Automação de todo o ciclo
4. **IaC para recursos ML**: Especificação em código
5. **Source control triplo**: Data, code, model

---

## Palavras-Chave
`mlops` `devops` `cicd` `infrastructure-as-code` `source-control` `agile` `automation` `model-lifecycle`