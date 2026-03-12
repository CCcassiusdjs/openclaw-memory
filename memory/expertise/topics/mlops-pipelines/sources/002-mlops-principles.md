# MLOps Principles - Resumo

**Fonte:** https://ml-ops.org/content/mlops-principles
**Tipo:** Guide
**Data:** 2026-03-12

---

## 📋 Conceitos Principais

### Processo Iterativo-Incremental em MLOps

Três fases principais:
1. **Designing the ML-powered application** - Business/data understanding, design da solução ML
2. **ML Experimentation and Development** - PoC, iteracoes de algoritmos, data/model engineering
3. **ML Operations** - Deploy com DevOps practices (testing, versioning, CD, monitoring)

### Níveis de Automação

| Nível | Descrição | Características |
|-------|-----------|-----------------|
| **Manual** | Processo manual, experimental | Jupyter notebooks, RAD tools |
| **ML Pipeline Automation** | Treino automatizado | Continuous training, data/model validation |
| **CI/CD Pipeline Automation** | Deploy automatizado | Build, test, deploy automáticos |

### Estágios MLOps

| Estágio | Output |
|---------|--------|
| Development & Experimentation | Source code para pipelines |
| Pipeline CI | Pipeline components (packages, executables) |
| Pipeline CD | Deployed pipeline com novo modelo |
| Automated Triggering | Trained model no registry |
| Model CD | Deployed prediction service (REST API) |
| Monitoring | Triggers para pipeline/experiment cycle |

## 🔧 Componentes MLOps Setup

| Componente | Descrição |
|------------|-----------|
| **Source Control** | Versionamento Code, Data, Model artifacts |
| **Test & Build Services** | CI tools para QA e building |
| **Deployment Services** | CD tools para deploy pipelines |
| **Model Registry** | Registry para modelos treinados |
| **Feature Store** | Preprocessing features para training e serving |
| **ML Metadata Store** | Tracking metadata (params, metrics, data) |
| **ML Pipeline Orchestrator** | Automatiza steps dos experimentos |

## 💡 Conceitos-Chave Extraídos

1. **Technical Debt** - MLOps evita technical debt em ML applications
2. **Unified Release Process** - ML assets tratados como software assets em CI/CD
3. **Iterative Development** - Foco em uma ML use case por vez
4. **Triggers** - Calendar events, messaging, monitoring events, changes em data/code
5. **Maturity = Automation Level** - Quanto mais automação, mais maduro o processo

## 📊 Aplicações Práticas

- **CI/CD + CT + CD** - Continuous Integration, Training, Deployment
- **Testing** - Automatizado para descobrir problemas cedo
- **Reproducibility** - Via versioning de data, code, model

## 🔗 Referências Cruzadas

- Relacionado a: Google Cloud MLOps (001)
- Pré-requisito para: Pipeline Orchestration Tools (006-010)
- Fundamenta: CI/CD for ML (011-015)

---

**Conceitos aprendidos:** 8
**Relevância:** Alta (fundamenta toda prática MLOps)