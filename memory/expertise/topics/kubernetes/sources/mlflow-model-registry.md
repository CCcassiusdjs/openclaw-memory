# MLflow Model Registry: Overview

**Fonte:** https://mlflow.org/docs/latest/ml/model-registry/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

MLflow Model Registry é um modelo store centralizado, APIs e UI para gerenciar o ciclo de vida completo de modelos ML.

## Por que Model Registry?

Problemas sem registry:
- Gerenciamento manual error-prone
- Ineficiente em escala
- Falta de governança
- Dificuldade de colaboração

### Benefícios

| Benefício | Descrição |
|-----------|-----------|
| 🗂️ **Version Control** | Track automático de versões, rollback, parallel versions |
| 🧬 **Model Lineage** | Rastreabilidade completa: run → params → data → model |
| 🚀 **Production Workflows** | Aliases, tags, staging → production transitions |
| 🛡️ **Governance** | Metadados estruturados, RBAC (em Databricks) |

## Conceitos

### Model
- Criado com `mlflow.<flavor>.log_model()`
- Ou `mlflow.create_external_model()` (MLflow 3+)
- Pode ser registrado no Model Registry

### Registered Model
- Nome único
- Contém versões, aliases, tags, metadados
- Criado ao registrar um model

### Model Version
- Incrementado automaticamente (v1, v2, ...)
- Cada versão tem tags próprias
- Exemplo: `pre_deploy_checks: "PASSED"`

### Model URI
```
models:/<model-name>/<model-version>
models:/MyModel/1
```

### Model Alias
- Referência nomeada para uma versão
- Mutável (pode ser atualizado)
- Exemplo: `@champion` → versão 1

```python
# URI com alias
models:/MyModel@champion
```

### Tags
- Key-value pairs para models e versions
- Categorização por função ou status
- Exemplo: `task:question-answering`
- Version tags: `validation_status:approved`

### Annotations
- Markdown descriptions
- Metadados relevantes
- Algorithm descriptions, datasets, methodology

## MLflow OSS vs Databricks

| Feature | OSS MLflow | Databricks |
|---------|------------|------------|
| **Registry UI** | ✅ | ✅ |
| **Version Control** | ✅ | ✅ |
| **Tags/Annotations** | ✅ | ✅ |
| **Unity Catalog** | ❌ | ✅ |
| **Cross-workspace** | ❌ | ✅ |
| **Fine-grained RBAC** | ❌ | ✅ |
| **Model Lineage** | Parcial | ✅ Completo |

## Python APIs

### Registrar um Modelo

```python
import mlflow

# Opção 1: Especificar nome ao logar
mlflow.<flavor>.log_model(
    ...,
    registered_model_name="MyModel"
)

# Opção 2: Registrar modelo já logado
mlflow.register_model(
    model_uri="runs:/<run-id>/model",
    name="MyModel"
)
```

### Carregar Modelo

```python
# Por versão
model = mlflow.<flavor>.load_model("models:/MyModel/1")

# Por alias
model = mlflow.<flavor>.load_model("models:/MyModel@champion")
```

### Databricks Unity Catalog

```python
import mlflow

mlflow.set_registry_uri("databricks-uc")

mlflow.<flavor>.log_model(
    ...,
    registered_model_name="catalog.schema.model_name"
)
```

## Benefícios para Enterprises

### Governança
- Policies de acesso
- Permission controls
- Audit trails

### Colaboração
- Cross-workspace access
- Shared catalogs
- Reutilização de modelos

### Compliance
- Rastreabilidade completa
- Metadados estruturados
- Version history

## Casos de Uso

### Solo Data Scientist
- Track de experiments
- Version models
- Compare iterations

### ML Platform Team
- Governança centralizada
- Deployment workflows
- Cross-team collaboration

### Enterprise
- Compliance requirements
- RBAC
- Unity Catalog integration

## Insights

- Model Registry é foundation para MLOps mature
- Aliases são úteis para deployment workflows
- Databricks Unity Catalog adiciona enterprise features
- OSS é suficiente para projetos pequenos/médios
- Lineage é critical para debugging e reproducibility
- Tags permitem organization por função/status