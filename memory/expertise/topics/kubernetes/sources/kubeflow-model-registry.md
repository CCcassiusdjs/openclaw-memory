# Kubeflow Model Registry: Overview

**Fonte:** https://www.kubeflow.org/docs/components/model-registry/overview/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Model Registry é componente central do MLOps, gerenciando ciclo de vida de modelos ML desde criação até monitoramento.

## O que é Model Registry?

Model Registry é um componente crítico no lifecycle de AI/ML models:
- **Central index** para model developers indexarem e gerenciarem modelos
- **Gap filler** entre experimentation e production
- **Collaboration interface** para stakeholders do ML lifecycle

## Lifecycle Coverage

| Fase | Função do Model Registry |
|------|--------------------------|
| **Create** | Track changes, experiment architectures, maintain history |
| **Verify** | Testing/validation records, performance metrics |
| **Package** | Organize artifacts, dependencies, reproducibility |
| **Release** | Version transitions, approval workflows |
| **Deploy** | Approved versions info, consistency, traceability |
| **Monitor** | Performance tracking, drift detection, retraining triggers |

## Personas

### Data Scientist
- Desenvolve e avalia modelos
- Tracks performance de versões
- Compara modelos
- Compartilha com team

### MLOps Engineer
- Deploy para production
- Configura serving environment
- Monitora deployed models
- Mitiga issues

### Business Analyst
- Audita deployed models
- Monitora performance
- Tomada de decisões baseada em dados
- Compliance e governance

## Casos de Uso

### 1. Tracking Model Training
- Catalog modelos em storage
- Track e compare performance (accuracy, recall, precision)
- Create lineage (data → code → model)
- Facilitate collaboration

### 2. Experimenting with Weights
- Register base model com hyperparameters
- Track experiments/runs com variações
- Compare metrics entre runs
- Enable reproducibility
- Share para deployment

### 3. Model Deployment
- Retrieve latest approved version
- Access metadata (architecture, hyperparameters, metrics)
- Configure serving environment
- Track deployments
- Monitor health

### 4. Monitoring and Governance
- View performance metrics em real-time
- Detect model drift
- Access lineage para debugging
- Audit model usage (compliance)
- Regulatory support (GDPR, EU AI Act)

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Improved Collaboration** | Comunicação entre Data Scientists e MLOps |
| **Experiment Management** | Organização centralizada |
| **Version Control** | Track de versões e configurações |
| **Increased Efficiency** | Streamline development e deployment |
| **Enhanced Governance** | Compliance com regulations |
| **Reproducibility** | Recreate experiments e versions |
| **Better Decision-making** | Data-driven insights |

## Kubeflow Model Registry Features

### Model Tracking
- Store location de modelos
- Catalog, list, index, share
- Compare versions
- Revert to previous versions

### Performance Comparison
- Key metrics por versão
- Accuracy, recall, precision
- Identify best-performing model

### Lineage
- Relacionamentos entre data, code, models
- Understand origin de cada model
- Reproducibility

### Collaboration
- Share models e experiments
- Seamless transition training → production

## Integration com Kubeflow

| Componente | Integração |
|------------|------------|
| **Notebooks** | Exploratory research, model development |
| **Pipelines** | Track experiments e runs |
| **Katib** | Hyperparameter tuning tracking |
| **KServe** | Deployment de registered models |

## Insights

- Model Registry é bridge entre experimentation e production
- Suporta todo ML lifecycle: create → verify → package → release → deploy → monitor
- Personas diferentes têm necessidades diferentes do registry
- Governance e compliance são casos de uso críticos
- Lineage é fundamental para debugging e reproducibility
- Kubeflow integra Model Registry com todo o ecosystem