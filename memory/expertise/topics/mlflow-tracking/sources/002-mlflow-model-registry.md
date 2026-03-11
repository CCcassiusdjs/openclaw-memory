# MLflow Model Registry - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/model-registry/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é Model Registry

Centralized model store para gerenciar o ciclo de vida completo de ML models. Fornece:
- Lineage (qual experiment/run produziu o modelo)
- Versioning
- Aliasing
- Metadata tagging
- Stage transitions

---

## Por que usar Model Registry?

1. **Version Control** - Track automático de versões, rollback, parallel versions
2. **Model Lineage** - Rastreabilidade completa (dados, parâmetros, run)
3. **Production-Ready Workflows** - Aliases (@champion), tags, stage transitions
4. **Governance & Compliance** - Metadados estruturados, RBAC (Databricks)

---

## Conceitos Principais

| Conceito | Descrição |
|----------|-----------|
| **Model** | Criado com `mlflow.<flavor>.log_model()` ou `mlflow.create_external_model()` |
| **Registered Model** | Modelo registrado com nome único, versões, aliases, tags |
| **Model Version** | Cada registro incrementa versão (1, 2, 3...) |
| **Model URI** | `models:/<model-name>/<model-version>` ou `models:/<model-name>@<alias>` |
| **Model Alias** | Referência nomeada mutável (ex: `@champion`) |
| **Tags** | Key-value pairs para categorização |
| **Annotations** | Descrições em Markdown |

---

## API Principal

### Registrar Modelo

```python
# Opção 1: parâmetro no log_model
mlflow.sklearn.log_model(model, "model", registered_model_name="MyModel")

# Opção 2: registro explícito
mlflow.register_model(model_uri="runs:/<run-id>/model", name="MyModel")
```

### Carregar Modelo

```python
# Por versão
model = mlflow.sklearn.load_model("models:/MyModel/1")

# Por alias
model = mlflow.sklearn.load_model("models:/MyModel@champion")
```

---

## Model Registry em Databricks

Databricks integra com Unity Catalog:
- Enhanced governance (políticas de acesso)
- Cross-workspace access
- Model lineage (notebooks, datasets, experiments)
- Discovery e reuse

```python
mlflow.set_registry_uri("databricks-uc")
mlflow.sklearn.log_model(model, "model", registered_model_name="catalog.schema.model")
```

---

## Conceitos Aprendidos

1. **Centralized Model Store** - Única fonte de verdade para modelos
2. **Versioning** - Automático, incremental
3. **Aliases** - Referências mutáveis para deployment (@champion, @challenger)
4. **Model URI** - `models:/name/version` ou `models:/name@alias`
5. **Databricks Unity Catalog** - Governance enterprise
6. **Lineage** - Rastreabilidade completa do modelo

---

## Workflow Típico

1. Treinar modelo → `mlflow.log_model()`
2. Registrar → `mlflow.register_model()`
3. Adicionar tags/descrição
4. Promover para Staging → testar
5. Promover para Production → alias @champion
6. Monitorar → rollback se necessário