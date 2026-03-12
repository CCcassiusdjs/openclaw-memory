# MLflow Model Registry: Workflows, Benefits & Challenges

**Fonte:** https://lakefs.io/blog/mlflow-model-registry/
**Autor:** lakeFS Blog
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Guia completo sobre MLflow Model Registry para gerenciamento de lifecycle de modelos. Explica componentes, workflows via UI e API, versioning, aliases, stages, e integração com lakeFS para data versioning.

---

## 🎯 O que é Model Registry?

**Definição:** Serviço do MLflow que permite gerenciar e trackear modelos ML, artifacts associados, com UI para navegação.

### Componentes Principais

1. **Centralized Model Store**: Área única para versionar, compartilhar e deployar modelos
2. **APIs**: CRUD programático para modelos
3. **GUI**: Interface visual para gerenciamento manual

### Os 4 Componentes do MLflow

| Componente | Descrição |
|------------|-----------|
| **MLflow Tracking** | Trackear experimentos, código, dados, setup, outcomes |
| **MLflow Projects** | Encapsular código independente de plataforma |
| **MLflow Models** | Deployar modelos para serving environments |
| **Model Registry** | Armazenar, anotar, encontrar, gerenciar modelos |

---

## 🔧 Quando Usar Model Registry?

- Monitorar múltiplas iterações de modelo
- Trackear versões em múltiplos ambientes
- Avaliar performance de iterações ao longo do tempo
- Streamlining deployment para staging/production

---

## 📦 Funcionalidades

### Model Registration
- Nome único para cada registered model
- Tags, aliases, versions, metadata

### Version of the Model
- Cada modelo pode ter múltiplas versões
- Versão 1 para novo modelo, incrementa com cada registro
- Tags por versão (ex: pre_deploy_checks: "PASSED")

### Model Aliases
- Referência nomeada e mutável para versão específica
- Útil para deployment (ex: "champion" → production)
- Reassign alias = upgrade production sem mudar código

### Descriptions e Annotations
- Markdown para top-level model e cada versão
- Dataset, algorithm, approach documentation

---

## 🔄 Workflows

### UI Workflow

#### Register a Model
1. Abrir MLflow Run details
2. Artifacts section → escolher model folder
3. Click "Register Model"
4. Opções: Create New Model ou Select Existing

#### Locate Registered Models
- Registered Models page para ver modelos e versões
- Artifacts section → model folder → model version

#### Deploy and Organize
- Aliases e tags na overview page
- Click pencil ou Add link para modificar

### API Workflow

#### Registrar Modelos Programaticamente

```python
# Método 1: log_model()
mlflow.log_model(model, "model_name", registered_model_name="MyModel")

# Método 2: register_model()
mlflow.register_model("runs:/run-id/model", "MyModel")

# Método 3: create_registered_model()
client = MlflowClient()
client.create_registered_model("MyModel")
```

#### Carregar Modelos

```python
# Por versão
model = mlflow.pyfunc.load_model("models:/MyModel/1")

# Por alias
model = mlflow.pyfunc.load_model("models:/MyModel/champion")
```

---

## 🏷️ Stages e Aliases

### Stages (Legacy)
- **None**: Recém registrado
- **Staging**: Em testes
- **Production**: Em produção
- **Archived**: Não mais usado

### Aliases (Modern)
- Referências nomeadas mais flexíveis
- "champion", "challenger", etc.
- Permitem trocar versão sem mudar código de inference

---

## 🔄 Promoção Entre Ambientes

### Ambientes Típicos
- **Dev**: Desenvolvimento
- **Staging**: Testes/QA
- **Prod**: Produção

### Promoção com CI/CD
1. CI/CD treina e registra em cada ambiente
2. Source control espalha código
3. Promoção via aliases (champion → production)

---

## 🗑️ Deletar Modelos

**Atenção:** Deleção é irreversível!

```python
# Deletar versão específica
client.delete_model_version(name="MyModel", version="1")

# Deletar modelo inteiro (todas versões)
client.delete_registered_model(name="MyModel")
```

---

## 🛡️ Access Management

### Permissões Padrão
- Todos usuários: READ por default
- Configurável via config file

### Recursos Suportados
- Experiment
- Registered Model

### AuthServiceClient
```python
client = mlflow.server.get_app_client("auth")
client.create_user("username", "password")
client.grant_permission("username", "registered_model", "MyModel", "READ")
```

---

## ⚠️ Desafios de Data Versioning

1. **Scaling para Big Datasets**: Storage e performance
2. **Automação**: Datasets grandes e dinâmicos
3. **Schema Changes**: Dependências e backfilling
4. **Tooling Integration**: ETL, pipelines, data warehouse

---

## ✅ Best Practices

### 1. Test in Staging
- Staging environment antes de production
- Remove errors e failures antes de customer-facing

### 2. Centralize Experiment Tracking
- Same experiment name across users
- Shared table for comparison

### 3. Specific Pipeline Parameter Storage
- Cloud storage dedicado para artifacts
- Evita acumulação excessiva

### 4. Tune Entire Pipeline
- Não apenas módulos isolados
- MLflow centraliza tracking

### 5. Automate Version Control
- Write-Audit-Publish pattern
- Automated ETL testing, data validation, deployment

---

## 🔗 lakeFS Integration

**O que é:** Open-source data versioning com Git-like semantics (commit, merge, branch)

**Benefícios:**
- Manage data com Git workflows
- Zero-clone copies (sem duplicação)
- Petabytes de data
- Integração com MLflow

---

## 💡 Insights Principais

1. **Model Registry = lifecycle management** para modelos ML
2. **Aliases > Stages**: Moderno e mais flexível
3. **Centralização**: Todos modelos em um lugar
4. **CI/CD ready**: Promoção entre ambientes automatizada
5. **lakeFS complementa**: Data versioning para datasets

---

## 📝 Tags

`#mlflow` `#model-registry` `#mlops` `#versioning` `#model-management` `#deployment`