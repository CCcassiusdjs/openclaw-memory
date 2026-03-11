# MLflow Production Guide - Scaling e Best Practices

**Fonte:** GUIDE-002 - MLflow Production Guide: Experiment Tracking, Model Registry, and Scalable MLOps Workflow  
**URL:** https://www.youngju.dev/blog/ai-platform/2026-03-07-ai-platform-mlflow-experiment-tracking-model-registry.en  
**Tipo:** Blog/Guia Avançado  
**Data:** Março 2026  
**Status:** completed

---

## Resumo

Guia production-grade para MLflow: scaling tracking server com PostgreSQL e S3, estruturando experiments para multi-team, model registry lifecycle com aliases, CI/CD integration com GitHub Actions, e failure modes.

---

## Platform Comparison

| Feature | MLflow | W&B | Neptune | ClearML |
|---------|--------|-----|---------|---------|
| License | Apache 2.0 (OSS) | Proprietary | Proprietary | Apache 2.0 |
| Self-hosted | Full | Limited | Limited | Full |
| Model Registry | Built-in | Built-in | Metadata-only | Built-in |
| Hyperparameter Sweeps | Manual/Optuna | Built-in | Via integrations | Built-in |
| Pricing (Team) | Free (self-hosted) | ~$50/user/mo | ~$79/user/mo | Free |

MLflow wins: self-hosting flexibility, vendor independence

---

## Architecture Overview

Production MLflow separa 3 concerns:

1. **Tracking Server** - API e UI process
2. **Backend Store** - PostgreSQL para metadata (params, metrics, tags)
3. **Artifact Store** - S3 para models, plots, large binaries

### Docker Compose Production

```yaml
services:
  mlflow-server:
    image: ghcr.io/mlflow/mlflow:v2.20.0
    ports: ['5000:5000']
    environment:
      MLFLOW_BACKEND_STORE_URI: 'postgresql://...'
      MLFLOW_DEFAULT_ARTIFACT_ROOT: 's3://mlflow-artifacts-prod/'
    command: >
      mlflow server
      --backend-store-uri postgresql://...
      --default-artifact-root s3://mlflow-artifacts-prod/
      --workers 4
      --app-name basic-auth
```

**SECURITY WARNING**: Never expose MLflow directly to internet without auth. Use Nginx reverse proxy with TLS.

---

## PostgreSQL Tuning for MLflow

MLflow workload: write-heavy during training, read-heavy during analysis.

```sql
-- postgresql.conf for MLflow (8GB RAM dedicated)
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 64MB
maintenance_work_mem = 512MB

-- Write-heavy optimizations
wal_buffers = 64MB
checkpoint_completion_target = 0.9
max_wal_size = 4GB

-- Connection pooling (PgBouncer for 50+ jobs)
max_connections = 200
```

**OPERATIONAL WARNING**: >50 concurrent training jobs logging frequently → connection pool exhaustion. Deploy PgBouncer in transaction mode.

---

## Experiment Tracking Best Practices

### Naming Convention

```python
# team/project/experiment-type
EXPERIMENT_NAME = "recommendation-team/product-ranking/hyperparameter-search"
```

### Production-Grade Run

```python
import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("https://mlflow.internal.company.com")
mlflow.set_experiment("recommendation-team/product-ranking/hyperparameter-search")

def train_model(config: dict):
    with mlflow.start_run(
        run_name=f"xgb-{config['max_depth']}d-{config['learning_rate']}lr",
        tags={
            "team": "recommendation",
            "project": "product-ranking",
            "environment": "staging",
            "git_commit": config.get("git_sha", "unknown"),
            "data_version": config.get("data_version", "v1"),
        },
    ) as run:
        # Log all hyperparameters
        mlflow.log_params({...})
        
        # Log dataset info
        dataset = mlflow.data.from_pandas(config["train_df"], source=config["data_path"])
        mlflow.log_input(dataset, context="training")
        
        # Log metrics at each evaluation point
        for epoch, metrics in enumerate(model.eval_history):
            mlflow.log_metrics(metrics, step=epoch)
        
        # Log final metrics
        mlflow.log_metrics(final_metrics)
        
        # Log model with signature
        signature = mlflow.models.infer_signature(config["sample_input"], model.predict(...))
        mlflow.xgboost.log_model(model, artifact_path="model", signature=signature,
            registered_model_name="product-ranking-xgb")
        
        # Log artifacts
        mlflow.log_artifact("feature_importance.png")
```

---

## Batch Metric Logging

**WARNING**: Calling `mlflow.log_metric()` every step creates separate HTTP request. For deep learning with thousands of steps, this saturates tracking server.

```python
def log_metrics_batched(metrics_buffer: list, batch_size: int = 100):
    if len(metrics_buffer) >= batch_size:
        with mlflow.start_run(run_id=current_run_id):
            for step, metrics in metrics_buffer:
                mlflow.log_metrics(metrics, step=step)
        metrics_buffer.clear()

# Usage: accumulate metrics, flush every 100 steps
metrics_buffer = []
for step in range(100000):
    loss = train_step()
    metrics_buffer.append((step, {"train_loss": loss}))
    log_metrics_batched(metrics_buffer, batch_size=100)
```

**Impact**: 50-100x reduction in tracking server load for long training runs.

---

## Model Registry Lifecycle (Aliases)

### Post-Stages Deprecation (MLflow 2.9+)

Legacy stages (Staging, Production, Archived) deprecated → use aliases.

```python
from mlflow.tracking import MlflowClient
client = MlflowClient()

# Register new version
result = client.create_model_version(
    name="product-ranking-xgb",
    source="s3://mlflow-artifacts-prod/3/abc123/artifacts/model",
    run_id="abc123",
    description="XGBoost v2 with new user features, NDCG@10 improved 3.2%",
)

# Set aliases for deployment workflow
client.set_registered_model_alias(
    name="product-ranking-xgb",
    alias="champion",  # currently serving production traffic
    version=result.version,
)

client.set_registered_model_alias(
    name="product-ranking-xgb",
    alias="challenger",  # candidate in shadow mode
    version=result.version + 1,
)

# Load by alias in serving code
champion_model = mlflow.pyfunc.load_model("models:/product-ranking-xgb@champion")
```

---

## Concepts Adicionados

- PostgreSQL tuning for MLflow workloads
- PgBouncer for connection pooling (>50 concurrent jobs)
- Batch metric logging pattern (50-100x load reduction)
- Model aliases vs deprecated stages
- Champion/Challenger deployment workflow
- Team/project/experiment naming convention
- Production architecture (tracking server + backend + artifact store)
- git_commit and data_version tags

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 30 min