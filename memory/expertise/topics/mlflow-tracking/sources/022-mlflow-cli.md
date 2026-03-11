# MLflow CLI - Resumo

**Fonte:** https://mlflow.org/docs/latest/api_reference/cli.html  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

MLflow CLI fornece interface de linha de comando para gerenciar projects, tracking UI, experiments, models e deployments.

**Importante:** Setar `MLFLOW_TRACKING_URI` para conectar ao tracking server.

---

## Comandos Principais

### server

Iniciar MLflow Tracking Server:

```bash
mlflow server --port 5000
# ou
mlflow server --backend-store-uri postgresql://user:pass@host/db \
              --default-artifact-root s3://my-bucket/ \
              --port 5000
```

### run

Executar MLflow Project:

```bash
mlflow run . -P alpha=0.5 -P l1_ratio=0.01
mlflow run https://github.com/mlflow/mlflow-example.git
```

---

## Experiments

### Criar Experiment

```bash
mlflow experiments create -n "my-experiment" -l s3://bucket/artifacts/
```

### Listar Experiments

```bash
mlflow experiments search --view active_only --max-results 100
```

### Obter Experiment

```bash
mlflow experiments get --experiment-id 1
mlflow experiments get --experiment-name "Default" --output json
```

### Deletar/Restaurar

```bash
mlflow experiments delete --experiment-id 1
mlflow experiments restore --experiment-id 1
```

### Renomear

```bash
mlflow experiments rename --experiment-id 1 --new-name "new-name"
```

---

## Runs

### Download Artifacts

```bash
mlflow artifacts download --run-id <run-id>
mlflow artifacts download --artifact-uri s3://bucket/path/artifact
```

### Listar Artifacts

```bash
mlflow artifacts list --run-id <run-id>
```

### Log Artifact

```bash
mlflow artifacts log-artifact --local-file model.pkl --run-id <run-id>
mlflow artifacts log-artifacts --local-dir ./outputs/ --run-id <run-id>
```

---

## Models

### Serve Model

```bash
mlflow models serve -m runs:/<run-id>/model -p 5001
mlflow models serve -m models:/my-model/production -p 5001
```

### Build Docker

```bash
mlflow models build-docker -m runs:/<run-id>/model --name my-image
docker run -p 5001:8080 my-image
```

### Predict

```bash
mlflow models predict -m runs:/<run-id>/model -i input.json -o output.json
```

---

## Deployments

Gerenciar deployments em targets:

```bash
# Criar deployment
mlflow deployments create --name my-deployment --model-uri models:/my-model/1 \
                          --target sagemaker --endpoint my-endpoint

# Listar deployments
mlflow deployments list --target sagemaker

# Atualizar deployment
mlflow deployments update --name my-deployment --model-uri models:/my-model/2 \
                          --target sagemaker

# Deletar deployment
mlflow deployments delete --name my-deployment --target sagemaker
```

**Targets suportados:** databricks, http, https, openai, sagemaker, faketarget

---

## Garbage Collection

Remover permanentemente runs deletados:

```bash
# Runs deletados há mais de 30 dias
mlflow gc --older-than 30d

# Runs específicos
mlflow gc --run-ids 'run1,run2,run3'

# Experiments deletados
mlflow gc --experiment-ids 'exp1,exp2'

# Jobs antigos
mlflow gc --jobs --older-than 7d
```

---

## Database Commands

### Schema Migration

```bash
mlflow db upgrade postgresql://user:pass@host:5432/mlflow
```

**Importante:** Sempre fazer backup antes de migrations!

---

## Demo

Launch MLflow com dados demo:

```bash
mlflow demo --port 5000
mlflow demo --refresh  # Regenerate data
mlflow demo --no-browser
```

---

## Doctor

Debug info:

```bash
mlflow doctor --mask-envs
```

Output: system info, Python version, MLflow version, dependencies.

---

## Autolog Commands

### Claude Code Tracing

```bash
# Setup Claude Code tracing
mlflow autolog claude ~/my-project -u databricks -e 123456789

# Disable
mlflow autolog claude --disable

# Status
mlflow autolog claude --status
```

---

## Gateway Commands

### Start Gateway

```bash
mlflow gateway start --config-path gateway.yaml --port 5000
```

---

## Datasets Commands

```bash
# Listar datasets de evaluation
mlflow datasets list --experiment-id 1 --max-results 10

# Filtrar
mlflow datasets list --experiment-id 1 --filter-string "name LIKE 'qa_%'"
```

---

## Quick Reference

```bash
# Server
mlflow server --port 5000 --backend-store-uri sqlite:///mlflow.db

# Experiments
mlflow experiments create -n "my-exp"
mlflow experiments search --view all
mlflow experiments get --experiment-id 1 --output json

# Runs
mlflow run . -P alpha=0.5
mlflow artifacts download --run-id <id>

# Models
mlflow models serve -m models:/my-model/production -p 5001
mlflow models build-docker -m runs:/<id>/model --name my-image

# Deployments
mlflow deployments create --name deploy --model-uri models:/m/1 --target sagemaker
mlflow deployments list --target sagemaker

# GC
mlflow gc --older-than 30d

# Debug
mlflow doctor
```

---

## Conceitos Aprendidos

1. **mlflow server** - Iniciar Tracking Server
2. **mlflow run** - Executar Projects
3. **mlflow experiments** - CRUD de experiments
4. **mlflow artifacts** - Gerenciar artifacts
5. **mlflow models** - Serve e build Docker
6. **mlflow deployments** - Deploy em Sagemaker, Databricks, etc.
7. **mlflow gc** - Garbage collection
8. **mlflow db** - Schema migrations
9. **mlflow demo** - Ambiente demo
10. **mlflow doctor** - Debug info