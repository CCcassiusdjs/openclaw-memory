# DVC: Data Version Control for MLOps

**Fonte:** https://anderfernandez.com/en/blog/dvc-tutorial-mlops-data-version-control/
**Autor:** Ander Fernández
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Tutorial completo sobre DVC (Data Version Control) para versionamento de dados em projetos ML. Explica como DVC funciona, instalação, configuração de remotes (GCS, S3, Azure), e criação de data pipelines.

---

## 🎯 Por que DVC?

**Problema:** Git não suporta arquivos > 100MB, mas datasets de ML frequentemente excedem isso.

**Solução:** DVC versiona dados sem armazená-los no servidor. Armazena apenas metadados leves, enquanto dados ficam em storage externo (S3, GCS, Azure, Drive, etc.).

---

## 🏗️ Como DVC Funciona

### Fluxo Básico

```
1. dvc init → Inicializa DVC no repositório
2. dvc add arquivo → Adiciona arquivo ao DVC
3. dvc remote add → Configura storage remoto
4. dvc push → Envia dados para remote
5. dvc pull → Baixa dados do remote
```

### Arquivos Gerados

| Arquivo | Descrição |
|---------|-----------|
| `.dvc/.gitignore` | Exclui arquivos grandes do Git |
| `arquivo.dvc` | Metadados do arquivo (hash, tamanho) |

---

## 📦 Comandos Principais

```bash
# Instalar
pip install dvc

# Inicializar
dvc init

# Adicionar arquivo
dvc add data/data.csv

# Ver status
dvc status

# Push para remote
dvc push

# Pull do remote
dvc pull
```

---

## 🌐 Configuração de Remotes

### Google Cloud Storage

```bash
# Login
gcloud auth login

# Criar bucket (via console)
# Adicionar remote
dvc remote add -d myremote gs://mybucket/path

# Push
dvc push
```

### AWS S3

```bash
# Login
aws configure

# Criar bucket (via console)
# Adicionar remote
dvc remote add -d aws_remote s3://dvc-bucket

# Push
dvc push
```

### Azure Blob Storage

```bash
# Login
az login

# Criar storage account e container
# Adicionar remote
dvc remote add -d azure_remote azure://container-name
dvc remote modify azure_remote account_name 'storage-account'

# Push
dvc push
```

---

## 🔄 Data Pipelines com DVC

### Por que Data Pipelines?

1. **Reprodutibilidade**: Passos documentados e versionados
2. **Eficiência**: Executa apenas steps modificados (caching)
3. **Visualização**: DAG do pipeline visível

### Estrutura de Pipeline

| Arquivo | Função |
|---------|--------|
| `dvc.yaml` | Define pipeline (stages, dependências, outputs) |
| `params.yaml` | Parâmetros do pipeline |
| `dvc.lock` | Lock file com hashes |

### Parâmetros do `dvc run`

| Flag | Descrição |
|------|-----------|
| `-n` | Nome do stage |
| `-d` | Dependências (inputs) |
| `-o` | Outputs |
| `-p` | Arquivo de parâmetros |
| `-m` | Arquivo de métricas |
| `-f` | Forçar overwrite |

### Exemplo de Pipeline

```yaml
# dvc.yaml
stages:
  prepare:
    cmd: python prepare.py
    deps:
      - data/raw.csv
    params:
      - prepare.parking
    outs:
      - data/prepared.csv

  train:
    cmd: python train.py
    deps:
      - data/prepared.csv
    params:
      - train.seed
      - train.steps
    outs:
      - models/model.pickle
    metrics:
      - metrics.json
```

---

## 🚀 Benefícios do DVC

1. **Agnóstico**: Funciona com Python, R, Julia
2. **Sem limite de tamanho**: Dados em storage externo
3. **Versionamento**: Metadados leves no Git
4. **Pipelines**: DAG visual e eficiente
5. **Caching**: Executa apenas steps modificados

---

## 💡 Insights Principais

1. **DVC ≠ Git para dados**: Metadados no Git, dados em storage
2. **Pipelines como código**: YAML define workflow
3. **Reprodutibilidade completa**: Dados + código + parâmetros versionados
4. **Caching inteligente**: Só re-executa steps modificados
5. **Integração MLflow**: DVC para dados, MLflow para modelos

---

## 📝 Tags

`#dvc` `#data-versioning` `#mlops` `#pipelines` `#reproducibility` `#storage`