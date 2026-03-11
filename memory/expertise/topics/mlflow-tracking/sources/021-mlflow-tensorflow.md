# MLflow TensorFlow Integration - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/deep-learning/tensorflow/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

MLflow + TensorFlow = Experiment tracking, model versioning e deployment para deep learning com Keras API.

---

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Autologging** | Uma linha: `mlflow.tensorflow.autolog()` |
| **Experiment Tracking** | Métricas, hiperparâmetros, arquiteturas |
| **Model Registry** | Versionamento, staging, deployment |
| **Reproducibility** | Training configs, environments |

---

## Autologging

```python
import mlflow
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Enable autologging
mlflow.tensorflow.autolog()

# Prepare sample data
data = np.random.uniform(size=[20, 28, 28, 3])
label = np.random.randint(2, size=20)

# Define model
model = keras.Sequential([
    keras.Input([28, 28, 3]),
    keras.layers.Conv2D(8, 2),
    keras.layers.MaxPool2D(2),
    keras.layers.Flatten(),
    keras.layers.Dense(2),
    keras.layers.Softmax(),
])

model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(),
    optimizer=keras.optimizers.Adam(0.001),
    metrics=[keras.metrics.SparseCategoricalAccuracy()],
)

# Training with automatic logging
with mlflow.start_run():
    model.fit(data, label, batch_size=5, epochs=2)
```

**Requer:** TensorFlow >= 2.3.0, model.fit() Keras API

### Configurar Autologging

```python
mlflow.tensorflow.autolog(
    log_models=True,
    log_input_examples=True,
    log_model_signatures=True,
    log_every_n_steps=1,
)
```

---

## Manual Logging with Callback

```python
import mlflow
from tensorflow import keras

# Define and compile model
model = keras.Sequential([
    keras.Input([28, 28, 3]),
    keras.layers.Conv2D(8, 3),
    keras.layers.MaxPool2D(2),
    keras.layers.Flatten(),
    keras.layers.Dense(2, activation="softmax"),
])

model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer=keras.optimizers.Adam(0.001),
    metrics=["accuracy"],
)

# Use MLflow callback
with mlflow.start_run() as run:
    model.fit(
        data,
        labels,
        batch_size=32,
        epochs=10,
        callbacks=[mlflow.tensorflow.MlflowCallback(run)],
    )
```

---

## Custom Callback

```python
from tensorflow import keras
import math
import mlflow

class CustomMlflowCallback(keras.callbacks.Callback):
    def on_epoch_begin(self, epoch, logs=None):
        mlflow.log_metric("current_epoch", epoch)
    
    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        # Log metrics in log scale
        for k, v in logs.items():
            if v > 0:
                mlflow.log_metric(f"log_{k}", math.log(v), step=epoch)
            mlflow.log_metric(k, v, step=epoch)
    
    def on_train_end(self, logs=None):
        # Log final model weights statistics
        weights = self.model.get_weights()
        mlflow.log_metric("total_parameters", sum(w.size for w in weights))
```

---

## Model Logging

```python
import mlflow
import tensorflow as tf
from tensorflow import keras

# Define and train model
model = keras.Sequential([
    keras.Input([28, 28, 3]),
    keras.layers.Conv2D(8, 2),
    keras.layers.MaxPool2D(2),
    keras.layers.Flatten(),
    keras.layers.Dense(2),
    keras.layers.Softmax(),
])

# Train (code omitted)
# model.fit(...)

# Log model
model_info = mlflow.tensorflow.log_model(model, name="model")

# Load for inference
loaded_model = mlflow.tensorflow.load_model(model_info.model_uri)
predictions = loaded_model.predict(tf.random.uniform([1, 28, 28, 3]))
```

---

## Hyperparameter Optimization

