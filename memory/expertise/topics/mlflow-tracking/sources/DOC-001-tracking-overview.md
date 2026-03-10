# MLflow Tracking - Resumo da Documentação Oficial

**Fonte:** DOC-001 - MLflow Tracking Official  
**URL:** https://mlflow.org/docs/latest/ml/tracking/  
**Lido em:** 2026-03-10  
**Tempo de leitura:** ~15 min

---

## Conceitos Fundamentais

### Runs
- Execuções de código de ML (ex: `python train.py`)
- Cada run registra:
  - Metadata: métricas, parâmetros, timestamps
  - Artifacts: modelos, imagens, arquivos de saída

### Models
- Artefatos de ML treinados durante runs
- Possuem metadata e artifacts próprios
- Podem ser referenciados por `models:/<model_id>` (MLflow 3)

### Experiments
- Containers lógicos para agrupar runs
- Criados via CLI, API ou UI
- Organizam experimentos relacionados

---

## API de Tracking

### Logging Básico

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
    # código de treinamento...
    mlflow.log_metric("val_loss", val_loss)
```

### Autologging

```python
import mlflow
mlflow.autolog()  # Uma linha para logging automático!
# Seu código de treinamento funciona inalterado
model.fit(X_train, y_train)
```

**Bibliotecas suportadas:** Scikit-learn, XGBoost, PyTorch, Keras/TensorFlow, Spark, LightGBM

---

## Novidades do MLflow 3

### Model Search (`mlflow.search_logged_models()`)

```python
top_models = mlflow.search_logged_models(
    experiment_ids=["1", "2"],
    filter_string="metrics.accuracy > 0.95 AND params.model_type = 'RandomForest'",
    order_by=[{"field_name": "metrics.f1_score", "ascending": False}],
    max_results=5,
)
```

**Features:**
- Filtros SQL-like com prefixos `metrics.`, `params.`, `attribute`
- Dataset-aware search para comparação justa
- Ordenação flexível por múltiplos critérios
- Loading direto via `models:/<model_id>`

### Model Checkpoints

```python
for epoch in range(100):
    train_model(model, epoch)
    if epoch % 10 == 0:
        model_info = mlflow.pytorch.log_model(
            pytorch_model=model,
            name=f"checkpoint-epoch-{epoch}",
            step=epoch,
        )
        # Log métricas vinculadas ao modelo específico
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

# Log métrica com links para modelo e dataset
mlflow.log_metric(
    key="f1_score",
    value=0.95,
    step=epoch,
    model_id=model_info.model_id,
    dataset=train_dataset,
)
```

---

## Dataset Tracking

```python
mlflow.log_input(dataset)  # Registra dataset usado no treinamento
```

**Features:**
- Lineage de datasets
- Versioning
- Metadados (nome, digest, profile)

---

## Arquitetura de Tracking

### Componentes

1. **MLflow Tracking APIs** - Python, REST, R, Java
2. **Backend Store** - Persiste metadata (SQLite, PostgreSQL, MySQL)
3. **Artifact Store** - Persiste artefatos (local, S3, GCS, Azure Blob)
4. **Tracking Server** (opcional) - HTTP server com REST APIs

### Setups Comuns

| Cenário | Backend | Artifacts | Uso |
|---------|---------|-----------|-----|
| Localhost (default) | mlruns/ | mlruns/ | Solo dev |
| Local DB | SQLite/PostgreSQL | local | Solo dev com queries |
| Remote Server | PostgreSQL | S3/GCS | Team dev |

### Configuração de Tracking URI

```python
mlflow.set_tracking_uri("http://localhost:5000")
# ou
mlflow.set_tracking_uri("postgresql://user:pass@host/db")
```

---

## Tracking UI

```bash
mlflow server --port 5000
# Acesse http://127.0.0.1:5000
```

**Features:**
- Listagem e comparação de runs por experimento
- Busca por parâmetro ou métrica
- Visualização de métricas
- Download de artifacts e metadata

---

## Conceitos-Chave Extraídos

1. **Runs** = unidade básica de execução
2. **Experiments** = agrupamento lógico de runs
3. **Autologging** = integração automática com 15+ bibliotecas
4. **Backend Store** = banco para metadata (SQLite, PostgreSQL, MySQL)
5. **Artifact Store** = storage para arquivos grandes (S3, GCS, Azure)
6. **Tracking Server** = servidor HTTP para team collaboration
7. **Model URIs** = `models:/<model_id>` (MLflow 3) ou `models:/<name>/<version>`
8. **Dataset Tracking** = lineage de dados com `mlflow.log_input()`
9. **Model Checkpoints** = múltiplos modelos por run com step tracking
10. **Search Logged Models** = busca avançada de modelos com filtros SQL-like

---

## Padrões de Uso Recomendados

### Básico

```python
with mlflow.start_run():
    mlflow.log_params({"lr": 0.01, "batch_size": 32})
    for epoch in range(num_epochs):
        loss = train_epoch()
        mlflow.log_metric("loss", loss, step=epoch)
    mlflow.sklearn.log_model(model, "model")
```

### Com Autolog + Custom

```python
mlflow.autolog()
with mlflow.start_run():
    model.fit(X_train, y_train)
    # Custom metrics adicionais
    mlflow.log_metric("custom_score", custom_score)
    mlflow.log_artifact("feature_importance.csv")
```

### Nested Runs (Hiperparâmetros)

```python
with mlflow.start_run(run_name="hyperparameter_sweep") as parent:
    for lr in [0.001, 0.01, 0.1]:
        with mlflow.start_run(nested=True, run_name=f"lr_{lr}"):
            mlflow.log_param("learning_rate", lr)
            score = train_and_evaluate(lr)
            mlflow.log_metric("accuracy", score)
```

---

## Próximos Passos

1. Estudar Model Registry em detalhes (DOC-003 a DOC-005)
2. Explorar Autologging para bibliotecas específicas (DOC-008)
3. Praticar com tutoriais (TUT-001 a TUT-003)
4. Configurar Tracking Server local