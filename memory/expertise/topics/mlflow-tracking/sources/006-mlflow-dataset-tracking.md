# MLflow Dataset Tracking - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/dataset/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é Dataset Tracking

Solução para gerenciar datasets ao longo do ciclo de vida de ML. Permite:
- Track, version, manage datasets
- Lineage completo de raw data → model predictions
- Reprodutibilidade

---

## Por que Dataset Tracking?

1. **Data Lineage** - Journey completa raw data → model inputs
2. **Reproducibility** - Experiments com datasets idênticos
3. **Version Control** - Gerenciar versões de datasets
4. **Collaboration** - Compartilhar datasets e metadados
5. **Evaluation Integration** - Integração com mlflow.models.evaluate()
6. **Production Monitoring** - Track datasets em produção

---

## Core Components

### Dataset

Objeto de metadata com:
- **Name** - Identificador descritivo
- **Digest** - Hash único (computado automaticamente)
- **Source** - DatasetSource com lineage
- **Schema** - Schema opcional (MLflow Schema)
- **Profile** - Estatísticas opcionais (row count, column stats)

### Tipos Suportados

| Tipo | Para |
|------|------|
| PandasDataset | Pandas DataFrames |
| SparkDataset | Apache Spark DataFrames |
| NumpyDataset | NumPy arrays |
| PolarsDataset | Polars DataFrames |
| HuggingFaceDataset | Hugging Face datasets |
| TensorFlowDataset | TensorFlow datasets |
| MetaDataset | Metadata-only (sem armazenamento) |

### DatasetSource

Lineage para source original:
- File URL
- S3 bucket
- Database table
- Qualquer data source

---

## Quick Start

```python
import mlflow.data
import pandas as pd

# Load data
dataset_source_url = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-white.csv"
raw_data = pd.read_csv(dataset_source_url, delimiter=";")

# Create Dataset
dataset = mlflow.data.from_pandas(
    raw_data, 
    source=dataset_source_url, 
    name="wine-quality-white", 
    targets="quality"
)

# Log to run
with mlflow.start_run():
    mlflow.log_input(dataset, context="training")
    # model = train_model(raw_data)
    # mlflow.sklearn.log_model(model, "model")
```

### Access Metadata
```python
print(f"Dataset name: {dataset.name}")
print(f"Dataset digest: {dataset.digest}")  # Hash único
print(f"Dataset source: {dataset.source}")
print(f"Dataset profile: {dataset.profile}")  # {"num_rows": 4898, ...}
print(f"Dataset schema: {dataset.schema}")
```

---

## Dataset Sources

```python
# Local file
local_dataset = mlflow.data.from_pandas(df, source="/path/to/local/file.csv", name="local-data")

# Cloud storage
s3_dataset = mlflow.data.from_pandas(df, source="s3://bucket/data.parquet", name="s3-data")

# Database
db_dataset = mlflow.data.from_pandas(df, source="postgresql://user:pass@host/db", name="db-data")

# URL
url_dataset = mlflow.data.from_pandas(df, source="https://example.com/data.csv", name="web-data")
```

---

## MLflow UI

Dataset aparece na UI com:
- Dataset name e digest
- Schema (column types)
- Profile statistics
- Source lineage
- Context de uso

---

## Integration with MLflow Evaluate

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Prepare data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Create evaluation dataset
eval_data = X_test.copy()
eval_data["target"] = y_test

eval_dataset = mlflow.data.from_pandas(eval_data, targets="target", name="evaluation-set")

with mlflow.start_run():
    mlflow.sklearn.log_model(model, name="model", input_example=X_test)
    
    # Evaluate using dataset
    result = mlflow.models.evaluate(
        model=f"runs:/{mlflow.active_run().info.run_id}/model",
        data=eval_dataset,
        model_type="classifier",
    )
    
    print(f"Accuracy: {result.metrics['accuracy_score']:.3f}")
```

---

## Advanced: Dataset Versioning

```python
def create_versioned_dataset(data, version, base_name="customer-data"):
    dataset = mlflow.data.from_pandas(
        data,
        source=f"data_pipeline_v{version}",
        name=f"{base_name}-v{version}",
        targets="target",
    )
    
    with mlflow.start_run(run_name=f"Dataset_Version_{version}"):
        mlflow.log_input(dataset, context="versioning")
        
        # Log version metadata
        mlflow.log_params({
            "dataset_version": version,
            "data_size": len(data),
            "features_count": len(data.columns) - 1,
        })
        
        # Log data quality metrics
        mlflow.log_metrics({
            "missing_values_pct": (data.isnull().sum().sum() / data.size) * 100,
            "duplicate_rows": data.duplicated().sum(),
        })
    
    return dataset

# Create versions
v1_dataset = create_versioned_dataset(data_v1, "1.0")
v2_dataset = create_versioned_dataset(data_v2, "2.0")
```

---

## Production: Batch Monitoring

```python
def monitor_batch_predictions(batch_data, model_version, date):
    batch_dataset = mlflow.data.from_pandas(
        batch_data,
        source=f"production_batch_{date}",
        name=f"batch_predictions_{date}",
        targets="true_label" if "true_label" in batch_data.columns else None,
        predictions="prediction" if "prediction" in batch_data.columns else None,
    )
    
    with mlflow.start_run(run_name=f"Batch_Monitor_{date}"):
        mlflow.log_input(batch_dataset, context="production_batch")
        
        mlflow.log_params({
            "batch_date": date,
            "model_version": model_version,
            "batch_size": len(batch_data),
        })
        
        # Monitor prediction distribution
        if "prediction" in batch_data.columns:
            mlflow.log_metrics({
                "prediction_mean": batch_data["prediction"].mean(),
                "prediction_std": batch_data["prediction"].std(),
            })
    
    return batch_dataset
```

---

## Best Practices

1. **Data Quality** - Validar antes de logar
2. **Naming Conventions** - Nomes consistentes com versão
3. **Source Documentation** - URLs identificáveis
4. **Context Specification** - Labels claros ("training", "validation", "evaluation", "production")
5. **Metadata Logging** - Incluir data collection, preprocessing
6. **Version Control** - Track versions explicitamente

---

## Digest Computation

| Dataset Type | Digest Based On |
|--------------|-----------------|
| Standard datasets | Data content + structure |
| MetaDataset | Metadata only (name, source, schema) |
| EvaluationDataset | Optimized hashing (sample rows) |

---

## Conceitos Aprendidos

1. **Dataset Object** - Metadata tracking com name, digest, source, schema, profile
2. **DatasetSource** - Lineage para source original
3. **Supported Types** - Pandas, Spark, NumPy, Polars, HuggingFace, TensorFlow
4. **log_input()** - API para logar datasets a runs
5. **Evaluation Integration** - mlflow.models.evaluate() usa datasets
6. **Versioning** - Track dataset versions explicitamente
7. **Production Monitoring** - Track datasets em batch predictions

---

## Key Benefits

- **Reproducibility** - Experiments com datasets idênticos
- **Lineage Tracking** - Source → model predictions
- **Collaboration** - Share datasets com metadata
- **Quality Assurance** - Capture data quality metrics