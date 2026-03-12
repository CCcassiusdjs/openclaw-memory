# MLflow Projects - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/projects/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 O que é MLflow Projects?

Formato padrão para **empacotar e compartilhar código de data science reprodutível**:
- Convention-based
- Execução em qualquer ambiente
- Colaboração seamless

## 🚀 Quick Start

### Rodar Projeto

```bash
# Run from GitHub
mlflow run https://github.com/mlflow/mlflow-example.git -P alpha=0.5

# Run local project
mlflow run . -P data_file=data.csv -P regularization=0.1

# Run specific entry point
mlflow run . -e validate -P data_file=data.csv
```

### Programmatic Execution

```python
import mlflow

# Execute remote project
result = mlflow.run(
    "https://github.com/mlflow/mlflow-example.git",
    parameters={"alpha": 0.5, "l1_ratio": 0.01},
    experiment_name="elasticnet_experiment",
)

# Execute local project
result = mlflow.run(
    ".", entry_point="train", parameters={"epochs": 100}, synchronous=True
)
```

## 📋 Core Concepts

### Project Components

| Componente | Descrição |
|------------|-----------|
| **Project Name** | Identificador human-readable |
| **Entry Points** | Comandos executáveis com params |
| **Environment** | Contexto de execução e dependências |

### Entry Points
- Parameters com types e defaults
- Commands que são executados
- Environment especificado

## 🏗️ Project Structure

### Convention-Based (Sem MLproject)

```
my-project/
├── train.py          # Executable entry point
├── validate.sh        # Shell script entry point
├── conda.yaml        # Optional: Conda environment
├── python_env.yaml   # Optional: Python environment
└── data/             # Project data
```

**Default Behavior:**
- Name: Directory name
- Entry Points: Any .py or .sh file
- Environment: conda.yaml or python_env.yaml
- Parameters: CLI `--key value`

### MLproject File Configuration

```yaml
name: My ML Project

# Environment (choose one)
python_env: python_env.yaml
# conda_env: conda.yaml
# docker_env:
#   image: python:3.9

entry_points:
  main:
    parameters:
      data_file: path
      regularization: {type: float, default: 0.1}
      max_epochs: {type: int, default: 100}
    command: "python train.py --reg {regularization} --epochs {max_epochs} {data_file}"

  validate:
    parameters:
      model_path: path
      test_data: path
    command: "python validate.py {model_path} {test_data}"
```

## 📊 Parameter Types

| Tipo | Descrição | Exemplo | Special Handling |
|------|-----------|---------|------------------|
| **string** | Text data | "hello" | None |
| **float** | Decimal numbers | 0.1, 3.14 | Validation |
| **int** | Whole numbers | 42, 100 | Validation |
| **path** | Local file paths | data.csv | Downloads remote URIs |
| **uri** | Any URI | s3://bucket/ | Converts relative to absolute |

## 🔧 Environment Management

### Python Virtual Environments (Recommended)

```yaml
# python_env.yaml
python: "3.9.16"

build_dependencies:
  - pip
  - setuptools
  - wheel==0.37.1

dependencies:
  - mlflow>=2.0.0
  - scikit-learn==1.2.0
  - pandas>=1.5.0
```

### Conda Environments

```yaml
# conda.yaml
name: ml-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - cudnn=8.2.1  # CUDA libraries
  - scikit-learn
  - pip:
    - mlflow>=2.0.0
    - tensorflow==2.10.0
```

### Docker Environments

```yaml
# MLproject
name: Containerized Project
docker_env:
  image: my-ml-image:latest
  volumes: ["/host/data:/container/data"]
  environment:
    - ["CUDA_VISIBLE_DEVICES", "0,1"]
    - "AWS_PROFILE"  # Copy from host

entry_points:
  train:
    command: "python distributed_training.py"
```

## 🚀 Execution & Deployment

### Local Execution

```bash
# Basic
mlflow run .

# With parameters
mlflow run . -P lr=0.01 -P batch_size=32

# Specific entry point
mlflow run . -e hyperparameter_search -P n_trials=100

# Custom environment
mlflow run . --env-manager virtualenv
```

### Remote Execution

#### Databricks
```bash
mlflow run . --backend databricks --backend-config cluster-config.json
```

#### Kubernetes
```bash
mlflow run . --backend kubernetes --backend-config k8s-config.json
```

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **MLproject file** | Configuração declarativa do projeto |
| **Entry Point** | Comando executável com params |
| **Environment** | Virtualenv, Conda, ou Docker |
| **Parameter Types** | string, float, int, path, uri |
| **Backend** | Local, Databricks, Kubernetes |

## 🔗 Referências Cruzadas

- Complementa: MLflow Tracking (031)
- Relacionado a: MLflow Model Registry (016-020)
- Pré-requisito para: MLflow Deployment

---

**Conceitos aprendidos:** 15
**Relevância:** Alta (project packaging e reproducibility)