```python
import mlflow
import tensorflow as tf
from tensorflow import keras
import optuna

def objective(trial, x_train, y_train, x_val, y_val):
    with mlflow.start_run(nested=True):
        params = {
            "learning_rate": trial.suggest_float("learning_rate", 1e-5, 1e-1, log=True),
            "units": trial.suggest_int("units", 32, 512),
            "dropout": trial.suggest_float("dropout", 0.1, 0.5),
        }
        
        mlflow.log_params(params)
        
        model = keras.Sequential([
            keras.layers.Input(shape=(28, 28, 3)),
            keras.layers.Flatten(),
            keras.layers.Dense(params["units"], activation="relu"),
            keras.layers.Dropout(params["dropout"]),
            keras.layers.Dense(10, activation="softmax"),
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=params["learning_rate"]),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        
        history = model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=5,
            verbose=0
        )
        
        val_accuracy = max(history.history["val_accuracy"])
        mlflow.log_metric("val_accuracy", val_accuracy)
        
        return val_accuracy

# Main experiment run
with mlflow.start_run(run_name="tensorflow_hpo"):
    study = optuna.create_study(direction="maximize")
    study.optimize(
        lambda trial: objective(trial, x_train, y_train, x_val, y_val),
        n_trials=20
    )
    
    mlflow.log_params({f"best_{k}": v for k, v in study.best_params.items()})
    mlflow.log_metric("best_val_accuracy", study.best_value)
```

---

## Model Registry Integration

```python
import mlflow
from tensorflow import keras
from mlflow import MlflowClient

client = MlflowClient()

with mlflow.start_run():
    model = keras.Sequential([
        keras.layers.Conv2D(32, 3, activation="relu", input_shape=(224, 224, 3)),
        keras.layers.MaxPooling2D(2),
        keras.layers.Flatten(),
        keras.layers.Dense(10, activation="softmax"),
    ])
    
    # Log model to registry
    model_info = mlflow.tensorflow.log_model(
        model,
        name="tensorflow_model",
        registered_model_name="ImageClassifier"
    )
    
    mlflow.set_tags({
        "model_type": "cnn",
        "dataset": "imagenet",
        "framework": "tensorflow"
    })

# Set alias for production
client.set_registered_model_alias(
    name="ImageClassifier",
    alias="champion",
    version=model_info.registered_model_version,
)
```

---

## Quick Reference

```python
import mlflow
from tensorflow import keras

# Autologging
mlflow.tensorflow.autolog()

# Callback
with mlflow.start_run() as run:
    model.fit(data, labels, callbacks=[mlflow.tensorflow.MlflowCallback(run)])

# Manual logging
with mlflow.start_run():
    mlflow.log_params({"lr": 0.001, "epochs": 10})
    mlflow.log_metric("accuracy", accuracy, step=epoch)
    mlflow.tensorflow.log_model(model, name="model")

# Load
loaded = mlflow.tensorflow.load_model("runs:/<run_id>/model")

# Registry
model_info = mlflow.tensorflow.log_model(model, name="model", registered_model_name="MyModel")
```

---

## Conceitos Aprendidos

1. **Autologging** - Uma linha para logging completo
2. **MlflowCallback** - Callback para Keras
3. **Custom Callback** - Subclass keras.callbacks.Callback
4. **Model Logging** - mlflow.tensorflow.log_model()
5. **HPO with Optuna** - Nested runs para hyperparameter tuning
6. **Model Registry** - Register models for deployment
7. **Model Loading** - Load TensorFlow/Keras models

---

## Diferenças PyTorch vs TensorFlow

| Aspecto | PyTorch | TensorFlow |
|---------|---------|------------|
| **Autologging** | `mlflow.pytorch.autolog()` | `mlflow.tensorflow.autolog()` |
| **Callback** | Manual loop | `MlflowCallback` |
| **Model Load** | `mlflow.pytorch.load_model()` | `mlflow.tensorflow.load_model()` |
| **Training Loop** | Custom loop | `model.fit()` |
| **Distributed** | DDP | tf.distribute |