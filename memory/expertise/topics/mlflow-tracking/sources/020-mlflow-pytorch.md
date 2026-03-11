# MLflow PyTorch Integration - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/deep-learning/pytorch/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

MLflow + PyTorch = Experiment tracking, model versioning e deployment para deep learning.

---

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Autologging** | Uma linha: `mlflow.pytorch.autolog()` |
| **Experiment Tracking** | Métricas, hiperparâmetros, arquiteturas |
| **Model Registry** | Versionamento, staging, deployment |
| **Reproducibility** | Seeds, ambientes, model states |

---

## Autologging

```python
import mlflow
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Uma linha!
mlflow.pytorch.autolog()

# Seu código funciona igual
model = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

for epoch in range(10):
    for data, target in train_loader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
```

**O que é logado:**
- Training metrics (loss, accuracy)
- Model parameters
- Optimizer configuration
- Model checkpoints

---

## Manual Logging

```python
import mlflow
import torch.nn as nn

params = {"epochs": 5, "learning_rate": 1e-3, "batch_size": 64}

with mlflow.start_run():
    mlflow.log_params(params)
    
    model = NeuralNetwork()
    optimizer = optim.SGD(model.parameters(), lr=params["learning_rate"])
    
    for epoch in range(params["epochs"]):
        # Training
        train_loss, accuracy = train_epoch(model, optimizer, train_loader)
        
        # Log per epoch
        mlflow.log_metrics(
            {"train_loss": train_loss, "train_accuracy": accuracy},
            step=epoch
        )
    
    # Log final model
    mlflow.pytorch.log_model(model, name="model")
```

---

## System Metrics Tracking

```python
# Habilitar system metrics
mlflow.enable_system_metrics_logging()

with mlflow.start_run():
    # Training loop - system metrics logged automatically
    for epoch in range(10):
        train_loss = train_epoch(model, train_loader)
        mlflow.log_metric("loss", train_loss, step=epoch)
```

**Métricas capturadas:**
- **GPU:** Utilization, memory, temperature, power
- **CPU:** Utilization, memory
- **Disk I/O:** Read/write throughput
- **Network I/O:** Traffic statistics

---

## Model Signatures

```python
import mlflow
import torch
from mlflow.models import infer_signature

model = nn.Sequential(nn.Linear(10, 50), nn.ReLU(), nn.Linear(50, 1))

# Sample input/output
input_example = torch.randn(1, 10)
predictions = model(input_example)

# Infer signature
signature = infer_signature(
    input_example.numpy(),
    predictions.detach().numpy()
)

with mlflow.start_run():
    mlflow.pytorch.log_model(
        model,
        name="pytorch_model",
        signature=signature,
        input_example=input_example.numpy(),
    )
```

---

## Checkpoint Tracking (MLflow 3)

```python
with mlflow.start_run() as run:
    mlflow.log_params({"n_layers": 3, "activation": "ReLU"})
    
    for epoch in range(101):
        # Training
        train(model, train_loader)
        
        # Log checkpoint every 10 epochs
        if epoch % 10 == 0:
            model_info = mlflow.pytorch.log_model(
                pytorch_model=model,
                name=f"checkpoint-{epoch}",
                step=epoch,
                input_example=X_train[:5].numpy(),
            )
            
            # Link metrics to checkpoint
            accuracy = compute_accuracy(model, X_train, y_train)
            mlflow.log_metric(
                key="train_accuracy",
                value=accuracy,
                step=epoch,
                model_id=model_info.model_id,
                dataset=train_dataset,
            )

# Search and rank checkpoints
ranked_checkpoints = mlflow.search_logged_models(
    filter_string=f"source_run_id='{run.info.run_id}'",
    order_by=[{"field_name": "metrics.train_accuracy", "ascending": False}],
)
```

---

## Model Loading

```python
# Load as PyTorch model
model_uri = "runs:/<run_id>/pytorch_model"
loaded_model = mlflow.pytorch.load_model(model_uri)
predictions = loaded_model(input_tensor)

# Load as PyFunc (generic)
pyfunc_model = mlflow.pyfunc.load_model(model_uri)
predictions = pyfunc_model.predict(input_array)
```

---

## Hyperparameter Optimization

```python
import mlflow
import optuna
import torch.nn as nn

def objective(trial):
    with mlflow.start_run(nested=True):
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-1, log=True),
            "hidden_size": trial.suggest_int("hidden_size", 32, 512),
            "dropout": trial.suggest_float("dropout", 0.1, 0.5),
        }
        
        mlflow.log_params(params)
        
        model = create_model(params)
        val_loss = train_and_evaluate(model, train_loader, val_loader)
        
        mlflow.log_metric("val_loss", val_loss)
        return val_loss

with mlflow.start_run(run_name="PyTorch HPO"):
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=50)
    
    mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items()})
    mlflow.log_metric("best_val_loss", study.best_value)
```

---

## Model Registry Integration

```python
from mlflow import MlflowClient

client = MlflowClient()

with mlflow.start_run():
    model = create_cnn_model()
    
    # Log model to registry
    model_info = mlflow.pytorch.log_model(
        model,
        name="pytorch_model",
        registered_model_name="ImageClassifier",
    )
    
    mlflow.set_tags({
        "model_type": "cnn",
        "dataset": "imagenet",
        "framework": "pytorch"
    })

# Set alias for production
client.set_registered_model_alias(
    name="ImageClassifier",
    alias="champion",
    version=model_info.registered_model_version,
)
```

---

## Distributed Training

```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def train_distributed():
    dist.init_process_group(backend="nccl")
    rank = dist.get_rank()
    
    model_ddp = DDP(model.to(rank), device_ids=[rank])
    
    # Only log from rank 0
    if rank == 0:
        mlflow.start_run()
        mlflow.log_params({"world_size": dist.get_world_size()})
    
    for epoch in range(epochs):
        train_loss = train_epoch(model_ddp, train_loader)
        
        if rank == 0:
            mlflow.log_metric("train_loss", train_loss, step=epoch)
    
    if rank == 0:
        mlflow.pytorch.log_model(model, name="distributed_model")
        mlflow.end_run()
```

---

## Quick Reference

```python
import mlflow
import torch.nn as nn

# Autologging
mlflow.pytorch.autolog()

# Manual logging
with mlflow.start_run():
    mlflow.log_params({"lr": 0.001, "epochs": 10})
    mlflow.log_metric("accuracy", accuracy, step=epoch)
    mlflow.pytorch.log_model(model, name="model")

# Checkpoints
model_info = mlflow.pytorch.log_model(model, name=f"checkpoint-{epoch}", step=epoch)
mlflow.log_metric("accuracy", accuracy, step=epoch, model_id=model_info.model_id)

# Load
loaded = mlflow.pytorch.load_model("runs:/<run_id>/model")

# Registry
model_info = mlflow.pytorch.log_model(model, name="model", registered_model_name="MyModel")
```

---

## Conceitos Aprendidos

1. **Autologging** - Uma linha para logging completo
2. **System Metrics** - GPU, CPU, Disk, Network tracking
3. **Model Signatures** - Input/output schema
4. **Checkpoint Tracking** - Version checkpoints with `step` parameter
5. **Metric Links** - Link metrics to model_id and dataset
6. **Search Logged Models** - Rank checkpoints by performance
7. **HPO with Optuna** - Nested runs for hyperparameter tuning
8. **Model Registry** - Register models for deployment
9. **Distributed Training** - Log only from rank 0