# MLflow vs Weights & Biases vs ZenML - ZenML Blog

**Fonte:** https://www.zenml.io/blog/mlflow-vs-weights-and-biases
**Autor:** ZenML Blog
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Comparação abrangente das três ferramentas MLOps mais populares. Explica diferenças fundamentais: MLflow (experiment tracking + model registry), W&B (cloud experiment tracking + visualization), ZenML (pipeline orchestration).

---

## 🎯 Visão Geral

| Ferramenta | Foco Principal | Tipo |
|------------|---------------|------|
| **MLflow** | Experiment tracking, Model registry | Open-source |
| **W&B** | Experiment tracking, Visualization | Cloud-hosted |
| **ZenML** | Pipeline orchestration | Open-source |

**TL;DR:**
- **Experiment tracking**: MLflow ou W&B
- **Model registry**: MLflow (turnkey) ou ZenML (pipeline lineage)
- **Pipeline orchestration**: ZenML
- **Collaboration & visualization**: W&B

---

## 📊 Feature 1: Experiment Tracking

### MLflow
- API e UI para logar parâmetros, métricas, outputs
- Funciona em qualquer ambiente (script, notebook, cloud)
- Suporta múltiplos usuários com tracking server compartilhado
- **Auto-logging** para TensorFlow, PyTorch, etc.
- Language-agnostic: Python, R, Java, REST

### Weights & Biases
- Experiência de tracking mais polida
- `wandb.init()` para inicializar run
- Salva automaticamente: código, hyperparams, system metrics, checkpoints
- **Hosted**: Sem setup de servidor, UI web instantânea
- Dashboards em tempo real

### ZenML
- Não substitui trackers, **integra com eles**
- Plugins (flavors) para MLflow, W&B, etc.
- Pipeline roda com tracker configurado no stack
- Exemplo: ZenML orquestra pipeline + MLflow loga métricas

---

## 📦 Feature 2: Model Registry & Artifact Versioning

### MLflow
- **Model Registry** built-in
- Central hub para gerenciar lifecycle de modelos
- Features: versioning, stages (Staging, Production), annotations, webhooks
- Artifacts salvos em backend configurável (local, S3, etc.)

```python
# Exemplo: Registrar modelo no MLflow
mlflow.sklearn.log_model(
    sk_model=model,
    artifact_path="sklearn-model",
    registered_model_name="sk-learn-random-forest-reg-model"
)
```

### Weights & Biases
- **Artifacts system** para versioning
- Cada artifact = data item versionado
- Model Registry UI construída sobre artifacts
- Versioning automático de arquivos

```python
# Exemplo: Logar artifact no W&B
artifact = wandb.Artifact(name="model", type="model")
artifact.add_file(local_path="./model.h5")
run.log_artifact(artifact)
```

### ZenML
- Artifact store integrado com pipeline
- Cada step produz artifacts versionados por run
- Metadata store racha URLs e lineage
- **End-to-end lineage**: sabe como modelo foi produzido
- Model Registry disponível em planos pagos

---

## 🔄 Feature 3: Pipeline Orchestration

### MLflow
- **NÃO é orchestrator**
- Ferramenta de tracking e model management
- Precisa de orchestrator externo: Airflow, Prefect, Kubeflow, ZenML

### Weights & Biases
- **NÃO é orchestrator**
- W&B Sweeps: hyperparameter search (grid, Bayesian, etc.)
- W&B Launch: deploy de training jobs em diferentes ambientes
- Não encadeia steps em DAG

### ZenML
- **Core purpose: pipeline orchestration**
- Define steps como Python functions/classes
- Composes into pipeline, ZenML executa em ordem correta
- Features:
  - Caching: steps não re-rodam se dados não mudaram
  - Artifact passing: outputs passam automaticamente para próximos steps
  - Config management
  - Multiple orchestrators: local, Airflow, Kubeflow, Vertex AI

```python
# Exemplo: Pipeline ZenML
@step
def preprocess_data(data_path: str) -> str:
    return processed_data

@step
def train_model(data: str):
    return model

@pipeline
def my_pipeline(data_path: str):
    processed_data = preprocess_data(data_path)
    model = train_model(processed_data)
```

---

## 👥 Feature 4: Collaboration & Visualization

### MLflow
- Colaboração via tracking server compartilhado
- UI relativamente básica
- Sem user accounts/auth no open-source
- Deployado em ambiente seguro com auth proxy

### Weights & Biases
- **Colaboração é core strength**
- Hosted platform: UI web compartilhável
- Projects podem ser private ou public
- **Reports**: Dashboards narrativos compartilháveis
- Alerts e notificações (Slack integration)
- Visualizations: charts, parallel coordinates, embedding projector, confusion matrices

### ZenML
- Colaboração via **reproducibility**
- Pipelines codificadas em formato padrão
- Qualquer membro pode rodar mesmo pipeline
- 50+ plugins para diferentes ferramentas
- RBAC (Role-Based Access Control) em ZenML Pro
- Built-in artifact visualization

---

## 🔌 Integration Capabilities

### MLflow
- Library-agnostic: Python, R, Java, REST
- Auto-logging: TensorFlow, Keras, PyTorch, XGBoost, LightGBM, Scikit-learn
- Deploy: AWS SageMaker, Azure ML, Docker

### Weights & Biases
- SDKs: Python, JavaScript
- Integrations com ML frameworks
- Launch para Kubernetes, SageMaker, etc.

### ZenML
- **50+ integrations**
- Orchestrators: Airflow, Kubeflow, Vertex AI, local
- Experiment trackers: MLflow, W&B
- Model deployers: MLflow, Seldon, KServe
- Artifact stores: S3, GCS, Azure, local

---

## 💡 Insights Principais

1. **MLflow**: Open-source, flexível, bom para quem quer controle
2. **W&B**: Hosted, polido, melhor visualização e colaboração
3. **ZenML**: Orchestration-focused, integra com ambos
4. **Combinável**: Usar ZenML + MLflow ou ZenML + W&B
5. **Pipeline-first**: ZenML é único em orquestração de pipelines ML

---

## 📊 Matriz de Decisão

| Precisa de... | Escolha |
|---------------|---------|
| Experiment tracking básico | MLflow |
| Rich visualization + collaboration | W&B |
| Pipeline orchestration | ZenML |
| End-to-end MLOps | ZenML + MLflow/W&B |
| Turnkey model registry | MLflow |
| Pipeline lineage | ZenML |

---

## 📝 Tags

`#mlflow` `#wandb` `#zenml` `#experiment-tracking` `#pipeline-orchestration` `#comparison` `#mlops-tools`