# MLflow Projects - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/projects/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que são MLflow Projects

Formato padrão para empacotar e compartilhar código de data science reprodutível. Baseado em convenções simples, permite colaboração e execução automatizada em diferentes ambientes.

---

## Quick Start

```bash
# Rodar projeto do GitHub
mlflow run https://github.com/mlflow/mlflow-example.git -P alpha=0.5

# Rodar projeto local
mlflow run . -P data_file=data.csv -P regularization=0.1

# Entry point específico
mlflow run . -e validate -P data_file=data.csv
```

### Python API
```python
import mlflow

# Executar remote
result = mlflow.run(
    "https://github.com/mlflow/mlflow-example.git",
    parameters={"alpha": 0.5, "l1_ratio": 0.01},
    experiment_name="elasticnet_experiment",
)

# Executar local
result = mlflow.run(
    ".", entry_point="train", parameters={"epochs": 100}, synchronous=True
)
```

---

## Core Concepts

### Project Components
1. **Project Name** - Identificador
2. **Entry Points** - Comandos executáveis
   - Parameters (inputs com tipos e defaults)
   - Commands (o que executa)
   - Environment (contexto de execução)
3. **Environment** - Dependências

### Environment Types

| Environment | Use Case | Dependencies |
|-------------|----------|--------------|
| Virtualenv (Recommended) | Python packages PyPI | python_env.yaml |
| Conda | Python + native libraries | conda.yaml |
| Docker | Complex dependencies, non-Python | Dockerfile |
| System | Current environment | None |

---

## Project Structure

### Convention-Based (sem MLproject)
```
my-project/
├── train.py           # Entry point
├── validate.sh        # Shell script entry point
├── conda.yaml         # Optional: Conda env
├── python_env.yaml    # Optional: Python env
└── data/              # Project data
```

### MLproject File (advanced)
```yaml
name: My ML Project

python_env: python_env.yaml

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

---

## Parameter Types

| Type | Description | Example | Special |
|------|-------------|---------|---------|
| string | Text data | "hello world" | None |
| float | Decimal numbers | 0.1, 3.14 | Validation |
| int | Whole numbers | 42, 100 | Validation |
| path | Local file paths | data.csv | Downloads remote URIs |
| uri | Any URI | s3://bucket/ | Converts relative to absolute |

---

## Environment Management

### Virtualenv (python_env.yaml)
```yaml
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

### Conda (conda.yaml)
```yaml
name: ml-project
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - cudnn=8.2.1
  - scikit-learn
  - pip:
    - mlflow>=2.0.0
    - tensorflow==2.10.0
```

### Docker
```yaml
name: Containerized Project
docker_env:
  image: my-ml-image:latest
  volumes: ["/host/data:/container/data"]
  environment:
    - ["CUDA_VISIBLE_DEVICES", "0,1"]
    - "AWS_PROFILE"
```

---

## Execution & Deployment

### Local
```bash
# Basic
mlflow run .

# With parameters
mlflow run . -P lr=0.01 -P batch_size=32

# Custom environment
mlflow run . --env-manager virtualenv
```

### Remote (Databricks)
```bash
mlflow run . --backend databricks --backend-config cluster-config.json
```

### Remote (Kubernetes)
```bash
mlflow run . --backend kubernetes --backend-config k8s-config.json
```

---

## Building Workflows

### Multi-Step Pipeline
```python
def ml_pipeline():
    client = MlflowClient()
    
    # Step 1: Data preprocessing
    prep_run = mlflow.run("./preprocessing", parameters={"input_path": "s3://bucket/raw-data"})
    
    # Step 2: Feature engineering
    feature_run = mlflow.run("./feature_engineering", parameters={"data_path": processed_data_path})
    
    # Step 3: Parallel model training
    model_runs = []
    for algo in ["random_forest", "xgboost", "neural_network"]:
        run = mlflow.run("./training", entry_point=algo, synchronous=False)
        model_runs.append(run)
    
    # Step 4: Deploy best model
    mlflow.run("./deployment", parameters={"model_run_id": best_model})
```

---

## Best Practices

### Project Organization
```
ml-project/
├── MLproject          # Configuration
├── python_env.yaml    # Dependencies
├── src/               # Source code
│   ├── train.py
│   ├── evaluate.py
│   └── utils/
├── data/              # Sample/test data
├── configs/           # Configuration files
├── tests/             # Unit tests
└── README.md
```

### Environment Selection
- **Virtualenv**: Pure Python projects
- **Conda**: System libraries (CUDA, Intel MKL)
- **Docker**: Complex dependencies, production

---

## Conceitos Aprendidos

1. **Convention-Based Projects** - Funciona sem MLproject file
2. **Entry Points** - Múltiplos comandos parametrizados
3. **Environment Types** - Virtualenv, Conda, Docker, System
4. **Parameter Types** - string, float, int, path, uri
5. **Remote Execution** - Databricks, Kubernetes
6. **Multi-Step Pipelines** - Workflows compostos de múltiplos projects
7. **Parallel Execution** - Hyperparameter search com jobs paralelos

---

## Git Integration

```bash
# Specific commit
mlflow run https://github.com/mlflow/mlflow-example.git --version <commit hash>

# Branch
mlflow run https://github.com/mlflow/mlflow-example.git --version feature-branch

# Subdirectory
mlflow run https://github.com/my-repo.git#subdirectory/my-project
```