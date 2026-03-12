# MLOps: Continuous Delivery and Automation Pipelines in ML - Google Cloud

**Fonte:** https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning
**Autor:** Google Cloud Architecture
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Documento seminal do Google Cloud sobre MLOps. Define os três níveis de maturidade MLOps (Level 0, 1, 2) e estabelece práticas para CI/CD/CT (Continuous Integration, Delivery, Training) em sistemas de ML.

---

## 🎯 Motivação

**O desafio real não é construir um modelo ML, mas sim operar continuamente um sistema ML integrado em produção.**

ML systems são diferentes de software tradicional:
- **Team skills**: Data scientists não são necessariamente software engineers
- **Development**: ML é experimental por natureza
- **Testing**: Mais complexo (data validation, model quality evaluation, model validation)
- **Deployment**: Pipelines multi-step, não apenas deploy de modelo
- **Production**: Modelos podem degradar com dados em constante evolução

---

## 📊 DevOps vs MLOps

| Aspecto | DevOps | MLOps |
|---------|--------|-------|
| **CI** | Testar código e componentes | Testar código, dados, schemas e modelos |
| **CD** | Deploy de software/package | Deploy de pipeline + prediction service |
| **CT** | — | **Novo!** Continuous Training automático |

---

## 🔢 Níveis de Maturidade MLOps

### Level 0: Manual Process

**Características:**
- Processo manual, script-driven, interativo
- Desconexão entre ML e operations (handoff de modelo)
- Release iterations infrequentes
- Sem CI, sem CD
- Deployment = prediction service apenas
- Sem monitoramento ativo de performance

**Quando é suficiente:**
- Poucos modelos
- Mudanças raras
- Dados estáveis

**Problemas:**
- Modelos quebram em produção
- Não adaptam a mudanças de ambiente/dados
- Requer intervenção manual para retraining

### Level 1: ML Pipeline Automation

**Objetivo:** Continuous Training (CT) do modelo em produção

**Características:**
- Experimentação rápida (pipeline orchestrado)
- CT automático com dados novos
- Experimental-operational symmetry (mesma pipeline em dev/prod)
- Código modularizado e containerizado
- Continuous delivery de modelos
- Deploy de pipeline completa, não apenas modelo

**Componentes Adicionais:**

#### 1. Data & Model Validation
- **Data validation**: Detecta schema skews e value skews
- **Model validation**: Avalia modelo antes de promover a produção

#### 2. Feature Store (opcional)
- Repositório centralizado de features
- API para batch serving e real-time serving
- Evita training-serving skew
- Features consistentes entre training e serving

#### 3. Metadata Management
- Registra cada execução da pipeline
- Armazena: versões, timestamps, parâmetros, artefatos
- Habilita: reproducibility, lineage, debugging, rollback

#### 4. Pipeline Triggers
- On demand (manual)
- On schedule (diário, semanal, mensal)
- On new data availability
- On performance degradation
- On concept drift (mudança em distribuições)

---

### Level 2: CI/CD Pipeline Automation

**Características:**
- CI/CD completo para pipeline de ML
- Pipeline de ML é versionada e testada
- Deploy automático de novas implementações
- Monitoramento e alertas robustos

---

## 📝 Data Science Steps for ML

Steps que podem ser manuais ou automatizados:

1. **Data Extraction**: Seleção e integração de dados
2. **Data Analysis**: EDA para entender dados
3. **Data Preparation**: Limpeza, split, transformations
4. **Model Training**: Treinar diferentes algoritmos, hyperparameter tuning
5. **Model Evaluation**: Avaliação em holdout test set
6. **Model Validation**: Confirmar adequação para deployment
7. **Model Serving**: Deploy para prediction service
8. **Model Monitoring**: Monitorar performance, triggers para retraining

---

## 🔧 Componentes do Sistema ML

*"Only a small fraction of a real-world ML system is composed of ML code."*

**Elementos circundantes:**
- Configuration
- Automation
- Data collection
- Data verification
- Testing & debugging
- Resource management
- Model analysis
- Process & metadata management
- Serving infrastructure
- Monitoring

---

## 💡 Insights Principais

1. **ML ≠ Software tradicional**: Requer práticas específicas
2. **Pipeline > Modelo**: Deploy de pipeline completa, não apenas modelo
3. **Data validation é crítico**: Schema skews e value skews podem quebrar modelos
4. **Feature Store**: Centraliza features e evita training-serving skew
5. **Metadata é essencial**: Para reproducibility, debugging e rollback
6. **Continuous Training**: Automatizar retraining com triggers apropriados

---

## 🔗 Conceitos Relacionados

### Training-Serving Skew
Diferença entre features usadas em training e serving. Feature Store resolve isso garantindo consistência.

### Concept Drift
Mudança nas distribuições dos dados ao longo do tempo. Modelo "envelhece" e precisa ser retrained.

### Canary Deployment
Deploy gradual de novo modelo para um subset de tráfego antes de promover a produção completa.

---

## 📚 Referências Citadas

1. Hidden Technical Debt in ML Systems (Sculley et al., NIPS 2015)
2. Machine Learning: The High Interest Credit Card of Technical Debt (Google Research)
3. Google ML Rules (developers.google.com/machine-learning/guides/rules-of-ml/)

---

## 📝 Tags

`#mlops` `#google-cloud` `#ci-cd` `#continuous-training` `#pipeline-automation` `#fundamentals` `#maturity-levels`