# MLflow Artifact Store - Resumo

**Fonte:** https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é Artifact Store

Componente do MLflow Tracking que armazena artifacts grandes:
- **Model weights** (pickled models)
- **Images** (PNGs, plots)
- **Data files** (Parquet, CSV)

**Nota:** Metadata (params, metrics, tags) ficam no Backend Store.

---

## Configuração

### Default

```python
# Local filesystem (default)
# Artifacts salvos em ./mlruns
mlflow.log_artifact("model.pkl")
```

### Remote Storage

```bash
# S3
mlflow server --default-artifact-root s3://my-bucket/mlflow

# Azure Blob
mlflow server --default-artifact-root wasbs://container@account.blob.core.windows.net/mlflow

# GCS
mlflow server --default-artifact-root gs://my-bucket/mlflow
```

---

## Gerenciando Acesso

### S3 / AWS

```bash
# Credenciais via environment
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx

# Ou IAM role (EC2)
# Ou ~/.aws/credentials
```

### Azure Blob Storage

```bash
# Opção 1: Connection String
export AZURE_STORAGE_CONNECTION_STRING="..."

# Opção 2: Access Key
export AZURE_STORAGE_ACCESS_KEY="..."

# Opção 3: DefaultAzureCredential (requer azure-identity)
pip install azure-identity azure-storage-blob
```

### Google Cloud Storage

```bash
# Configurar credenciais GCP
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# Instalar dependência
pip install google-cloud-storage
```

---

## Storage Types Suportados

### Amazon S3

```bash
# URI
s3://<bucket>/<path>

# Credenciais (ordem de precedência)
# 1. IAM role
# 2. ~/.aws/credentials
# 3. AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY
```

#### S3 Upload Extra Args

```bash
# KMS Encryption
export MLFLOW_S3_UPLOAD_EXTRA_ARGS='{"ServerSideEncryption": "aws:kms", "SSEKMSKeyId": "1234"}'
```

#### Bucket Ownership Verification

```bash
# Proteção contra bucket takeover
export MLFLOW_S3_EXPECTED_BUCKET_OWNER=123456789012
```

#### Custom S3 Endpoints (MinIO, Digital Ocean)

```bash
# Digital Ocean Spaces
export MLFLOW_S3_ENDPOINT_URL=https://<region>.digitaloceanspaces.com

# MinIO
export MLFLOW_S3_ENDPOINT_URL=http://1.2.3.4:9000

# Self-signed certs
export MLFLOW_S3_IGNORE_TLS=true
# ou
export AWS_CA_BUNDLE=/path/to/ca-bundle.pem

# Non-default region
export AWS_DEFAULT_REGION=my_region
```

### Azure Blob Storage

```bash
# URI
wasbs://<container>@<storage-account>.blob.core.windows.net/<path>

# Timeout (segundos)
export MLFLOW_ARTIFACT_UPLOAD_DOWNLOAD_TIMEOUT=600
```

### Google Cloud Storage

```bash
# URI
gs://<bucket>/<path>

# Instalar
pip install google-cloud-storage

# Timeout e Chunk Size
export MLFLOW_ARTIFACT_UPLOAD_DOWNLOAD_TIMEOUT=60      # segundos
export MLFLOW_GCS_UPLOAD_CHUNK_SIZE=104857600          # 100MB
export MLFLOW_GCS_DOWNLOAD_CHUNK_SIZE=104857600        # 100MB
```

### FTP Server

```bash
# URI
ftp://user@host/path/to/directory

# Com senha (não recomendado)
ftp://user:pass@host/path/to/directory
```

### SFTP Server

```bash
# URI
sftp://user@host/path/to/directory

# Requer SSH key-based auth
# Instalar: pip install pysftp
```

### NFS

```bash
# Path deve ser igual em server e client
/mnt/nfs/mlflow-artifacts
```

### HDFS

```bash
# URI
hdfs://<host>:<port>/<path>
# ou
hdfs:///<path>

# Kerberos auth
export MLFLOW_KERBEROS_TICKET_CACHE=/tmp/krb5cc_22222222
export MLFLOW_KERBEROS_USER=user_name

# Dependência
pip install pyarrow
```

---

## Timeout Configuration

```bash
# Timeout para upload/download (segundos)
export MLFLOW_ARTIFACT_UPLOAD_DOWNLOAD_TIMEOUT=600
```

**Defaults:**
- Azure Blob: 600 segundos
- GCS: 60 segundos
- S3: Usa boto3 default

---

## Multipart Upload

Para artifacts grandes com proxied artifact access:

```bash
export MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD=true
```

**Funciona com:**
- Amazon S3
- Google Cloud Storage

**Configurações:**
```bash
# Tamanho mínimo para multipart (default: 500MB)
export MLFLOW_MULTIPART_UPLOAD_MINIMUM_FILE_SIZE=524288000

# Chunk size (default: 100MB)
export MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE=104857600
```

---

## Default Artifact Location

```python
# Por experiment
mlflow.create_experiment(
    "my-experiment",
    artifact_location="s3://my-bucket/experiments/"
)

# Recuperar URI
artifact_uri = mlflow.get_artifact_uri()
```

**Importante:** Se não especificar, MLflow usa local file system, que pode não ser acessível pelo server.

---

## Deletion Behavior

Artifacts **não** são deletados automaticamente quando run é deletado.

```bash
# Remover permanentemente artifacts de runs deletados
mlflow gc [options]
```

---

## Quick Reference

```bash
# S3
mlflow server --default-artifact-root s3://my-bucket/mlflow \
              --backend-store-uri postgresql://...

# Azure
mlflow server --default-artifact-root wasbs://container@account.blob.core.windows.net/mlflow

# GCS
mlflow server --default-artifact-root gs://my-bucket/mlflow

# MinIO
export MLFLOW_S3_ENDPOINT_URL=http://minio:9000
mlflow server --default-artifact-root s3://mlflow-artifacts/
```

```python
# Python - logar artifacts
import mlflow

# Arquivo único
mlflow.log_artifact("model.pkl")

# Diretório
mlflow.log_artifacts("./outputs/")

# Com path
mlflow.log_artifact("model.pkl", artifact_path="models/")
```

---

## Conceitos Aprendidos

1. **Artifact Store** - Armazena artifacts grandes (models, images, data)
2. **Backend Store vs Artifact Store** - Metadata vs Artifacts
3. **S3** - Suporta MinIO, Digital Ocean, custom endpoints
4. **Azure Blob** - Connection string, access key, DefaultAzureCredential
5. **GCS** - Credenciais GCP, chunk size configurável
6. **FTP/SFTP** - Suporte básico
7. **NFS** - Path deve ser idêntico em server e client
8. **HDFS** - Suporte Kerberos, PyArrow
9. **Multipart Upload** - Para artifacts grandes (S3, GCS)
10. **Timeout** - Configurável por storage
11. **Bucket Ownership** - Proteção contra bucket takeover