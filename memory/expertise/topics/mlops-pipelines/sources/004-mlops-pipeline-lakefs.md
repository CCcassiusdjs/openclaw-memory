# MLOps Pipeline: Types, Components & Best Practices - Resumo

**Fonte:** https://lakefs.io/mlops/mlops-pipeline/
**Tipo:** Guide
**Data:** 2026-03-12

---

## 🎯 O que é MLOps Pipeline?

Conjunto de processos e ferramentas para streamlinar o ML lifecycle:
- Development → Deployment → Monitoring

## 📊 Níveis de Automação MLOps

| Nível | Descrição | Ferramentas |
|-------|-----------|-------------|
| **Manual** | Processo experimental, iterativo | Jupyter Notebooks (RAD tools) |
| **ML Pipeline Automation** | Continuous training | Data/model validation stages |
| **CI/CD Pipeline Automation** | Build, test, deploy automáticos | Full automation |

## 🚀 Benefícios dos MLOps Pipelines

| Benefício | Descrição |
|-----------|-----------|
| **Faster time-to-market** | Framework para objetivos mais rápidos, agility, operacional costs menores |
| **Increased productivity** | Standardized development/testing, reusabilidade, reproducibility |
| **Effective model deployment** | Monitoring, troubleshooting, version management, CI/CD integration |

## ⚠️ Desafios Comuns

| Desafio | Descrição | Solução |
|---------|-----------|---------|
| **Data management** | Fontes múltiplas, formatos diferentes | Data integration, validation |
| **Lack of data versioning** | Resultados inconsistentes | Data versioning tools (DVC, lakeFS) |
| **Data quality/accuracy** | Insights imprecisos | Data validation, cleaning techniques |
| **Security & compliance** | Dados sensíveis, GDPR | Anonymization, masking techniques |

## 🔄 Tipos de MLOps Pipelines

### 1. Data Pipelines
- Input → Processing → Feature engineering
- Goal: High data quality/availability

### 2. Model Pipelines
- Training → Evaluation → Updates
- Steps: Model selection, hyperparameter tuning, evaluation

### 3. Experimental Pipelines
- Early stages, model exploration
- Characteristics: Rapid iteration, experimentation
- Use: Model selection, hyperparameter adjustment

### 4. Production Pipelines (Serving Pipelines)
- Deploy trained models to production
- Includes: Monitoring, retraining, continuous delivery

## 📋 MLOps Pipeline Process

### Data Ingestion and Validation
| Fonte | Tipo |
|-------|------|
| Internal/external databases | Estruturado |
| Data marts, warehouses | OLAP |
| OLTP systems | Transacional |
| Spark, HDFS | Big Data |

**Best Practices:**
- Identify data sources
- Document metadata
- Data exploration and validation

### Feature Engineering and Transformation
- Breaking down features (category, date/time)
- Adding feature transformations
- Combining features into new ones
- Feature scaling
- Standardizing/normalizing

### Model Training and Experiment Tracking
- Apply ML algorithm to training data
- Feature engineering integration
- Hyperparameter tuning

## 💡 Conceitos-Chave

1. **Three automation levels** - Manual → ML Pipeline → CI/CD Pipeline
2. **Four pipeline types** - Data, Model, Experimental, Production
3. **Data versioning** - Crítico para reproducibility
4. **Security** - Anonymization/masking para compliance
5. **Feature engineering** - Breaking down, transforming, combining, scaling

## 🔗 Referências Cruzadas

- Complementa: MLOps Principles (002)
- Relacionado a: Feature Stores (021-025)
- Pré-requisito para: Kubeflow Pipelines (039-043)

---

**Conceitos aprendidos:** 10
**Relevância:** Alta (tipos e componentes de pipeline)