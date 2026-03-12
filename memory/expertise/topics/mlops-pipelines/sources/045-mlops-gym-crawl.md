# MLOps Best Practices - Databricks MLOps Gym Crawl - Resumo

**Fonte:** https://www.databricks.com/blog/mlops-best-practices-mlops-gym-crawl
**Tipo:** Guide
**Data:** 2026-03-12

---

## 🎯 MLOps Gym Phases

| Phase | Focus |
|-------|-------|
| **Crawl** | Foundations for repeatable ML workflows |
| **Walk** | CI/CD integration in MLOps |
| **Run** | Rigor and quality elevation |

## 🛠️ Tools and Frameworks

### MLflow (Tracking + Model Registry)
| Component | Uso |
|-----------|-----|
| **MLflow Tracking** | Experiment tracking |
| **Model Registry** | Model repository with Unity Catalog |
| **Models in UC** | Centralized model governance |

### Unity Catalog
- Unified data governance
- Manage/secure data and ML assets
- External tables for AWS SageMaker, AzureML
- Principle of least privilege
- BROWSE privilege for discoverability

### Feature Stores
- Centralized repository for features
- Same code for training + inference
- Point-in-time feature lookups
- Real-time inference sync with online stores

### Version Control (Git)
- Essential for data science teams
- Reproducibility and audit trail
- Code, data, configs, environments
- Platforms: GitHub, Azure DevOps
- Databricks Repos integration

## 📋 Version Control Best Practices

### Feature Branch Workflow
1. Create branch from main
2. Make changes in branch
3. Create pull request
4. Review and merge

### Project Organization
| Setup | Descrição |
|-------|-----------|
| **Mono-repo** | Single repo for all projects |
| **Multi-repo** | Separate repos per project |

### Git Guidelines
- Clean commit history
- Meaningful commit messages
- Regular commits
- Code review before merge

## 🔄 Apache Spark for ML

### When to Use Spark
- Out-of-memory with Pandas
- Large datasets (>memory)
- Distributed processing needed
- Big data analytics

### Benefits
| Benefit | Description |
|---------|-------------|
| **Scalability** | Scale across cluster |
| **Speed** | Parallel processing |
| **Integration** | MLlib, DataFrames |

## 💡 Key Takeaways

1. **MLOps is a journey** - Not once-and-done
2. **Tools matter** - But practices matter more
3. **Collaboration** - Organizational behaviors critical
4. **Quality** - Every detail matters
5. **Trust** - Business perception affects adoption

## 🏗️ Architecture

```
Unity Catalog
    ├── Data Assets
    ├── ML Assets
    └── Models (MLflow)

Feature Store
    ├── Offline Store
    └── Online Store (real-time)

MLflow
    ├── Tracking Server
    └── Model Registry

Git / Repos
    ├── Code Versioning
    └── Collaboration
```

## 🔗 Referências Cruzadas

- Complementa: MLOps Principles (002)
- Relacionado a: MLflow (016-020)
- Pré-requisito para: Feature Stores (021-025)

---

**Conceitos aprendidos:** 15
**Relevância:** Alta (MLOps best practices enterprise)