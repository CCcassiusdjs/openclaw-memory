# ML Monitoring Module - MLOps Zoomcamp - Resumo

**Fonte:** https://www.evidentlyai.com/blog/mlops-zoomcamp-monitoring
**Tipo:** Course Summary
**Data:** 2026-03-12

---

## 🎯 Sobre MLOps Zoomcamp

Curso gratuito de MLOps da DataTalks.Club (40.000+ membros):
- MLOps best practices
- ML model lifecycle end-to-end
- Experiment tracking → ML pipelines → Monitoring

Ferramentas: MLflow, Prefect, Grafana, Evidently

## 📊 ML Monitoring Metrics

### Service Health (Camada 1)
| Métrica | Descrição |
|---------|-----------|
| **Uptime** | Disponibilidade do serviço |
| **Memory** | Uso de memória |
| **Latency** | Tempo de resposta |

### ML Model Performance (Camada 2)
| Tipo | Métricas |
|------|----------|
| **Ranking** | NDCG, MAP, MRR |
| **Regression** | MAE, MAPE, RMSE |
| **Classification** | Log Loss, Precision, Recall, F1 |

### Data Quality & Integrity (Camada 3)
| Métrica | Descrição |
|---------|-----------|
| **Missing values** | Share de valores nulos |
| **Column types** | Verificação de tipos |
| **Value range** | Range de valores por coluna |

### Data Drift & Concept Drift (Camada 4)
| Tipo | Descrição |
|------|-----------|
| **Data Drift** | Mudança na distribuição dos dados de input |
| **Concept Drift** | Mudança na relação input→output |

## 🔄 Batch vs Non-Batch Models

### Batch Models
- Métricas calculadas em batch
- Comparação: reference data vs current batch
- Mais simples de implementar

### Non-Batch (REST API)
- Métricas real-time para quality/integrity
- Window functions para drift/performance
- Moving windows com ou sem moving reference

## 🏗️ ML Monitoring Architecture

```
Prediction Service → Logging System → Monitoring Jobs → Database → Dashboard
       ↓                    ↓                 ↓              ↓           ↓
   REST/Batch         Local files      Prefect + Evidently    DB    Grafana
```

## 📋 Implementação

### Ferramentas
| Ferramenta | Uso |
|------------|-----|
| **Evidently** | Cálculo de métricas |
| **Grafana** | Visualização |
| **Prefect** | Orchestration de jobs |
| **PostgreSQL** | Armazenamento de métricas |

### Workflow
1. Use prediction service (REST ou batch)
2. Simulate production usage → logs
3. Implement monitoring jobs (Evidently + Prefect)
4. Load metrics into database
5. Visualize in Grafana

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Service Health** | Métricas de infraestrutura |
| **Model Performance** | Métricas de qualidade do modelo |
| **Data Quality** | Integridade dos dados de entrada |
| **Data Drift** | Mudança na distribuição de dados |
| **Concept Drift** | Mudança na relação input-output |
| **Window Functions** | Análise de streams contínuos |

## 🔗 Referências Cruzadas

- Complementa: MLOps Principles (002)
- Relacionado a: Evidently AI (monitoring tool)
- Pré-requisito para: Production ML systems

---

**Conceitos aprendidos:** 12
**Relevância:** Alta (monitoring prático)