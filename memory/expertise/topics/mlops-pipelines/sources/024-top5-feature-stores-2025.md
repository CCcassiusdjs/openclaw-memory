# Top 5 Feature Stores in 2025 - Resumo

**Fonte:** https://www.gocodeo.com/post/top-5-feature-stores-in-2025-tecton-feast-and-beyond
**Tipo:** Guide
**Data:** 2026-03-12

---

## 🎯 Por que Feature Stores?

Feature Stores são o **backbone de MLOps pipelines escaláveis**:
- **Centralized layer** para features: store, version, serve, monitor
- **Feature reuse** across models
- **Eliminate data leakage**
- **Operationalize ML reliably**

## 📊 Top 5 Feature Stores 2025

### 1. Feast - The Open Source Champion

| Aspect | Detalhes |
|--------|---------|
| **Origem** | Gojek → Linux Foundation |
| **Tipo** | Open source |
| **Foco** | Modularidade, transparência, controle |

**Pontos Fortes:**
- Online + offline feature retrieval
- Point-in-time correctness (sem feature leakage)
- Pluggable architecture (Spark, Kafka, Redis, Snowflake)
- No vendor lock-in

**Use Cases:**
- Real-time fraud detection (Redis)
- Batch recommendations (BigQuery)
- Experimentation platforms

---

### 2. Tecton - The Enterprise-Grade Platform

| Aspect | Detalhes |
|--------|---------|
| **Origem** | Criadores do Uber Michelangelo |
| **Tipo** | Managed, enterprise |
| **Foco** | Production-ready, lifecycle management |

**Pontos Fortes:**
- **Declarative DSL** (Python, SQL, Spark)
- **Real-time streaming** (seconds latency)
- **CDC** (Change Data Capture)
- GitOps-style management
- Materialization scheduling
- Monitoring + lineage tracking

**Use Cases:**
- Dynamic pricing (< 1s freshness)
- Personalized search/recommendations
- Real-time clickstream processing

**Clientes:** PayPal, Atlassian, DoorDash

---

### 3. Hopsworks - Integrated MLOps Platform

| Aspect | Detalhes |
|--------|---------|
| **Origem** | Hopsworks |
| **Tipo** | On-prem / managed |
| **Foco** | Governance, regulated industries |

**Pontos Fortes:**
- **End-to-end** feature + model management
- **Data lineage** + drift detection
- **Audit logging** + usage analytics
- Native TFX + MLflow integration
- HopsFS distributed file system

**Use Cases:**
- Healthcare, finance, manufacturing
- AI governance workflows

**Clientes:** Siemens, Intel, Safran

---

### 4. Databricks Feature Store - Lakehouse-First

| Aspect | Detalhes |
|--------|---------|
| **Origem** | Databricks |
| **Tipo** | Lakehouse-native |
| **Foco** | Spark/Delta Lake ecosystems |

**Pontos Fortes:**
- Native Delta tables + Spark DataFrames
- MLflow tracking integration
- ACID transactions
- Lineage tracking

**Best for:**
- Spark SQL / PySpark teams
- Enterprise data lake → production ML
- Large historical datasets

---

### 5. (Preview only - fonte truncada)
Possivelmente AWS SageMaker Feature Store ou similar.

## 📈 Feature Store Comparison Matrix

| Feature Store | Tipo | Real-time | Open Source | Best For |
|---------------|------|-----------|-------------|----------|
| **Feast** | Open source | ✅ | ✅ | Startups, flexibility |
| **Tecton** | Enterprise | ✅ (sub-second) | ❌ | Enterprise, streaming |
| **Hopsworks** | Hybrid | ✅ | ✅ (core) | Regulated industries |
| **Databricks** | Lakehouse | ✅ | ❌ | Spark teams |

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Feature Engineering** | Transform raw data into ML features |
| **Point-in-time correctness** | Avoid data leakage in training |
| **Online Store** | Low-latency serving (Redis, DynamoDB) |
| **Offline Store** | Batch training data (BigQuery, Delta Lake) |
| **Materialization** | Schedule feature updates |
| **CDC** | Change Data Capture for streaming |

## 🔗 Referências Cruzadas

- Complementa: Feast Official (021)
- Relacionado a: Feature Store Comparison (022)
- Pré-requisito para: MLOps pipelines

---

**Conceitos aprendidos:** 15
**Relevância:** Alta (market overview)