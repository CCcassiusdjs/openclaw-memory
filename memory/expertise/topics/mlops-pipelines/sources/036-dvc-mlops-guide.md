# DVC - Data Version Control - Resumo

**Fonte:** https://mlops-guide.github.io/Versionamento/
**Tipo:** Tutorial
**Data:** 2026-03-12

---

## 🎯 O que é DVC?

**DVC** (Data Version Control) é um **experiment management tool** para ML projects:
- Built on top of **Git**
- Codifica data, models, pipelines via command line
- Replace large files with small metafiles

## 📋 Como Funciona

| Git | DVC |
|-----|-----|
| Version control para código | Version control para data/models |
| Stores in repository | Stores in remote storage |
| Small files | Large files supported |

### Workflow
```
Large file (dataset/model) → DVC creates .dvc metafile → 
Git tracks metafile → Remote storage stores actual data
```

## 🚀 Features Principais

| Feature | Descrição |
|---------|-----------|
| **Data versioning** | Track datasets like code |
| **Model versioning** | Track ML models |
| **Pipeline management** | Lightweight dependency graphs |
| **Reproducibility** | Experiments reproducible for all members |
| **Platform agnostic** | Works with any OS, language, ML library |

## 🔧 Instalação

### Via pip
```bash
pip install dvc
# Optional dependencies for remote storage
pip install "dvc[s3]"  # For AWS S3, IBM COS
pip install "dvc[gs]"  # For Google Cloud Storage
pip install "dvc[all]"  # All storage backends
```

### Via conda
```bash
conda install -c conda-forge mamba
mamba install -c conda-forge dvc
mamba install -c conda-forge dvc-s3
```

## 📋 Setup Inicial

### Inicialização
```bash
# Initialize Git first
git init

# Initialize DVC
dvc init

# Check created config files
git status
```

### Remote Storage
```bash
# Add remote storage
dvc remote add -d remote-storage s3://bucket_name/folder/

# Configure endpoint (ex: IBM Cloud)
dvc remote modify remote-storage endpointurl \
  https://s3.us-south.cloud-object-storage.appdomain.cloud

# Configure credentials
dvc remote modify myremote profile myprofile

# Or point to credentials file
dvc remote modify credentialpath /path/to/creds
```

### Credentials Setup
```ini
# ~/.aws/credentials
[default]
aws_access_key_id = ************
aws_secret_access_key = ************

[myprofile]
aws_access_key_id = ************
aws_secret_access_key = ************
```

## 🔄 DVC Workflow

### Adicionar dados
```bash
# Create data folder
mkdir data

# Add file to DVC
dvc add data/data.csv

# Track .dvc file with Git
git add data/data.csv.dvc
git commit -m "Add dataset"
```

### Push to remote
```bash
# Push data to remote storage
dvc push
```

### Pull from remote
```bash
# Pull data from remote storage
dvc pull
```

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Metafile (.dvc)** | Small file pointing to actual data |
| **Remote storage** | Where large files are stored |
| **Dependency graph** | Pipeline stages with dependencies |
| **Reproducibility** | Same results from same code + data |

## 🔗 Storage Backends Suportados

- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Google Drive
- SFTP
- Local storage
- And more...

## 🔗 Referências Cruzadas

- Pré-requisito: Git basics
- Complementa: MLflow Model Registry (016-020)
- Relacionado a: CML (CI/CD for ML) (012)

---

**Conceitos aprendidos:** 12
**Relevância:** Alta (data versioning fundamental)