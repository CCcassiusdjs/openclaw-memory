# Feast - Open Source Feature Store - Resumo

**Fonte:** https://feast.dev/
**Tipo:** Official Documentation
**Data:** 2026-03-12

---

## 🎯 O que é Feast?

**Feast** (Feature Store) é o **leading open-source feature store** para ML:
- Desenvolvido originalmente por Gojek
- Agora parte da Linux Foundation
- Propósito: definir, registrar, e recuperar features de qualquer backend

## 🔧 Capacidades Principais

### Online + Offline Features
| Tipo | Uso | Latência |
|------|-----|----------|
| **Offline** | Training data | Batch pipelines |
| **Online** | Inference | Low-latency APIs |

### Pont-in-Time Correctness
- Resolve o problema de **feature leakage** durante model training
- Crítico para production ML

### RAG Support (Vector Search)
```python
features = store.retrieve_online_documents(
    features=[
        "corpus:document_id",
        "corpus:chunk_id",
        "corpus:chunk_text",
        "corpus:chunk_embedding",
    ],
    query="What is the biggest city in the USA?"
).to_dict()
```

## 📋 API Usage

### Get Historical Features (Training)
```python
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo")

training_df = store.get_historical_features(
    entity_df=training_entities,
    features=[
        "customer_stats:daily_transactions",
        "customer_stats:lifetime_value",
        "product_features:price"
    ]
).to_df()
```

### Get Online Features (Inference)
```python
features = store.get_online_features(
    features=[
        "customer_stats:daily_transactions",
        "customer_stats:lifetime_value",
        "product_features:price"
    ],
    entity_rows=[{"customer_id": "C123", "product_id": "P456"}]
).to_dict()
```

## 🔌 Pluggable Architecture

Feast suporta múltiplos backends:
- **Data warehouses**: BigQuery, Snowflake, Redshift
- **Online stores**: Redis, DynamoDB, Cassandra
- **Batch processing**: Spark, Kafka

**Benefício:** No vendor lock-in

## 📊 Use Cases

| Use Case | Descrição |
|----------|-----------|
| **Fraud detection real-time** | Streaming + Redis para millisecond inference |
| **Batch recommendations** | Pull features from BigQuery |
| **Experimentation platforms** | Offline/online consistency |

## 🔗 Integrações

- Airflow
- Prefect
- Python-first workflows (SDKs)

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Feature View** | Definição de feature com source + schema |
| **Entity** | Objeto que features descrevem (ex: customer_id) |
| **Feature Service** | Grupo de features para serving |
| **Feature Registry** | Metadata centralizada |

## 🔗 Referências Cruzadas

- Complementa: Feature Store Comparison (022)
- Relacionado a: Feast vs Tecton vs Hopsworks (023)
- Pré-requisito para: MLOps pipelines com Feature Store

---

**Conceitos aprendidos:** 10
**Relevância:** Alta (open source reference)