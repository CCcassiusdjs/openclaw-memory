# MLflow Backend Store - Resumo

**Fonte:** https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é Backend Store

Componente core do MLflow que armazena metadata de Runs, Models, Traces e Experiments:
- Run ID, Model ID, Trace ID
- Tags, Start & End Time
- Parameters, Metrics

**Nota:** Artifacts grandes (model weights) são armazenados no Artifact Store.

---

## Tipos de Backend Stores

### Relational Database (Default)

MLflow suporta databases via SQLAlchemy:
- **SQLite** (default)
- **PostgreSQL**
- **MySQL**
- **MSSQL**

**Vantagens:**
- Melhor performance (indexação)
- Escalabilidade
- Confiabilidade

**Default (MLflow 3.7+):**
```bash
# SQLite por default
mlflow server --port 5000
# Cria automaticamente sqlite:///mlflow.db
```

### Local File System (Legacy)

Armazena metadata em arquivos locais (`./mlruns`).

**Aviso:** Em modo KTLO (Keep-the-Light-On), sem novos features. Recomenda-se migrar para database.

```bash
mlflow server --backend-store-uri ./mlruns
# ou
export MLFLOW_TRACKING_URI=./mlruns
```

---

## Configuração

### Métodos

1. **Environment Variable:**
   ```bash
   export MLFLOW_TRACKING_URI=postgresql://user:pass@host:5432/mlflow
   ```

2. **Python API:**
   ```python
   import mlflow
   mlflow.set_tracking_uri("postgresql://user:pass@host:5432/mlflow")
   ```

3. **CLI Flag:**
   ```bash
   mlflow server --backend-store-uri postgresql://user:pass@host:5432/mlflow
   ```

### Supported URIs

| Tipo | Formato |
|------|---------|
| **Local File** | `file:/my/local/dir` |
| **Database** | `<dialect>+<driver>://<user>:<pass>@<host>:<port>/<db>` |
| **HTTP Server** | `https://my-server:5000` |
| **Databricks** | `databricks` ou `databricks://<profile>` |

---

## Database Requirements

### Model Registry Integration

Model Registry **requer** database-backed store.

### Schema Migrations

```bash
# Sempre fazer upgrade antes de iniciar
mlflow db upgrade postgresql://user:pass@host:5432/mlflow

# Backup antes de migrations!
pg_dump mlflow > backup.sql
```

### Parameter Limits

- Max param value length: 6000 caracteres
- Max param key length: 8k caracteres
- Migration pode levar tempo em databases grandes

---

## SQLAlchemy Options

Configurar connection pooling via environment variables:

| MLflow Variable | SQLAlchemy Option |
|-----------------|-------------------|
| `MLFLOW_SQLALCHEMYSTORE_POOL_SIZE` | `pool_size` |
| `MLFLOW_SQLALCHEMYSTORE_POOL_RECYCLE` | `pool_recycle` |
| `MLFLOW_SQLALCHEMYSTORE_MAX_OVERFLOW` | `max_overflow` |

---

## MySQL SSL Options

```bash
# SSL Certificates
export MLFLOW_MYSQL_SSL_CA=/path/to/ca.pem
export MLFLOW_MYSQL_SSL_CERT=/path/to/client-cert.pem
export MLFLOW_MYSQL_SSL_KEY=/path/to/client-key.pem

# Iniciar servidor
mlflow server --backend-store-uri="mysql+pymysql://username@hostname:port/database" \
              --default-artifact-root=s3://your-bucket \
              --host=0.0.0.0 --port=5000
```

---

## File Store Performance

### LibYAML

MLflow usa LibYAML para melhor performance em file stores.

**Instalar:**
```bash
# Ubuntu/Debian
apt-get install libyaml-cpp-dev libyaml-dev

# macOS
brew install yaml-cpp libyaml

# Reinstalar PyYAML
pip --no-cache-dir install --force-reinstall -I pyyaml
```

**Nota:** Recomenda-se usar database backend para melhor performance.

---

## Deletion Behavior

Runs deletados **não** removem artifacts automaticamente.

**Garbage Collection:**
```bash
mlflow gc [options]
```

Remove permanentemente metadata e artifacts de runs deletados.

---

## Quick Reference

```bash
# SQLite (default)
mlflow server --port 5000

# PostgreSQL
mlflow server --port 5000 \
              --backend-store-uri postgresql://user:pass@host:5432/mlflow

# MySQL com SSL
export MLFLOW_MYSQL_SSL_CA=/path/to/ca.pem
mlflow server --port 5000 \
              --backend-store-uri "mysql+pymysql://user@host:3306/mlflow"

# Schema Migration
mlflow db upgrade postgresql://user:pass@host:5432/mlflow
```

```python
# Conectar via Python
import mlflow
mlflow.set_tracking_uri("postgresql://user:pass@host:5432/mlflow")

# File Store (legacy)
mlflow.set_tracking_uri("file:///path/to/mlruns")
```

---

## Conceitos Aprendidos

1. **Backend Store** - Armazena metadata (params, metrics, tags)
2. **SQLite Default** - MLflow 3.7+ usa SQLite por default
3. **File Store Legacy** - `./mlruns` em modo KTLO
4. **Database Types** - SQLite, PostgreSQL, MySQL, MSSQL
5. **Model Registry** - Requer database backend
6. **Schema Migrations** - `mlflow db upgrade` antes de iniciar
7. **Connection Pooling** - Configurável via environment variables
8. **MySQL SSL** - Certificados via environment variables
9. **LibYAML** - Melhora performance em file stores
10. **Garbage Collection** - `mlflow gc` para deletar permanentemente