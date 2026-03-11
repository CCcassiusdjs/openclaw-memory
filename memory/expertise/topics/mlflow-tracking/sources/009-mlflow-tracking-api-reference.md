# MLflow Tracking APIs - Resumo Completo

**Fonte:** https://mlflow.org/docs/latest/ml/tracking/tracking-api/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Dois Métodos de Tracking

### 🤖 Automatic Logging

```python
import mlflow
mlflow.autolog()  # Uma linha!

# Treinamento funciona normalmente
model.fit(X_train, y_train)  # MLflow loga automaticamente
```

**O que é logado:**
- Parâmetros e hiperparâmetros
- Métricas de treino e validação
- Model artifacts e checkpoints
- Plots e visualizações
- Metadata específica do framework

**Bibliotecas suportadas:** Scikit-learn, XGBoost, LightGBM, PyTorch, Keras/TensorFlow, Spark, Statsmodels, etc.

### 🛠️ Manual Logging

```python
with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("batch_size", 32)
    
    for epoch in range(num_epochs):
        train_loss = train_model()
        val_loss = validate_model()
        
        mlflow.log_metrics({"train_loss": train_loss, "val_loss": val_loss}, step=epoch)
    
    mlflow.sklearn.log_model(model, name="model")
```

---

## Core Logging Functions

### Setup & Configuration

| Função | Propósito | Exemplo |
|--------|-----------|---------|
| `set_tracking_uri()` | Conectar ao server | `mlflow.set_tracking_uri("http://localhost:5000")` |
| `get_tracking_uri()` | Obter URI atual | `uri = mlflow.get_tracking_uri()` |
| `create_experiment()` | Criar experimento | `exp_id = mlflow.create_experiment("my-exp")` |
| `set_experiment()` | Definir experimento ativo | `mlflow.set_experiment("fraud-detection")` |

### Run Management

| Função | Propósito | Exemplo |
|--------|-----------|---------|
| `start_run()` | Iniciar run (context manager) | `with mlflow.start_run(): ...` |
| `end_run()` | Finalizar run | `mlflow.end_run(status="FINISHED")` |
| `active_run()` | Run ativo atual | `run = mlflow.active_run()` |
| `last_active_run()` | Último run completado | `last_run = mlflow.last_active_run()` |

### Data Logging

| Função | Propósito | Exemplo |
|--------|-----------|---------|
| `log_param()` / `log_params()` | Log hiperparâmetros | `mlflow.log_param("lr", 0.01)` |
| `log_metric()` / `log_metrics()` | Log métricas | `mlflow.log_metric("accuracy", 0.95, step=10)` |
| `log_input()` | Log dataset info | `mlflow.log_input(dataset)` |
| `set_tag()` / `set_tags()` | Metadata tags | `mlflow.set_tag("model_type", "CNN")` |

### Artifact Management

| Função | Propósito | Exemplo |
|--------|-----------|---------|
| `log_artifact()` | Log arquivo único | `mlflow.log_artifact("model.pkl")` |
| `log_artifacts()` | Log diretório | `mlflow.log_artifacts("./plots/")` |
| `get_artifact_uri()` | URI do artifact | `uri = mlflow.get_artifact_uri()` |

---

## Model Management (MLflow 3)

### Creating and Managing Logged Models

```python
import mlflow

# Initialize model in PENDING state
model = mlflow.initialize_logged_model(
    name="custom_neural_network",
    model_type="neural_network",
    tags={"architecture": "transformer"}
)

try:
    # Train and save
    train_model()
    mlflow.pytorch.log_model(
        pytorch_model=model_instance,
        name="model",
        model_id=model.model_id,  # Link ao logged model
    )
    
    # Finalize as READY
    mlflow.finalize_logged_model(model.model_id, "READY")
except Exception:
    mlflow.finalize_logged_model(model.model_id, "FAILED")
```

### External Models

```python
# Modelos armazenados fora do MLflow
model = mlflow.create_external_model(
    name="chatbot_agent",
    model_type="agent",
    tags={"version": "v1.0", "environment": "production"}
)

# Log parameters específicos
mlflow.log_model_params({"temperature": "0.7"}, model_id=model.model_id)

# Set as active model for trace linking
mlflow.set_active_model(model_id=model.model_id)

@mlflow.trace
def chat_with_agent(message):
    return agent.chat(message)

# Traces linkados ao modelo externo
traces = mlflow.search_traces(model_id=model.model_id)
```

### Searching Logged Models

```python
# Buscar modelos por tags
production_models = mlflow.search_logged_models(
    filter_string="tags.environment = 'production' AND model_type = 'transformer'",
    order_by=[{"field_name": "creation_time", "ascending": False}]
)

# Buscar por métricas
high_accuracy_models = mlflow.search_logged_models(
    filter_string="metrics.accuracy > 0.95",
    datasets=[{"dataset_name": "test_set"}],
    max_results=10
)

# Último modelo logado
latest_model = mlflow.last_logged_model()
```

---

## Precise Metric Tracking

