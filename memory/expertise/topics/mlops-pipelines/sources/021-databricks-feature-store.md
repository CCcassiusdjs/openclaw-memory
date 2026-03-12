# Databricks Feature Store - Overview

**Fonte:** https://docs.databricks.com/aws/en/machine-learning/feature-store/
**Autor:** Databricks Documentation
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Documentação oficial do Databricks Feature Store com Unity Catalog. Explica feature engineering, serving, governance, e integração completa com ML workflows.

---

## 🎯 O que é Feature Store?

**Definição:** Registro centralizado de features usados em modelos AI/ML.

**Benefícios:**
- Feature tables e modelos registrados em Unity Catalog
- Governance, lineage, cross-workspace sharing
- Single platform para training + serving + monitoring

---

## 🏗️ Capacidades Principais

### Feature Engineering
| Feature | Descrição |
|---------|-----------|
| **Feature Tables in Unity Catalog** | Criar e trabalhar com feature tables |
| **Declarative Feature Engineering** | APIs declarativas para time-windowed aggregations |
| **Materialize Features** | Features para offline training ou online serving |

### Feature Discovery
| Feature | Descrição |
|---------|-----------|
| **Explore Features** | Catalog Explorer + Features UI |
| **Tags** | Key-value pairs para categorizar features |

---

## 🔄 Training Workflows

### Use Features to Train Models
- Features automaticamente trackeados no modelo
- Lineage: modelo → features usados em training

### Point-in-Time Feature Joins
- Correção temporal: feature values no momento do label
- Evita data leakage no training

### Python API
- API completa para feature engineering

---

## 🚀 Feature Serving

### Databricks Online Feature Stores
- Serve feature data para online applications
- Real-time ML models
- Powered by Databricks Lakebase

### Model Serving with Automatic Feature Lookup
- Lookup automático de features no inference time
- Elimina training-serving skew

### Feature Serving Endpoints
- Serve features para models/apps fora do Databricks

### On-Demand Feature Computation
- Calcular features no momento do inference
- Feature store handle computation

---

## 🛡️ Governance e Lineage

### Feature Governance
- Unity Catalog controla acesso às feature tables
- View lineage de feature table, model, function

---

## 📊 Supported Data Types

| Tipo | Suporte |
|------|---------|
| IntegerType | ✅ |
| FloatType | ✅ |
| BooleanType | ✅ |
| StringType | ✅ |
| DoubleType | ✅ |
| LongType | ✅ |
| TimestampType | ✅ |
| DateType | ✅ |
| ShortType | ✅ |
| ArrayType | ✅ (dense vectors, tensors, embeddings) |
| BinaryType | ✅ |
| DecimalType | ✅ |
| MapType | ✅ (sparse vectors, tensors, embeddings) |
| StructType | ✅ |

---

## 🔄 Workflow Completo

```
Raw Data → Feature Tables → Training → Model Registration → Serving → Monitoring
              ↓                                              ↓
         Unity Catalog ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

---

## 💡 Insights Principais

1. **Unity Catalog = governance unificado** para features e modelos
2. **Training-serving skew eliminado**: mesmo código para features
3. **Point-in-time joins**: correção temporal no training
4. **On-demand computation**: features calculadas no inference
5. **Lakebase powered**: online serving com baixa latência

---

## 📝 Tags

`#feature-store` `#databricks` `#unity-catalog` `#mlops` `#feature-engineering` `#governance`