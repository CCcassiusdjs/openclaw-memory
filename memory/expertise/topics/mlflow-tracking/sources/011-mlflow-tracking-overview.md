# MLflow Tracking Overview - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/tracking/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é MLflow Tracking

API e UI para logging de parâmetros, versões de código, métricas e arquivos de saída durante execuções de ML. Disponível em Python, REST, R e Java.

---

## Conceitos Principais

### Runs

Execuções de código de data science. Cada run registra:
- **Metadata** - Métricas, parâmetros, timestamps
- **Artifacts** - Model weights, imagens, arquivos de saída

### Models

Artefatos de ML treinados produzidos durante runs. Logged Models têm sua própria metadata e artifacts.

### Experiments

Grupos de runs e models para uma tarefa específica.

---

## Tracking Runs

### Manual Logging

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    mlflow.log_metric("val_loss", val_loss)
```

### Auto-logging

```python
import mlflow

mlflow.autolog()  # Uma linha!

# Seu código de treinamento...
model.fit(X_train, y_train)  # MLflow loga automaticamente
```

**Bibliotecas suportadas:** Scikit-learn, XGBoost, PyTorch, Keras, Spark, etc.

---

## Tracking Models (MLflow 3)

### Logging Model Checkpoints

```python
import mlflow
import mlflow.pytorch

with mlflow.start_run() as run:
    for epoch in range(100):
        train_model(model, epoch)
        
        # Log checkpoint a cada 10 epochs
        if epoch % 10 == 0:
            model_info = mlflow.pytorch.log_model(
                pytorch_model=model,
                name=f"checkpoint-epoch-{epoch}",
                step=epoch,
                input_example=sample_input,
            )
            
            # Log métrica linkada ao checkpoint
            accuracy = evaluate_model(model, validation_data)
            mlflow.log_metric(
                key="accuracy",
                value=accuracy,
                step=epoch,
                model_id=model_info.model_id,
                dataset=validation_dataset,
            )
```

### Linking Metrics to Models and Datasets

```python
# Criar referência de dataset
train_dataset = mlflow.data.from_pandas(train_df, name="training_data")

# Log métrica com links
mlflow.log_metric(
    key="f1_score",
    value=0.95,
    step=epoch,
    model_id=model_info.model_id,  # Link para model checkpoint
    dataset=train_dataset,          # Link para dataset
)
```

### Searching Logged Models

```python
# Buscar modelos por performance
top_models = mlflow.search_logged_models(
    experiment_ids=["1", "2"],
    filter_string="metrics.accuracy > 0.95 AND params.model_type = 'RandomForest'",
    order_by=[{"field_name": "metrics.f1_score", "ascending": False}],
    max_results=5,
)

# Melhor modelo para deploy
best_model = mlflow.search_logged_models(
    experiment_ids=["1"],
    filter_string="metrics.accuracy > 0.9",
    max_results=1,
    order_by=[{"field_name": "metrics.accuracy", "ascending": False}],
    output_format="list",
)[0]

# Carregar modelo
loaded_model = mlflow.pyfunc.load_model(f"models:/{best_model.model_id}")
```

---

## Model URIs in MLflow 3

```python
# Novo formato MLflow 3
model_uri = f"models:/{model_info.model_id}"
loaded_model = mlflow.pyfunc.load_model(model_uri)

# Formato antigo (ainda suportado)
# model_uri = f"runs:/{run_id}/model_path"
```

**Vantagens do novo formato:**
- Direct model reference - Não precisa saber run ID
- Better lifecycle management - ID único por checkpoint
- Improved comparison - Comparar checkpoints do mesmo run
- Enhanced traceability - Links claros entre models, métricas, datasets

---

## Tracking Datasets

```python
import mlflow.data
import pandas as pd

df = pd.read_csv("data.csv")
dataset = mlflow.data.from_pandas(df, name="training-data", targets="label")

with mlflow.start_run():
    mlflow.log_input(dataset, context="training")
```

---

## Tracking UI

Interface visual para explorar experiments, runs e models:
- Experiment-based run listing e comparison
- Busca de runs por parâmetro ou métrica
- Visualização de métricas
- Download de artifacts

**Iniciar UI:**
```bash
mlflow server --port 5000
# Acessar http://127.0.0.1:5000
```

---

## Environment Setup

### Components

| Component | Descrição |
|-----------|-----------|
| **Tracking APIs** | Python, REST, R, Java APIs para logging |
| **Backend Store** | Persiste metadata (run ID, params, metrics) |
| **Artifact Store** | Persiste artifacts (model weights, images) |
| **Tracking Server** | HTTP server para REST APIs (opcional) |

### Common Setups

| Scenario | Use Case | Descrição |
|----------|----------|-----------|
| **Localhost** | Solo development | Local mlruns directory |
| **Local Database** | Solo development | SQLAlchemy database (SQLite, PostgreSQL) |
| **Remote Tracking** | Team development | Tracking Server com artifact proxy |

---

## Setup Examples

### Localhost (Default)

```python
# Sem configuração - logs para ./mlruns
import mlflow

with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
```

### Local Database

```python
import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")

with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
```

### Remote Tracking Server

```python
import mlflow

mlflow.set_tracking_uri("http://<tracking-server>:5000")

with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
```

---

## Querying Runs Programmatically

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Buscar melhor run por métrica
best_run = client.search_runs(
    experiment_ids=["0"],
    order_by=["metrics.val_loss ASC"],
    max_results=1
)[0]

print(best_run.info)
# {'run_id': '...', 'metrics': {'val_loss': 0.123}, ...}
```

---

## FAQ

### Múltiplos Runs em Paralelo?

Sim, MLflow suporta multiprocessing/threading.

### Organizar Runs?

- **Experiments** - Containers lógicos para runs
- **Child runs** - Agrupar runs sob parent
- **Tags** - Filtrar e buscar runs por metadata

### Acesso Direto a Remote Storage?

Sim, sem Tracking Server:
```python
mlflow.create_experiment(
    "my-experiment",
    artifact_location="s3://my-bucket/"
)
```

### Integrar com Model Registry?

Usar database-backed store (PostgreSQL) e log_model methods.

### Adicionar Descrição ao Run?

```python
mlflow.set_tag(
    "mlflow.note.content",
    "Descrição detalhada do run..."
)
```

---

## Conceitos Aprendidos

1. **Runs** - Execuções de código ML
2. **Models** - Artefatos treinados
3. **Experiments** - Grupos de runs
4. **Auto-logging** - Logging automático
5. **Model Checkpoints** - Múltiplos checkpoints por run
6. **Metric Links** - Links entre métricas, models, datasets
7. **Model URIs** - Formato `models:/<model_id>` (MLflow 3)
8. **Backend Store** - Persistência de metadata
9. **Artifact Store** - Persistência de artifacts
10. **Tracking Server** - HTTP server para REST APIs

---

## Key Points

- **Default:** Local mlruns directory
- **Team:** Use Tracking Server + database backend
- **MLflow 3:** Novo model URI format (`models:/<model_id>`)
- **Search:** `mlflow.search_logged_models()` para buscar modelos
- **Links:** Métricas podem ser linkadas a models e datasets