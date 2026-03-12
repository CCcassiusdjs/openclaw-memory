# CI/CD for Machine Learning - Databricks

**Fonte:** https://docs.databricks.com/aws/en/machine-learning/mlops/ci-cd-for-ml
**Autor:** Databricks Documentation
**Status:** completed
**Data Leitura:** 2026-03-12

---

## 📋 Resumo Executivo

Documentação oficial do Databricks sobre CI/CD para ML. Explica como integrar MLOps, DataOps, ModelOps e DevOps em uma plataforma unificada, com ferramentas específicas para cada etapa do ciclo de vida de ML.

---

## 🎯 Machine Learning Elements That Need CI/CD

**Desafio:** Times diferentes possuem partes diferentes do processo ML, com ferramentas e schedules diferentes.

**Solução:** Plataforma unificada com ferramentas integradas para consistência e reprodutibilidade.

### Elementos a Rastrear
1. **Training data:** Qualidade, schema changes, distribution changes
2. **Input data pipelines:** ETL, transformações
3. **Model code:** Training, validation, serving
4. **Model predictions e performance:** Outputs e métricas

---

## 📊 Framework: MLOps + DataOps + ModelOps + DevOps

| Framework | Foco | Goal |
|-----------|------|------|
| **MLOps** | ML lifecycle | Integration development + operations |
| **DataOps** | Data pipelines | Reliable and secure data |
| **ModelOps** | Model lifecycle | Development tracking, serving |
| **DevOps** | Production | Automation, deployment |

---

## 🔧 DataOps: Reliable and Secure Data

### Tasks and Tools

| DataOps Task | Databricks Tool |
|--------------|-----------------|
| Ingest and transform data | Auto Loader, Apache Spark |
| Track changes (versioning, lineage) | Delta tables |
| Build, manage, monitor pipelines | Lakeflow Spark Declarative Pipelines |
| Ensure security and governance | Unity Catalog |
| Exploratory analysis, dashboards | Databricks SQL, Dashboards, Notebooks |
| General coding | Databricks SQL, Notebooks |
| Schedule data pipelines | Lakeflow Jobs |
| Automate workflows | Lakeflow Jobs |
| Feature management | Databricks Feature Store |
| Data monitoring | Data quality monitoring |

---

## 🔧 ModelOps: Model Development and Lifecycle

### Tasks and Tools

| ModelOps Task | Databricks Tool |
|---------------|-----------------|
| Track model development | MLflow model tracking |
| Manage model lifecycle | Models in Unity Catalog |
| Model code versioning | Databricks Git folders |
| No-code model development | AutoML |
| Model monitoring | Data profiling |

---

## 🔧 DevOps: Production and Automation

### Platform Features
- **End-to-end lineage:** Model → raw data source
- **Model Serving:** Autoscaling based on demand
- **Jobs:** Automate and schedule workloads
- **Git folders:** Code versioning from workspace
- **Databricks Asset Bundles:** Automate resource deployment
- **Terraform provider:** Infrastructure automation

### Model Serving Options
| Option | Use Case |
|--------|----------|
| Batch serving | Large amounts of data |
| REST endpoint | Low-latency online serving |
| On-device / edge | Edge deployment |
| Multi-cloud | Train one cloud, deploy another |

---

## 🔄 Integration with CI/CD Tools

### Supported Tools
- **GitHub Actions:** Workflows + Databricks REST API
- **Azure DevOps pipelines:** Integration via REST API
- **Jenkins jobs:** Automation with API

### Best Practices
- Use Git folders for code versioning
- Use Databricks Asset Bundles for resource deployment
- Use REST API for automation
- Follow CI/CD workflows with Git integration

---

## 🛡️ Unity Catalog for Governance

**Features:**
- Fine-grained access control
- Security policies
- Governance for all data and AI assets

---

## 💡 Insights Principais

1. **Plataforma unificada:** Databricks integra DataOps + ModelOps + DevOps
2. **MLflow é central:** Tracking + Model Registry + Serving
3. **Delta tables:** Versioning + lineage para dados
4. **Unity Catalog:** Governance unificado para data + AI
5. **Asset Bundles:** Infrastructure as code para ML resources
6. **Feature Store:** Consistência de features entre training e serving

---

## 📝 Tags

`#cicd` `#databricks` `#mlops` `#dataops` `#modelops` `#devops` `#mlflow` `#unity-catalog`