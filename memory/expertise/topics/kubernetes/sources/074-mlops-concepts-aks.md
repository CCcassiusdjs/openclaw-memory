# MLOps Concepts for AI Workflows - AKS

**Fonte:** https://learn.microsoft.com/en-us/azure/aks/concepts-machine-learning-ops
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

Documentação oficial da Microsoft sobre conceitos de MLOps: pipeline, DevOps principles, automation, CI/CD e IaC.

---

## O que é MLOps?

MLOps engloba práticas que facilitam colaboração entre:
- **Data scientists** → Training (inner loop)
- **ML engineers** → Packaging, deployment (outer loop)
- **IT operations** → Infrastructure, monitoring (outer loop)
- **Business stakeholders** → Requirements, metrics

### MLOps Pipeline Components
| Componente | Função |
|------------|--------|
| Unstructured data store | New data flowing in |
| Vector database | Structured, pre-processed data |
| Data ingestion framework | Indexing pipeline |
| Retraining workflows | Model fine-tuning triggers |
| Metrics collection | Performance tracking |
| Lifecycle management | Model versioning, deployment |

---

## DevOps + MLOps

### Três Processos Essenciais
1. **ML Workloads:** EDA, feature engineering, training (data scientist)
2. **Software Development:** Planning, testing, packaging (ML engineer)
3. **Operations:** Releasing, configuring, monitoring (IT ops)

### Inner Loop vs Outer Loop
```
┌─────────────────────────────────────────────────────┐
│                  INNER LOOP (Data Scientist)        │
│  ┌─────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │   EDA   │ → │   Feature   │ → │  Training &  │  │
│  │         │   │ Engineering │   │   Tuning    │  │
│  └─────────┘   └─────────────┘   └─────────────┘  │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                 OUTER LOOP (ML Engineer + IT)       │
│  ┌──────────┐   ┌───────────┐   ┌──────────────┐   │
│  │ Package  │ → │ Validate  │ → │    Deploy    │   │
│  └──────────┘   └───────────┘   └──────────────┘   │
│  ┌──────────┐   ┌───────────┐   ┌──────────────┐   │
│  │ Monitor  │ → │  Retrain  │ → │   Feedback   │   │
│  └──────────┘   └───────────┘   └──────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## DevOps Principles Applied

### Automation
| Task | Automation Opportunity |
|------|-------------------------|
| Model tuning/retraining | Time intervals or data thresholds |
| Performance degradation | Trigger fine-tuning |
| CVE scanning | Base container images from registries |

### Continuous Integration (CI)
- Refactoring notebooks → Python/R scripts
- Validating input data (missing/error values)
- Unit testing + integration testing

**Tools:** Azure Pipelines, GitHub Actions

### Continuous Delivery (CD)
1. Package model in pre-production (dev, test)
2. Maintain portability of parameters/hyperparameters
3. QA testing → Approve for production

**Important for LLMs:** Model artifact portability

### Source Control
| Type | Tool |
|------|------|
| Data versioning | Git-based systems |
| Code versioning | Azure Repos, GitHub |
| Model versioning | Model Registry |

### Agile Planning
- Isolate work into sprints
- Scope the project
- Enable team alignment

**Tools:** Azure Boards, GitHub Issues

### Infrastructure as Code (IaC)
- Define Azure resources in code
- Version control infrastructure
- Optimize for cost, performance
- Templates for specific job types

---

## MLOps Pipeline Best Practices

### Reduce Overhead
- Automate data collection
- Standardize model training
- Streamline deployment
- Enable faster iteration

### Key Metrics
- Model performance
- Volume of ingested data
- Resource utilization
- Cost efficiency

---

## Insights

### ML vs Traditional DevOps
| Aspect | Traditional | MLOps |
|--------|-------------|-------|
| Code | Static | Dynamic (data) |
| Testing | Unit/integration | + Model validation |
| Deployment | Application | + Model artifacts |
| Monitoring | Performance | + Data drift |

### Inner/Outer Loop Pattern
- **Inner:** Experimental, iterative (notebooks)
- **Outer:** Production-ready (scripts, pipelines)
- **Feedback loop:** Monitoring → Retraining triggers

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Inner Loop | Data scientist work: EDA, training |
| Outer Loop | ML engineer work: packaging, deploy, monitor |
| MLOps Pipeline | Components for end-to-end ML lifecycle |
| Model Portability | Artifact portability across environments |
| Automation Triggers | Retraining on time/data thresholds |

---

## Referências

- Azure DevOps: https://azure.microsoft.com/products/devops/repos/
- Azure Boards: https://learn.microsoft.com/en-us/azure/devops/boards/