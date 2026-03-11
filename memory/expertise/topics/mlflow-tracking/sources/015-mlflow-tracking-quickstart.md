# MLflow Tracking Quickstart - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/tracking/quickstart/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

Guia rápido para as APIs essenciais do MLflow Tracking. Em poucos minutos você aprende:
- Log parameters, metrics e models
- Navegar na MLflow UI
- Carregar modelo para inference

---

## Step 1 - Setup

### Instalação

```bash
pip install mlflow
```

### Criar Experimento

```python
import mlflow

mlflow.set_experiment("MLflow Quickstart")
```

---

## Step 2 - Preparar Dados

```python
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load Iris dataset
X, y = datasets.load_iris(return_X_y=True)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameters
params = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "random_state": 8888,
}
```

---

## Step 3 - Autologging

A maneira mais simples de logar tudo automaticamente:

```python
import mlflow

# Enable autologging for scikit-learn
mlflow.sklearn.autolog()

# Train normally
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)
```

**O que é logado automaticamente:**
- Trained model
- Performance metrics (accuracy, precision, AUC)
- Hyperparameter values
- Metadata (input format, user, timestamp)

---

## Step 4 - MLflow UI

```bash
mlflow server --port 5000
# Acessar http://localhost:5000
```

**Na UI:**
1. Experiments → Lista de experimentos
2. Click no experiment → Lista de runs
3. Click no run → Detalhes (metrics, params, tags)
4. Model section → Ver modelo logado
5. Artifacts → Arquivos e dependências

---

## Step 5 - Manual Logging

Para controle total sobre o logging:

```python
import mlflow

with mlflow.start_run():
    # Log hyperparameters
    mlflow.log_params(params)
    
    # Train model
    lr = LogisticRegression(**params)
    lr.fit(X_train, y_train)
    
    # Log model
    model_info = mlflow.sklearn.log_model(sk_model=lr, name="iris_model")
    
    # Predictions and metrics
    y_pred = lr.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    mlflow.log_metric("accuracy", accuracy)
    
    # Tag for organization
    mlflow.set_tag("Training Info", "Basic LR model for iris data")
```

---

## Step 6 - Carregar Modelo para Inference

### Como pyfunc (genérico)

```python
# Load as pyfunc
loaded_model = mlflow.pyfunc.load_model(model_info.model_uri)

# Predict
predictions = loaded_model.predict(X_test)
```

### Como sklearn nativo

```python
# Load as native sklearn
loaded_model = mlflow.sklearn.load_model(model_info.model_uri)

# Predict
predictions = loaded_model.predict(X_test)
```

### Resultados

```python
iris_feature_names = datasets.load_iris().feature_names

result = pd.DataFrame(X_test, columns=iris_feature_names)
result["actual_class"] = y_test
result["predicted_class"] = predictions

print(result[:4])
```

---

## Fluxo Completo

```
┌─────────────────────────────────────────────────────────┐
│                   MLflow Tracking Flow                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Setup                                                │
│     pip install mlflow                                   │
│     mlflow.set_experiment("name")                        │
│                                                          │
│  2. Autolog (opção simples)                              │
│     mlflow.sklearn.autolog()                             │
│     model.fit(X, y)                                      │
│                                                          │
│  3. Manual Logging (controle total)                      │
│     with mlflow.start_run():                             │
│         mlflow.log_params(params)                         │
│         mlflow.log_model(model, "name")                   │
│         mlflow.log_metric("metric", value)                │
│         mlflow.set_tag("key", "value")                    │
│                                                          │
│  4. View UI                                              │
│     mlflow server --port 5000                            │
│     http://localhost:5000                                 │
│                                                          │
│  5. Load Model                                           │
│     model = mlflow.pyfunc.load_model(uri)                │
│     predictions = model.predict(X)                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Autologging vs Manual Logging

| Aspecto | Autologging | Manual |
|---------|-------------|--------|
| **Setup** | 1 linha | Múltiplas linhas |
| **Controle** | Limitado | Total |
| **Métricas** | Automáticas | Customizadas |
| **Models** | Auto-saved | Específico |
| **Tags** | System tags | Custom tags |
| **Uso** | Quick start | Production |

---

## Quick Reference

```python
import mlflow
from sklearn.linear_model import LogisticRegression

# Setup
mlflow.set_experiment("my-experiment")

# Autologging
mlflow.sklearn.autolog()
model = LogisticRegression()
model.fit(X_train, y_train)

# OU Manual
with mlflow.start_run():
    mlflow.log_params({"lr": 0.01, "epochs": 100})
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
    mlflow.set_tag("version", "1.0")

# Load model
loaded = mlflow.pyfunc.load_model("models:/my-model/1")
predictions = loaded.predict(X_test)
```

---

## Conceitos Aprendidos

1. **Autologging** - Logging automático com uma linha
2. **Manual Logging** - Controle total com API granular
3. **MLflow UI** - Interface visual para explorar runs
4. **Model Loading** - pyfunc (genérico) vs nativo (sklearn)
5. **Context Manager** - `with mlflow.start_run():`
6. **Experiment Organization** - Agrupar runs por experimento

---

## Próximos Passos

- **MLflow for GenAI** - LLM development
- **MLflow for Deep Learning** - PyTorch, TensorFlow
- **MLflow Tracking** - APIs avançadas
- **Self-hosting Guide** - Deploy para times