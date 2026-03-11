# MLflow Model Registry - Guia Completo (LakeFS)

**Fonte:** GUIDE-001 - MLflow Model Registry: Workflows, Benefits & Challenges  
**URL:** https://lakefs.io/blog/mlflow-model-registry/  
**Tipo:** Blog/Guia  
**Data:** Fevereiro 2025  
**Status:** completed

---

## Resumo

Guia completo sobre MLflow Model Registry: componentes, casos de uso, workflows via UI e API, versionamento, access management, e melhores práticas. Discussão de challenges de data versioning.

---

## Componentes do Model Registry

| Componente | Descrição |
|------------|-----------|
| **Centralized Model Store** | Área única para versionar, compartilhar e deployar modelos |
| **APIs** | CRUD programático de modelos |
| **GUI** | Interface web para visualizar e gerenciar modelos |

### MLflow Componentes (Contexto)

| Componente | Função |
|------------|--------|
| MLflow Tracking | Track experiments (code, data, setup, outcomes) |
| MLflow Projects | Encapsula código independentemente da plataforma |
| MLflow Models | Deploy de modelos para serving environment |
| MLflow Model Registry | Store centralizado para gerenciar modelos |

---

## Casos de Uso

1. **Monitoramento de Iterações**: Track de várias versões de modelos durante desenvolvimento
2. **Multi-environment Deployment**: Track de qual versão está em qual ambiente
3. **Performance Comparison**: Avaliação de performance de versões over time
4. **Staging to Production**: Streamline deployment workflow

---

## Conceitos Fundamentais

### Model Registration
- Cada modelo registrado tem: nome único, tags, aliases, versões, metadata
- Ao registrar primeiro modelo → Version 1
- Novos modelos com mesmo nome → versões incrementadas

### Model Aliases
- Referência nomeada e mutável para uma versão específica
- Ex: `champion` para versão em produção
- Reassign alias → upgrade production model sem mudar código

```python
# Carregar modelo por alias
model = mlflow.pyfunc.load_model("models:/my-model@champion")
```

### Tags
- Key-value pairs para labelar e agrupar modelos
- Ex: `pre_deploy_checks: "PASSED"`

### Descriptions
- Markdown annotations no nível do modelo e versão
- Dataset usado, algoritmo, approach

---

## Workflows

### UI Workflow

1. **Register Model**:
   - Abrir Run details page
   - Artifacts section → escolher model folder
   - Click "Register Model"
   - Opções: Create New Model ou Select Existing

2. **Locate Models**:
   - Registered Models page → lista de modelos e versões
   - Artifacts → model folder → model version link

3. **Deploy & Organize**:
   - Usar aliases e tags na overview page
   - View: creation timestamp, source run, model signature

### API Workflow

```python
import mlflow

# Método 1: log_model
mlflow.log_model(model, "my-model")

# Método 2: register_model
mlflow.register_model(
    model_uri="runs:/{run_id}/model",
    name="my-model"
)

# Método 3: create_registered_model
client = mlflow.tracking.MlflowClient()
client.create_registered_model("my-model")
```

### Carregar Modelos do Registry

```python
# Por versão
model = mlflow.pyfunc.load_model("models:/my-model/1")

# Por alias
model = mlflow.pyfunc.load_model("models:/my-model@champion")

# Carregamento genérico
from mlflow.models import load_model
model = load_model("models:/my-model@champion")
```

---

## Databricks Unity Catalog Integration

```python
# Configurar environment variables
os.environ["DATABRICKS_HOST"] = "..."
os.environ["DATABRICKS_TOKEN"] = "..."

# OU OAuth
os.environ["DATABRICKS_CLIENT_ID"] = "..."
os.environ["DATABRICKS_CLIENT_SECRET"] = "..."

# Registry URI
mlflow.set_registry_uri("databricks-uc")
```

---

## Access Management

### Permissões Padrão
- Default: READ para todos os usuários
- Configurável via configuration file
- Resources: Experiment, Registered Model

### APIs de Autenticação

```python
from mlflow.server import get_app_client

auth_client = get_app_client("AuthServiceClient")
# Gerenciar usuários e permissões
```

---

## Challenges de Data Versioning

1. **Scaling para Big Datasets**: storage e performance com múltiplas versões
2. **Automação**: track de lineage, modificações, dependencies
3. **Schema Changes**: gerenciar conflicts, backfilling, impact em downstream
4. **Tooling Integration**: ETL processes, pipelines

---

## Best Practices

### 1. Test in Staging Environments
- Staging como cópia de production
- Remover errors antes de customer-facing

### 2. Centralize Experiment Tracking
- Track information centralizado para comparação
- Facilita collaboration e knowledge sharing

### 3. Model Versioning Automation
- Automatizar versionamento de data/modelos
- Track transformations, preprocessing

### 4. Production Promotion Workflow
- CI/CD para spread ML code across environments
- Productionize última versão automaticamente

---

## Ambiente Multi-Environment

```
dev → staging → prod
```

- Access-controlled contexts via MLflow Authentication
- Registered models por environment + business problem
- Permissions configuradas por contexto
- Promotion automático via CI/CD

---

## Conceitos Adicionados

- Model aliases for deployment workflows
- Unity Catalog integration patterns
- Multi-environment promotion
- Access control patterns (READ default)
- Data versioning challenges in ML
- Staging environment best practice

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 25 min