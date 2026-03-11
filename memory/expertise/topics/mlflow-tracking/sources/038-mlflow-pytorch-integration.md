# MLflow PyTorch Integration - Guia Completo

**Fonte:** DOC-013 - MLflow PyTorch Integration  
**URL:** https://mlflow.org/docs/latest/ml/deep-learning/pytorch/  
**Tipo:** Documentação Oficial  
**Data:** 2025  
**Status:** completed

---

## Resumo

Documentação oficial da integração MLflow + PyTorch: autologging, manual logging, system metrics, checkpoint tracking, model signatures, hyperparameter optimization.

---

## Why MLflow + PyTorch?

| Feature | Description |
|---------|-------------|
| **Autologging** | One line: `mlflow.pytorch.autolog()` |
| **Experiment Tracking** | Metrics, hyperparameters, architectures, artifacts |
| **Model Registry** | Version, stage, deploy PyTorch models |
| **Reproducibility** | Model states, random seeds, environments |

---

## Getting Started with Autologging

```python
import mlflow
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Enable autologging
mlflow.pytorch.autolog()

# Create synthetic data
X = torch.randn(1000, 784)
y = torch.randint(0, 10, (1000,))
train_loader = DataLoader(TensorDataset(X, y), batch_size=32, shuffle=True)

# Your existing PyTorch code works unchanged
model = nn.Sequential(nn.Linear(784, 128), nn.ReLU(), nn.Linear(128, 10))
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training loop - metrics, parameters, models logged automatically
for epoch in range(10):
    for data, target in train_loader:
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
```

**Note**: Autologging works seamlessly with PyTorch Lightning. For vanilla PyTorch with custom training loops, use manual logging.

---

## Manual Logging

```python
import mlflow
import torch
import torch.nn as nn
import torch.optim as optim

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28 * 28, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )
    
    def forward(self, x):
        x = self.flatten(x)
        return self.linear_relu_stack(x)

params = {
    "epochs": 5,
    "learning_rate": 1e-3,
    "batch_size": 64,
}

with mlflow.start_run():
    mlflow.log_params(params)
    
    model = NeuralNetwork()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=params["learning_rate"])
    
    for epoch in range(params["epochs"]):
        # Training code...
        avg_loss = train_loss / len(train_loader)
        accuracy = 100.0 * correct / total
        
        mlflow.log_metrics(
            {"train_loss": avg_loss, "train_accuracy": accuracy},
            step=epoch
        )
    
    mlflow.pytorch.log_model(model, name="model")
```

---

## System Metrics Tracking

```python
# Enable system metrics logging
mlflow.enable_system_metrics_logging()

with mlflow.start_run():
    mlflow.log_params({"learning_rate": 0.001, "batch_size": 32, "epochs": 10})
    
    # Training loop - system metrics logged automatically
    for epoch in range(10):
        # ...
        mlflow.log_metric("loss", loss.item(), step=epoch)
```

### Metrics Captured Automatically

| Category | Metrics |
|----------|---------|
| **GPU** | Utilization %, memory usage, temperature, power |
| **CPU** | Utilization %, memory usage |
| **Disk I/O** | Read/write throughput |
| **Network I/O** | Traffic statistics |

### Use Cases
- Identify GPU underutilization (data loading bottlenecks)
- Detect memory issues before OOM errors
- Optimize batch sizes based on GPU memory
- Compare resource efficiency across architectures

---

## Model Logging with Signatures

```python
from mlflow.models import infer_signature

model = nn.Sequential(nn.Linear(10, 50), nn.ReLU(), nn.Linear(50, 1))

# Create sample input/output
input_example = torch.randn(1, 10)
predictions = model(input_example)

# Infer signature
signature = infer_signature(input_example.numpy(), predictions.detach().numpy())

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
    mlflow.log_params({...})
    
    for epoch in range(101):
        # Training step...
        
        if epoch % 10 == 0:
            # Log checkpoint with step parameter
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
best_checkpoint = ranked_checkpoints[0]
```

---

## Model Loading

```python
# Load as PyTorch model
model_uri = "runs:/<run_id>/pytorch_model"
loaded_model = mlflow.pytorch.load_model(model_uri)
predictions = loaded_model(input_tensor)

# Load as PyFunc for generic inference
pyfunc_model = mlflow.pyfunc.load_model(model_uri)
predictions = pyfunc_model.predict(input_tensor.numpy())
```

---

## Hyperparameter Optimization with Optuna

```python
import optuna

def train_and_evaluate(model, optimizer, train_loader, val_loader, epochs=5):
    # Training logic...
    pass

def objective(trial):
    with mlflow.start_run():
        # Suggest hyperparameters
        lr = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
        hidden_size = trial.suggest_int("hidden_size", 32, 256)
        
        model = nn.Sequential(
            nn.Linear(784, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 10)
        )
        optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        
        # Train and evaluate
        accuracy = train_and_evaluate(model, optimizer, train_loader, val_loader)
        
        mlflow.log_metric("val_accuracy", accuracy)
        mlflow.pytorch.log_model(model, "model")
        
        return accuracy

study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)
```

---

## Concepts Adicionados

- System metrics for GPU/CPU monitoring
- Checkpoint versioning with step parameter
- model_id linking metrics to checkpoints
- search_logged_models for ranking
- PyTorch Lightning autologging support
- Optuna integration patterns

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 20 min