# Feature Store Landscape - Resumo

**Fonte:** https://www.featurestore.org/
**Tipo:** Reference
**Data:** 2026-03-12

---

## 📊 Feature Stores por Categoria

### Open Source

| Feature Store | Company | Notas |
|---------------|---------|-------|
| **Hopsworks** | Hopsworks | First open-source FS, DataFrame API, stream processing |
| **Feast** | Linux Foundation | Minimal, configurable, any platform |
| **Feathr** | Microsoft/LinkedIn | Point-in-time correct, auto compute |
| **Iguazio** | Iguazio | MLRun integration, V3IO backend |
| **Featureform** | Featureform | Virtual feature store, plug-in architecture |
| **OpenMLDB** | OpenMLDB | Open-source feature platform |

### Vendor (Managed)

| Feature Store | Company | Notas |
|---------------|---------|-------|
| **Tecton** | Tecton | Enterprise, streaming, GitOps |
| **Databricks** | Databricks | Lakehouse, Delta Lake native |
| **Vertex AI** | Google | GCP native, BigQuery + BigTable |
| **SageMaker** | Amazon | AWS native, S3 + Dynamo |
| **Fennel** | Fennel | Rust-powered, real-time |
| **Feature Byte** | FeatureByte | AI data prep platform |

### In-House (Built by Companies)

| Platform | Company | Online Store | Offline Store |
|---------|---------|--------------|---------------|
| **Michelangelo/Palette** | Uber | Redis/Cassandra | Hive |
| **Zipline (Chronon)** | Airbnb | Custom | Spark/Flink |
| **FBLearner** | Facebook | Custom | Custom |
| **Overton** | Apple | Custom | Custom |
| **Jukebox** | Spotify | TFX/Kubeflow | Custom |
| **Nexus** | Disney Streaming | Redis | Delta Lake |
| **Beast** | Robinhood | Kafka/Flink | Custom |
| **Sibyl** | DoorDash | Redis (extended) | Custom |

## 🏆 Feature Store Pioneers

### Michelangelo (Uber) - "The Mother of Feature Stores"
- First major feature store (2017)
- Palette = feature store component
- DSL → Spark + Flink jobs
- Online: Redis/Cassandra
- Offline: Hive

### Zipline (Airbnb/Chronon)
- One of the first (2018)
- DSL with point-in-time correct backfills
- Auto data quality monitoring
- Feature visualizations

## 📋 Feature Store Architecture Patterns

### Online Store (Low-latency)
| Store | Latency | Use Case |
|-------|---------|----------|
| Redis | Sub-ms | Real-time inference |
| DynamoDB | Low | AWS native |
| BigTable | Low | GCP native |
| Cassandra | Low | High throughput |

### Offline Store (Batch)
| Store | Use Case |
|-------|----------|
| BigQuery | GCP, analytics |
| Delta Lake | Databricks |
| Hive | Uber, batch |
| Parquet/S3 | AWS, simple |

## 💡 Key Insights

1. **First FS**: Hopsworks (open-source with DataFrame API)
2. **Enterprise leader**: Tecton (from Uber Michelangelo creators)
3. **Most flexible**: Feast (any backend)
4. **Lakehouse native**: Databricks Feature Store
5. **Real-time focus**: Fennel (Rust), Tecton (streaming)

## 🔗 Referências Cruzadas

- Complementa: Feast Official (021)
- Relacionado a: Top 5 Feature Stores (024)
- Contexto: Feast vs Tecton vs Hopsworks (023)

---

**Conceitos aprendidos:** 20
**Relevância:** Alta (market landscape overview)