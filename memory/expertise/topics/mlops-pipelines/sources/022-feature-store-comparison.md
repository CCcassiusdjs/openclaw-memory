# Feature Store Comparison - Overview

**Fonte:** https://www.featurestorecomparison.com/
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Site de comparação de Feature Stores. Lista as principais soluções disponíveis com suas características: open-source vs managed, online/offline support, tecnologias suportadas.

---

## 🏪 Feature Stores Listados

| Feature Store | Tipo | Online/Offline | Tecnologias |
|---------------|------|----------------|-------------|
| **Databricks Feature Store** | Managed Cloud | ✅ Both | PySpark, Spark, Spark Streaming |
| **Feast** | Open-source | ✅ Both | Kubernetes |
| **Iguazio** | Managed | ✅ Both | Kubernetes |
| **Kaskada** | AWS Managed | ✅ Online | Python |
| **Rasgo** | Managed Cloud | ✅ Both | Cloud Data Warehouse |
| **SageMaker Feature Store** | AWS Only | ✅ Both | PySpark, Python, SQL |
| **Tecton** | Managed Cloud | ✅ Both | PySpark (Databricks/EMR) |
| **Vertex AI** | GCP Managed | ✅ Both | - |

---

## 🔍 Análise por Tipo

### Open-Source
**Feast**
- Framework open-source
- Registrar, ingerir, servir, monitorar features
- Sem UI nativa
- Não suporta feature engineering (só ingere features prontas)

### Cloud-Managed

**Databricks Feature Store**
- Unity Catalog integration
- Feature sharing e discovery
- Mesmo código para training e inference
- Governance e lineage built-in

**SageMaker Feature Store**
- AWS-only
- Fully managed
- SQL support
- PySpark/Python

**Tecton**
- Managed feature store
- PySpark para compute (Databricks/EMR)
- DynamoDB para online serving
- Python DSL para feature transformations

**Vertex AI Feature Store**
- GCP managed ML platform
- Feature store integrado

---

## 💡 Insights Principais

1. **Open-source (Feast)**: Flexível, mas sem UI e feature engineering
2. **Managed solutions**: Mais features, mas vendor lock-in
3. **Online + Offline**: Essencial para real-time ML
4. **Databricks + Tecton**: Líderes em feature engineering
5. **SageMaker**: Melhor para AWS-only shops

---

## 📝 Tags

`#feature-store` `#comparison` `#feast` `#tecton` `#sagemaker` `#databricks` `#mlops`