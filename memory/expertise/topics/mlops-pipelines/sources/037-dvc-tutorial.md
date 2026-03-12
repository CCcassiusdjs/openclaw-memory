# DVC Tutorial: Data Version Control for MLOps - Resumo

**Fonte:** https://anderfernandez.com/en/blog/dvc-tutorial-mlops-data-version-control/
**Tipo:** Tutorial
**Data:** 2026-03-12

---

## 🎯 Por que DVC?

### Problema: Git Limitations
| Git | DVC |
|-----|-----|
| Max 100MB files | No size limit |
| Stores in repo | Stores in remote storage |
| Code versioning | Data + Model versioning |

### Solução: DVC
- **No file size limit** - datasets, models large
- **Platform agnostic storage** - S3, GCS, Azure, Drive, SFTP
- **Lightweight metafiles** - .dvc files tracked in Git

## 📋 Como DVC Funciona

### Arquitetura
```
Original Data (large) → DVC creates .dvc metafile (small) →
Git tracks .dvc → Remote storage holds actual data
```

### Metafiles
| Arquivo | Propósito |
|---------|-----------|
| `data.csv.dvc` | Metadata pointing to data.csv |
| `.gitignore` | Auto-excludes large files from Git |

## 🔧 Features do DVC

1. **Language agnostic** - Python, R, Julia, etc.
2. **Data pipelines** - Visualize as DAG
3. **Efficient execution** - Only run modified steps
4. **Reproducibility** - Track data + code + parameters

## 🚀 Tutorial Passo a Passo

### Instalação
```bash
# Check installation
dvc version
```

### Inicialização
```bash
# Initialize Git repository
git init

# Initialize DVC
dvc init
```

### Adicionar Dados
```bash
# Create data folder
mkdir data
cd data

# Download data
curl -o data.csv https://example.com/data.csv

# Add to DVC
dvc add data/data.csv
```

### Arquivos Criados
```
data/
├── data.csv          # Original data (large)
├── data.csv.dvc      # DVC metafile (small)
└── .gitignore        # Auto-generated
```

## 📦 Storage Backends

### Google Cloud Storage
```bash
# Requires Google Cloud CLI
# Configure credentials first
dvc remote add -d myremote gs://mybucket/path
```

### AWS S3
```bash
dvc remote add -d myremote s3://mybucket/path
```

### Azure Blob Storage
```bash
dvc remote add -d myremote azure://container/path
```

### Google Drive
```bash
dvc remote add -d myremote gdrive://root/path
```

## 🔄 Workflow Completo

### Adicionar e versionar
```bash
# Add data
dvc add data/dataset.csv

# Track metafile with Git
git add data/dataset.csv.dvc
git commit -m "Add dataset v1"

# Push data to remote
dvc push
```

### Recuperar versão
```bash
# Checkout Git version
git checkout <commit>

# Pull corresponding data
dvc pull
```

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **.dvc file** | Metafile com hash, size, path |
| **Remote** | Storage backend (S3, GCS, etc.) |
| **DAG Pipeline** | Directed Acyclic Graph for stages |
| **Cache** | Local cache of data files |
| **Stage** | Single step in pipeline |

## 🔗 Referências Cruzadas

- Complementa: DVC MLOps Guide (036)
- Relacionado a: Git LFS (alternative)
- Pré-requisito para: CML (012)

---

**Conceitos aprendidos:** 10
**Relevância:** Alta (practical tutorial)