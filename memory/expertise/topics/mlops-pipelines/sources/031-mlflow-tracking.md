# MLflow Tracking - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/tracking/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 O que é MLflow Tracking?

API e UI para **logging parameters, code versions, metrics, output files** quando rodando ML code, com visualização posterior.

APIs disponíveis: Python, REST, R, Java

## 📋 Core Concepts

### Runs
- Execução de data science code
- Exemplo: único `python train.py`
- Registra: metadata (metrics, params, timestamps), artifacts (model weights, images)

### Models
- Trained ML artifacts produzidos durante runs
- Metadata + artifacts similares a runs

### Experiments
- Agrupa runs e models para uma task específica
- Criar via CLI, API, UI

## 🚀 Quick Start

### Manual Logging
```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    # Your ml code
    mlflow.log_metric("val_loss", val_loss)
```

### Auto-logging
```python
import mlflow

mlflow.autolog()

# Your training code...
```

**Supported libraries:** Scikit-learn, XGBoost, PyTorch, Keras, Spark, more

## 🔍 Search Logged Models (MLflow 3)

```python
import mlflow

# Find high-performing models
top_models = mlflow.search_logged_models(
    experiment_ids=["1", "2"],
    filter_string="metrics.accuracy > 0.95 AND params.model_type = 'RandomForest'",
    order_by=[{"field_name": "metrics.f1_score", "ascending": False}],
    max_results=5,
)

# Get best model for deployment
best_model = mlflow.search_logged_models(
    experiment_ids=["1"],
    filter_string="metrics.accuracy > 0.9",
    max_results=1,
    order_by=[{"field_name": "metrics.accuracy", "ascending": False}],
)[0]

# Load directly
loaded_model = mlflow.pyfunc.load_model(f"models:/{best_model.model_id}")
```

### Key Features
| Feature | Descrição |
|---------|-----------|
| **SQL-like filtering** | metrics., params., attribute prefixes |
| **Dataset-aware search** | Filter por dataset específico |
| **Flexible ordering** | Sort por múltiplos critérios |
| **Direct loading** | models:/ URI format |

## 📊 Model Checkpoints

```python
import mlflow
import mlflow.pytorch

with mlflow.start_run() as run:
    for epoch in range(100):
        train_model(model, epoch)

        # Log checkpoint every 10 epochs
        if epoch % 10 == 0:
            model_info = mlflow.pytorch.log_model(
                pytorch_model=model,
                name=f"checkpoint-epoch-{epoch}",
                step=epoch,
                input_example=sample_input,
            )

            # Log metrics linked to checkpoint
            accuracy = evaluate_model(model, validation_data)
            mlflow.log_metric(
                key="accuracy",
                value=accuracy,
                step=epoch,
                model_id=model_info.model_id,
            )
```

## 🔧 Querying Runs Programmatically

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
experiment_id = "0"
best_run = client.search_runs(
    experiment_id, order_by=["metrics.val_loss ASC"], max_results=1
)[0]
print(best_run.info)
```

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Run** | Execução única de código ML |
| **Experiment** | Grupo de runs |
| **Logged Model** | Modelo salvo com metadata |
| **Checkpoint** | Snapshot do modelo em um step |
| **Auto-logging** | Logging automático de params/metrics |

## 🔗 Referências Cruzadas

- Complementa: MLflow Model Registry (016-020)
- Relacionado a: W&B Tracking (033), Neptune (034)
- Pré-requisito para: MLflow Projects (032)

---

**Conceitos aprendidos:** 12
**Relevância:** Alta (core MLflow functionality)