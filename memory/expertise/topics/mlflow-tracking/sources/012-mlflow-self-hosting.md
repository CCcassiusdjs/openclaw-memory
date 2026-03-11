# MLflow Self-Hosting - Resumo

**Fonte:** https://mlflow.org/docs/latest/self-hosting/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

MLflow é totalmente open-source e vendor-neutral. Milhares de usuários e organizações rodam suas próprias instâncias.

### Mudança Importante (MLflow 3.7.0+)

- **Default backend:** SQLite (`sqlite:///mlflow.db`) em vez de file-based (`./mlruns`)
- **Existing users:** MLflow detecta automaticamente dados em `./mlruns`
- **New users:** SQLite por default. Para file-based: `MLFLOW_TRACKING_URI=./mlruns`

---

## Início Rápido

### Instalação

```bash
pip install mlflow
```

### Iniciar Servidor

```bash
mlflow server --port 5000
```

Acessar UI: http://localhost:5000

### Conectar Cliente

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

# Start tracking!
with mlflow.start_run():
    mlflow.log_param("lr", 0.001)
```

---

## Opções de Deployment

### Docker Compose

```bash
git clone https://github.com/mlflow/mlflow.git
cd docker-compose
cp .env.dev.example .env
docker compose up -d
```

Inclui: MLflow + PostgreSQL + RustFS

### Kubernetes

Helm charts disponíveis:
- [Bitnami MLflow Helm](https://artifacthub.io/packages/helm/bitnami/mlflow)
- [Community Helm Charts](https://artifacthub.io/packages/helm/community-charts/mlflow)

### Cloud Services (Managed)

| Provider | Serviço |
|----------|---------|
| **Databricks** | Managed MLflow |
| **AWS** | SageMaker AI Experiments |
| **Azure** | Azure Machine Learning |
| **Nebius** | Managed MLflow |
| **GCP** | GKE MLflow |

---

## Arquitetura

### Componentes

```
┌─────────────────────────────────────────────────────────┐
│                    MLflow Tracking                       │
├─────────────────┬──────────────────┬────────────────────┤
│ Tracking Server │  Backend Store   │   Artifact Store   │
│ (FastAPI)       │  (Database)      │   (Cloud/Local)    │
└─────────────────┴──────────────────┴────────────────────┘
```

| Componente | Descrição |
|------------|-----------|
| **Tracking Server** | FastAPI server que serve UI e API |
| **Backend Store** | Database para metadata (experiments, runs, traces) |
| **Artifact Store** | Storage para artifacts (model weights, images) |

### Pluggable Architecture

Cada componente é plugável:
- **Single host:** SQLite + local filesystem
- **Production:** PostgreSQL + S3/GCS/Azure Blob

---

## Backend Store Options

| Tipo | Uso |
|------|-----|
| **SQLite** | Development, single user |
| **PostgreSQL** | Production, team |
| **MySQL** | Production, team |
| **File-based** | Development only |

---

## Artifact Store Options

| Storage | Protocol |
|---------|----------|
| **Local filesystem** | `./mlruns` |
| **Amazon S3** | `s3://bucket/path` |
| **Google Cloud Storage** | `gs://bucket/path` |
| **Azure Blob Storage** | `wasbs://container@account.blob.core.windows.net/path` |
| **SFTP** | `sftp://host/path` |
| **NFS** | `/mnt/nfs/path` |

---

## Workspaces

Organizar experiments, models, prompts e artifacts em instância compartilhada:
- Separação lógica
- Permissões por workspace
- Requer SQL database backend

---

## Access Control & Security

### Authentication Options

| Método | Descrição |
|--------|-----------|
| **Basic HTTP Auth** | Username/password |
| **SSO** | Single Sign-On |
| **Custom Plugins** | Plugins de autenticação customizados |

### Network Protection

```bash
mlflow server --allowed-hosts "mlflow.company.com,localhost:*" \
               --cors-allowed-origins "https://app.company.com"
```

**Proteções:**
- Host validation (`--allowed-hosts`)
- CORS restrictions (`--cors-allowed-origins`)

---

## Common Issues

### "ACCESS DENIED" Error

**Causa:** Configuração de segurança do tracking server

**Solução:**
```bash
mlflow server --allowed-hosts "mlflow.company.com,localhost:*" \
               --cors-allowed-origins "https://app.company.com"
```

**Nota:** Security options apenas com FastAPI (uvicorn), não Flask.

---

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        MLflow Architecture                    │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌─────────────────────┐    ┌─────────────────────────────┐ │
│   │   MLflow Client     │    │    MLflow UI               │ │
│   │   (Python/R/Java)    │    │    (Browser)               │ │
│   └──────────┬──────────┘    └──────────────┬──────────────┘ │
│              │                               │                 │
│              └───────────────┬───────────────┘                 │
│                              │                                 │
│                              ▼                                 │
│                   ┌─────────────────────┐                     │
│                   │   Tracking Server    │                     │
│                   │   (FastAPI)          │                     │
│                   └──────────┬──────────┘                     │
│                              │                                 │
│              ┌───────────────┴───────────────┐                 │
│              ▼                               ▼                 │
│   ┌─────────────────────┐    ┌─────────────────────────────┐ │
│   │   Backend Store      │    │   Artifact Store            │ │
│   │   (PostgreSQL)       │    │   (S3/GCS/Azure)            │ │
│   └─────────────────────┘    └─────────────────────────────┘ │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Conceitos Aprendidos

1. **Vendor-Neutral** - Open-source, sem vendor lock-in
2. **Default Backend** - SQLite (MLflow 3.7+), era file-based
3. **Docker Compose** - Deployment com PostgreSQL + RustFS
4. **Kubernetes** - Helm charts (Bitnami, Community)
5. **Managed Services** - Databricks, AWS, Azure, Nebius, GCP
6. **Pluggable Components** - Backend Store + Artifact Store
7. **Workspaces** - Separação lógica com permissões
8. **Authentication** - Basic HTTP, SSO, Custom Plugins
9. **Network Protection** - Host validation, CORS

---

## Quick Reference

```bash
# Instalar
pip install mlflow

# Iniciar servidor (SQLite default)
mlflow server --port 5000

# Com PostgreSQL
mlflow server --port 5000 \
              --backend-store-uri postgresql://user:pass@host/db \
              --artifacts-destination s3://my-bucket/

# Com autenticação
mlflow server --port 5000 \
              --app-name basic-auth

# Network protection
mlflow server --port 5000 \
              --allowed-hosts "mlflow.company.com" \
              --cors-allowed-origins "https://app.company.com"
```

```python
# Conectar ao servidor
import mlflow
mlflow.set_tracking_uri("http://localhost:5000")

# Usar workspaces
mlflow.set_experiment("/workspace-name/experiment-name")
```