```python
import time

# Log com step (epoch/iteration)
for epoch in range(100):
    loss = train_epoch()
    mlflow.log_metric("train_loss", loss, step=epoch)

# Log com timestamp customizado
now = int(time.time() * 1000)  # MLflow expects milliseconds
mlflow.log_metric("inference_latency", latency, timestamp=now)

# Log com step e timestamp
mlflow.log_metric("gpu_utilization", gpu_usage, step=epoch, timestamp=now)
```

**Step Requirements:**
- Deve ser inteiro 64-bit
- Pode ser negativo ou out of order
- Suporta gaps (1, 5, 75, -20)

---

## Hierarchical Runs (Parent/Child)

```python
# Parent run
with mlflow.start_run(run_name="hyperparameter_sweep") as parent:
    mlflow.log_param("search_strategy", "random")
    
    best_score = 0
    
    for lr in [0.001, 0.01, 0.1]:
        for batch_size in [16, 32, 64]:
            # Child run
            with mlflow.start_run(nested=True, run_name=f"lr_{lr}_bs_{batch_size}") as child:
                mlflow.log_params({"learning_rate": lr, "batch_size": batch_size})
                
                model = train_model(lr, batch_size)
                score = evaluate_model(model)
                mlflow.log_metric("accuracy", score)
                
                if score > best_score:
                    best_score = score
    
    mlflow.log_metric("best_accuracy", best_score)

# Query child runs
child_runs = mlflow.search_runs(
    filter_string=f"tags.mlflow.parentRunId = '{parent.info.run_id}'"
)
```

---

## System Tags Reference

| Tag | Descrição | Quando é setado |
|-----|-----------|-----------------|
| `mlflow.source.name` | Arquivo/notebook fonte | Sempre |
| `mlflow.source.type` | Tipo (NOTEBOOK, JOB, LOCAL) | Sempre |
| `mlflow.user` | Usuário que criou | Sempre |
| `mlflow.source.git.commit` | Git commit hash | Quando em git repo |
| `mlflow.source.git.branch` | Git branch | MLflow Projects |
| `mlflow.parentRunId` | Parent run ID | Child runs |
| `mlflow.docker.image.name` | Docker image | Docker environments |
| `mlflow.note.content` | Descrição editável | Manual |

---

## Smart Tagging

```python
with mlflow.start_run():
    # Tags para filtering
    mlflow.set_tags({
        "model_family": "transformer",
        "dataset_version": "v2.1",
        "environment": "production",
        "team": "nlp-research",
    })
    
    # Notes para documentação
    mlflow.set_tag(
        "mlflow.note.content",
        "Baseline transformer model with attention dropout."
    )

# Buscar por tags
transformer_runs = mlflow.search_runs(
    filter_string="tags.model_family = 'transformer'"
)
```

---

## Integration with Auto Logging

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

mlflow.autolog()

with mlflow.start_run():
    # Auto logging captura treinamento
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Adicionar métricas customizadas
    predictions = model.predict(X_test)
    report = classification_report(y_test, predictions, output_dict=True)
    
    mlflow.log_metrics({
        "precision_macro": report["macro avg"]["precision"],
        "recall_macro": report["macro avg"]["recall"],
        "f1_macro": report["macro avg"]["f1-score"],
    })
    
    # Artifact customizado
    feature_importance.to_csv("feature_importance.csv")
    mlflow.log_artifact("feature_importance.csv")
```

---

## Language API Coverage

| Capability | Python | Java | R | REST |
|------------|--------|------|---|------|
| Basic Logging | ✅ Full | ✅ Full | ✅ Full | ✅ Full |
| Auto Logging | ✅ 15+ libs | ❌ | ✅ Limited | ❌ |
| Model Logging | ✅ 20+ flavors | ✅ Basic | ✅ Basic | ✅ Via artifacts |
| Logged Model Mgmt | ✅ Full (MLflow 3) | ❌ | ❌ | ✅ Basic |
| Dataset Tracking | ✅ Full | ✅ Basic | ✅ Basic | ✅ Basic |

---

## Conceitos Aprendidos

1. **Autologging** - Uma linha para logging completo
2. **Manual Logging** - Controle total com API granular
3. **Logged Models (MLflow 3)** - Gerenciamento independente de runs
4. **External Models** - Modelos fora do MLflow podem ser trackeados
5. **Parent/Child Runs** - Hierarquia para hyperparameter sweeps
6. **System Tags** - Tags automáticas para contexto de execução
7. **Smart Tagging** - Organização estratégica de experimentos
8. **Precise Metrics** - Step e timestamp customizados

---

## Quick Reference

```python
# Setup
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-experiment")

# Autologging
mlflow.autolog()

# Manual run
with mlflow.start_run():
    mlflow.log_params({"lr": 0.01, "epochs": 100})
    mlflow.log_metric("accuracy", 0.95, step=10)
    mlflow.sklearn.log_model(model, "model")

# Nested runs
with mlflow.start_run(run_name="parent"):
    with mlflow.start_run(nested=True):
        ...

# Query
runs = mlflow.search_runs(filter_string="metrics.accuracy > 0.9")
```