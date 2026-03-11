# MLflow Python API - Fluent API Reference - Resumo

**Fonte:** https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

O módulo `mlflow` fornece uma API "fluent" de alto nível para gerenciar runs de ML. Não é thread-safe - callers concorrentes devem implementar exclusão mútua manual.

---

## Classes Principais

### ActiveRun
Wrapper para `mlflow.entities.Run` para usar com context manager:

```python
with mlflow.start_run() as run:
    mlflow.log_param("my", "param")
    mlflow.log_metric("score", 100)
```

### ActiveModel (MLflow 3)
Wrapper para `mlflow.entities.LoggedModel` para gerenciar modelos logados independentemente de runs.

### Image
Classe para handling de imagens:

```python
import mlflow
import numpy as np

image = np.zeros((100, 100, 3), dtype=np.uint8)
image_obj = mlflow.Image(image)

# Métodos
image_obj.resize((50, 50))
image_obj.to_array()
image_obj.to_list()
image_obj.to_pil()
image_obj.save("image.png")
```

### MlflowException
Exceção genérica para operações MLflow:

```python
try:
    mlflow.get_run("invalid_id")
except mlflow.MlflowException as e:
    print(f"Error: {e.message}")
    print(f"HTTP Status: {e.get_http_status_code()}")
```

---

## Setup Functions

### set_tracking_uri()
```python
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_tracking_uri("postgresql://user:pass@host/db")
```

### get_tracking_uri()
```python
uri = mlflow.get_tracking_uri()  # Retorna URI atual
```

### set_experiment()
```python
mlflow.set_experiment("my-experiment")
```

### create_experiment()
```python
experiment_id = mlflow.create_experiment(
    "Social NLP Experiments",
    artifact_location="s3://bucket/experiments/",
    tags={"version": "v1", "priority": "P1"}
)
```

### get_experiment() / get_experiment_by_name()
```python
experiment = mlflow.get_experiment("0")
experiment = mlflow.get_experiment_by_name("Default")

print(f"Name: {experiment.name}")
print(f"Artifact Location: {experiment.artifact_location}")
print(f"Lifecycle_stage: {experiment.lifecycle_stage}")
```

---

## Run Management Functions

### start_run()
```python
# Básico
with mlflow.start_run():
    mlflow.log_param("p", 0)

# Com parâmetros
with mlflow.start_run(
    run_name="my-run",
    experiment_id="1",
    description="Training run",
    tags={"team": "ml"},
    log_system_metrics=True
) as run:
    print(f"Run ID: {run.info.run_id}")
```

### end_run()
```python
mlflow.end_run(status="FINISHED")  # FINISHED, FAILED, KILLED
```

### active_run() / last_active_run()
```python
run = mlflow.active_run()  # Run ativo no momento
last_run = mlflow.last_active_run()  # Último run completado
```

### get_run()
```python
run = mlflow.get_run(run_id)
print(f"Status: {run.info.status}")
print(f"Params: {run.data.params}")
print(f"Metrics: {run.data.metrics}")
```

### get_parent_run()
```python
# Para nested runs
parent_run = mlflow.get_parent_run(child_run_id)
```

### delete_run()
```python
mlflow.delete_run(run_id)
# Run fica em lifecycle_stage: deleted
```

---

## Autologging Function

### autolog()
```python
mlflow.autolog(
    log_input_examples=False,       # Logar exemplos de input
    log_model_signatures=True,       # Logar assinaturas do modelo
    log_models=True,                 # Logar modelos treinados
    log_datasets=True,               # Logar info de datasets
    log_traces=True,                 # Logar traces
    disable=False,                   # Desabilitar autologging
    exclusive=False,                 # Não logar em runs do usuário
    silent=False,                    # Suprimir logs
    extra_tags={"team": "ml"},       # Tags adicionais
    exclude_flavors=["tensorflow"]   # Excluir flavors
)
```

**Bibliotecas suportadas:** sklearn, tensorflow, pytorch, xgboost, lightgbm, spark, etc.

---

## Data Logging Functions

### log_param() / log_params()
```python
# Parâmetro único
mlflow.log_param("learning_rate", 0.01)

# Múltiplos parâmetros
mlflow.log_params({
    "learning_rate": 0.01,
    "batch_size": 32,
    "epochs": 100
})
```

### log_metric() / log_metrics()
```python
# Métrica única
mlflow.log_metric("accuracy", 0.95)

# Com step
mlflow.log_metric("loss", 0.1, step=10)

# Com timestamp
mlflow.log_metric("latency", 50, timestamp=int(time.time() * 1000))

# Múltiplas métricas
mlflow.log_metrics({
    "train_loss": 0.1,
    "val_loss": 0.2,
    "accuracy": 0.95
}, step=epoch)
```

### log_input()
```python
import mlflow.data
import pandas as pd

df = pd.read_csv("data.csv")
dataset = mlflow.data.from_pandas(df, name="training-data", targets="label")

with mlflow.start_run():
    mlflow.log_input(dataset, context="training")
```

