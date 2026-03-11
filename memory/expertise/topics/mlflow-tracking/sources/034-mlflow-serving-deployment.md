# MLflow Serving - Deployment Guide

**Fonte:** DOC-011 - MLflow Serving Official Documentation  
**URL:** https://mlflow.org/docs/latest/ml/deployment/  
**Tipo:** Documentação Oficial  
**Data:** 2025  
**Status:** completed

---

## Resumo

Documentação oficial de deployment do MLflow: conceitos (Model, Container, Deployment Target), deployment targets suportados, CLI e Python APIs.

---

## Benefits of MLflow Deployment

1. **Effortless Deployment**: Simple interface for deploying to various targets
2. **Dependency Management**: Deployment environment mirrors training environment
3. **Packaging Models and Code**: Model + supplementary code + configurations packaged together
4. **Avoid Vendor Lock-in**: Standard format, easy switch between targets

---

## Core Concepts

### MLflow Model
- Standard format for packaging ML model + metadata
- Dependencies, inference schema included
- Created via `mlflow.pyfunc.log_model()`
- Can be registered via Model Registry

### Container
- Docker containers package models with dependencies
- Enables deployment without environment compatibility issues
- Critical role in standardizing deployment process

### Deployment Target
- Destination environment for model
- Supports: local, cloud services, Kubernetes clusters

---

## How It Works

1. **MLflow Model** already packages model + dependencies
2. MLflow creates either:
   - Virtual environment (local deployment)
   - Docker container image (cloud/Kubernetes)
3. MLflow launches inference server with REST endpoints (FastAPI)
4. Ready for deployment to various destinations

---

## Supported Deployment Targets

| Target | Description |
|--------|-------------|
| **Local** | `mlflow models serve` - simple local deployment |
| **Amazon SageMaker** | Fully managed ML inference containers |
| **Azure ML** | Managed online/batch endpoints, ACI, AKS |
| **Databricks Model Serving** | Fully managed with performance optimizations |
| **Kubernetes** | Seldon Core, KServe (formerly KFServing) |
| **Modal** | Serverless cloud with on-demand GPU (T4 to H200) |
| **Community Targets** | Ray Serve, Redis AI, Torch Serve, OCI |

---

## CLI Commands

### Primary Modules
- `mlflow models` - typically for local deployment
- `mlflow deployments` - for deploying to custom targets

### Target-Specific Commands
- `mlflow sagemaker` - Amazon SageMaker deployments
- `azureml-mlflow` library required for Azure ML

---

## Python APIs

```python
# Model management
import mlflow.models

# Deployment management
import mlflow.deployments

# SageMaker specific
import mlflow.sagemaker
```

---

## Local Deployment

```bash
# Serve model locally
mlflow models serve \
  --model-uri "models:/my-model/Production" \
  --host 0.0.0.0 \
  --port 5001

# From run
mlflow models serve \
  --model-uri "runs:/abc123/model" \
  --host 0.0.0.0 \
  --port 5001
```

---

## Kubernetes Deployment

### Integration Options
1. **Seldon Core**: Kubernetes-native ML serving
2. **KServe** (formerly KFServing): Serverless inference

### Docker Container
- MLflow builds Docker image with model + dependencies
- Deploy to Kubernetes with standard manifests
- Auto-scaling, rolling updates, health checks

---

## Concepts Adicionados

- Vendor lock-in avoidance pattern
- Container-based deployment standard
- FastAPI inference server
- Virtual environment vs Docker container
- Modal serverless GPU platform
- Community deployment plugins

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 10 min