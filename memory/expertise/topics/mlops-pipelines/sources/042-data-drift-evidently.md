# Data Drift in ML - Evidently AI - Resumo

**Fonte:** https://www.evidentlyai.com/ml-in-production/data-drift
**Tipo:** Guide
**Data:** 2026-03-12

---

## 🎯 O que é Data Drift?

**Data drift** = Mudança nas propriedades estatísticas e características dos dados de entrada:
- Occorre quando modelo em produção encontra dados diferentes do treinamento
- Pode causar queda na performance do modelo
- Detecção é vital para manter ML model reliability

## 📋 Exemplo Prático

**Retail sales forecasting:**
- Modelo treinado com vendas físicas
- Marketing campaign → surge em online sales
- Treinamento não tinha dados online suficientes
- Modelo perde accuracy em previsões

## 🔄 Data Drift vs Conceitos Relacionados

### Data Drift vs Concept Drift

| Aspecto | Data Drift | Concept Drift |
|---------|------------|---------------|
| **Definição** | Mudança na distribuição dos inputs | Mudança na relação input-output |
| **O que muda** | Features | Padrões de previsão |
| **Exemplo** | Mais vendas online | Comportamento de compra diferente |
| **Pode ocorrer junto?** | Sim, frequentemente | Sim, frequentemente |

**Concept Drift Exemplo:**
- Novo competidor com descontos
- COVID-19 mudou comportamento de compra
- Modelos anteriores tornam-se obsoletos

### Data Drift vs Prediction Drift

| Aspecto | Data Drift | Prediction Drift |
|---------|------------|-----------------|
| **O que muda** | Input features | Output predictions |
| **Sinal** | Mudança no input | Mudança no output |
| **Proxy para** | Environment change | Model quality issues |

**Prediction Drift:**
- Fraud model prevê mais fraud
- Pricing model mostra preços mais baixos
- Mudança nas predictions = investigate

## 📊 Detecção de Data Drift

### Métodos

| Método | Descrição |
|--------|-----------|
| **Summary statistics** | Monitorar mean, std, min, max |
| **Statistical tests** | Kolmogorov-Smirnov, Chi-square |
| **Distance metrics** | PSI (Population Stability Index), Wasserstein |

### Quando usar cada método

| Cenário | Método Recomendado |
|---------|-------------------|
| Quick check | Summary statistics |
| Distribution comparison | Statistical tests |
| Automated monitoring | PSI threshold |

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Data Drift** | Mudança na distribuição dos inputs |
| **Concept Drift** | Mudança na relação input-output |
| **Prediction Drift** | Mudança na distribuição das predictions |
| **Training-serving Skew** | Diferença entre treino e produção |
| **Proxy Signal** | Data drift como proxy para model quality |

## 🔧 Ferramentas

- **Evidently** - Open-source Python library
- Monitor data drift
- Statistical tests
- Visual reports

## 🔗 Referências Cruzadas

- Complementa: ML Monitoring Zoomcamp (044)
- Relacionado a: MLOps Principles (002)
- Pré-requisito para: Model Retraining Strategies

---

**Conceitos aprendidos:** 12
**Relevância:** Alta (monitoring fundamentals)