### set_tag() / set_tags()
```python
# Tag única
mlflow.set_tag("model_type", "CNN")

# Múltiplas tags
mlflow.set_tags({
    "model_family": "transformer",
    "dataset_version": "v2.1",
    "environment": "production"
})

# Notes (documentação)
mlflow.set_tag(
    "mlflow.note.content",
    "Baseline transformer model with attention dropout."
)
```

---

## Artifact Management Functions

### log_artifact() / log_artifacts()
```python
# Arquivo único
mlflow.log_artifact("model.pkl")
mlflow.log_artifact("confusion_matrix.png", artifact_path="plots")

# Diretório inteiro
mlflow.log_artifacts("./outputs/")
```

### get_artifact_uri()
```python
# URI do artifact root
uri = mlflow.get_artifact_uri()

# URI de artifact específico
uri = mlflow.get_artifact_uri("model/model.pkl")
```

---

## Model Management Functions (MLflow 3)

### initialize_logged_model()
```python
model = mlflow.initialize_logged_model(
    name="my_model",
    model_type="neural_network",
    tags={"architecture": "transformer"}
)
# Status: PENDING
```

### create_external_model()
```python
model = mlflow.create_external_model(
    name="chatbot_agent",
    model_type="agent",
    tags={"version": "v1.0"}
)
# Para modelos armazenados fora do MLflow
```

### finalize_logged_model()
```python
from mlflow.entities import LoggedModelStatus

mlflow.finalize_logged_model(model.model_id, LoggedModelStatus.READY)
mlflow.finalize_logged_model(model.model_id, LoggedModelStatus.FAILED)
```

### get_logged_model() / last_logged_model()
```python
model = mlflow.get_logged_model(model_id)
latest = mlflow.last_logged_model()
```

### search_logged_models()
```python
models = mlflow.search_logged_models(
    filter_string="tags.environment = 'production'",
    order_by=[{"field_name": "creation_time", "ascending": False}],
    max_results=10
)
```

### set_active_model() / get_active_model_id()
```python
mlflow.set_active_model(model_id=model.model_id)
model_id = mlflow.get_active_model_id()
mlflow.clear_active_model()
```

---

## Tracing Functions

### get_active_trace_id()
```python
@mlflow.trace
def my_function():
    trace_id = mlflow.get_active_trace_id()
    print(f"Trace ID: {trace_id}")
```

### set_trace_tag() / delete_trace_tag()
```python
mlflow.set_trace_tag(trace_id, "key", "value")
mlflow.delete_trace_tag(trace_id, "key")
```

---

## Search Functions

### search_runs()
```python
runs = mlflow.search_runs(
    experiment_ids=["1", "2"],
    filter_string="metrics.accuracy > 0.9",
    order_by=["metrics.accuracy DESC"],
    max_results=100
)
```

### search_experiments()
```python
experiments = mlflow.search_experiments(
    filter_string="tags.project = 'my-project'"
)
```

---

## Model Evaluation

### evaluate()
```python
result = mlflow.evaluate(
    model="models:/my_model/1",
    data=test_df,
    targets="label",
    model_type="classifier",
    evaluators="default"
)

print(result.metrics)
```

**Model Types Suportados:**
- `classifier` - Classificação
- `regressor` - Regressão
- `question-answering` - QA
- `text-summarization` - Sumarização
- `text` - Texto genérico
- `retriever` - Retrieval

---

## System Metrics

### enable_system_metrics_logging() / disable_system_metrics_logging()
```python
# Habilitar globalmente
mlflow.enable_system_metrics_logging()

# Desabilitar globalmente
mlflow.disable_system_metrics_logging()

# Por run
with mlflow.start_run(log_system_metrics=True):
    ...
```

---

## Utility Functions

### doctor()
```python
mlflow.doctor(mask_envs=True)  # Mascara variáveis sensíveis
```

Output: system info, Python version, MLflow version, dependencies, tracking URI.

### flush_async_logging()
```python
mlflow.flush_async_logging()  # Flush all pending async logging
mlflow.flush_artifact_async_logging()  # Flush artifact logging
mlflow.flush_trace_async_logging()  # Flush trace logging
```

---

## Quick Reference

```python
import mlflow

# Setup
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-experiment")

# Autologging
mlflow.autolog()

# Run básico
with mlflow.start_run():
    mlflow.log_params({"lr": 0.01, "epochs": 100})
    mlflow.log_metric("accuracy", 0.95, step=10)
    mlflow.sklearn.log_model(model, "model")

# Search
runs = mlflow.search_runs(filter_string="metrics.accuracy > 0.9")

# Evaluate
result = mlflow.evaluate(model, data, targets="label", model_type="classifier")

# Doctor
mlflow.doctor()
```

---

## Conceitos Aprendidos

1. **Fluent API** - API de alto nível para gerenciar runs
2. **ActiveRun/ActiveModel** - Wrappers para context managers
3. **Autologging** - Logging automático com configurações
4. **Logged Models (MLflow 3)** - Gerenciamento independente de modelos
5. **System Metrics** - Logging de métricas de sistema (CPU, GPU, etc.)
6. **Search API** - Busca avançada de runs e experimentos
7. **Evaluate** - Avaliação de modelos com métricas automáticas
8. **Tracing** - Rastreamento de execuções GenAI
9. **Doctor** - Debug info para troubleshooting
10. **Async Logging** - Flush para logging assíncrono