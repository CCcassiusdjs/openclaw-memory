# MLflow Model Registry - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/model-registry/
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 O que é MLflow Model Registry?

**Centralized model store** + APIs + UI para gerenciar o **full lifecycle de ML models**:
- Lineage (qual experiment/run produziu o modelo)
- Versioning
- Aliasing
- Metadata tagging
- Annotations

## 📋 Por que Model Registry?

### Problemas sem Registry
- Gerenciar models manualmente é error-prone
- Diferentes environments, teams, iterations
- Falta de traceabilidade

### Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **🗂️ Version Control** | Track versions, rollback, parallel versions |
| **🧬 Model Lineage** | Link to experiment/run, reproducibility |
| **🚀 Production Workflows** | Aliases (@champion), tags para deployment |
| **🛡️ Governance** | Metadata, tagging, role-based access |

## 🔧 Concepts

| Conceito | Descrição |
|----------|-----------|
| **Model** | Criado com `mlflow.<flavor>.log_model()` ou `mlflow.create_external_model()` |
| **Registered Model** | Model registrado com nome único, versions, aliases, tags |
| **Model Version** | Versão específica de um registered model (version 1, 2, 3...) |
| **Model URI** | `models:/<model-name>/<model-version>` ou `models:/<model-name>@<alias>` |
| **Model Alias** | Named reference para uma version (ex: @champion) |
| **Tags** | Key-value pairs para categorizar models e versions |
| **Annotations** | Markdown descriptions com info adicional |

## 🚀 Model Registry in Practice

### OSS MLflow

```python
# Option 1: specify registered_model_name when logging
mlflow.<flavor>.log_model(..., registered_model_name="MyModel")

# Option 2: register a logged model
mlflow.register_model(model_uri="runs:/<run-id>/model", name="MyModel")

# Load model
mlflow.<flavor>.load_model("models:/MyModel/1")

# Use alias
mlflow.<flavor>.load_model("models:/MyModel@champion")
```

### Databricks Unity Catalog Integration

**Benefits:**
- 🛡️ Enhanced governance (access policies)
- 🌐 Cross-workspace access
- 🔗 Model lineage
- 🔍 Discovery and reuse

```python
# Set tracking uri to Databricks
mlflow.set_tracking_uri("databricks")

# Register to Unity Catalog
mlflow.<flavor>.log_model(..., registered_model_name="catalog.schema.model_name")
```

## 📊 Model Lifecycle

```
Development → Staging → Production → Archived
     ↓            ↓          ↓           ↓
  Experiment   Validate   Deploy   Retire/Archive
```

### Stages (OSS)
| Stage | Descrição |
|-------|-----------|
| **None/Archived** | Modelo inicial ou arquivado |
| **Staging** | Validação antes de production |
| **Production** | Deploy em produção |

### Aliases (Modern approach)
| Alias | Uso |
|-------|-----|
| **@champion** | Modelo em produção |
| **@challenger** | Modelo candidato a substituir |
| **@latest** | Última versão |

## 💡 Concepts-Chave

| Conceito | Descrição |
|----------|-----------|
| **Registered Model** | Container para todas versions |
| **Model Version** | Versão específica |
| **Alias** | Named reference mutável |
| **Tags** | Metadata key-value |
| **URI** | `models:/name/version` ou `models:/name@alias` |
| **Lineage** | Trace para experiment/run |

## 🔗 Referências Cruzadas

- Complementa: MLflow Tracking (031)
- Relacionado a: MLflow Projects (032)
- Pré-requisito para: MLflow Serving (018)

---

**Conceitos aprendidos:** 15
**Relevância:** Alta (core MLflow functionality)