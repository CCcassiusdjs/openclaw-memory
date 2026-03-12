# MLOps Best Practices in AKS

**Fonte:** https://learn.microsoft.com/en-us/azure/aks/best-practices-ml-ops
**Tipo:** Documentação
**Data:** 2026-03-12

---

## Resumo

Best practices da Microsoft Azure para MLOps no AKS (Azure Kubernetes Service). Foco em infrastructure-as-code, containerização, model management e segurança.

---

## Conceitos Principais

### Infrastructure as Code (IaC)

| Benefício | Descrição |
|-----------|-----------|
| **Consistency** | Provisioning consistente |
| **Reproducibility** | Ambientes idênticos |
| **Cost-effectiveness** | Templates versionados por job type |
| **Accelerated deployment** | Demystify hardware requirements |

**Considerações:**
- IaC muda ao longo do AI pipeline
- Compute power varia: inferencing, serving, training, fine-tuning
- Templates específicos por tipo de workload

---

## Containerization

### Benefícios
- **Portability:** Run anywhere
- **Simplified versioning:** Model weights, metadata, configs
- **Reduced storage:** Layered images

### Best Practices
| Prática | Descrição |
|---------|-----------|
| **Leverage existing images** | LLMs bilhões de parâmetros em registries |
| **Avoid SPOF** | Multiple lightweight containers vs one large image |
| **External datasets** | Store large data outside base image |

### KAITO (Kubernetes AI Toolchain Operator)
- Deploy high-performance LLMs on AKS in minutes
- Simplified deployment process

---

## Model Management and Versioning

### Benefícios
- Track changes over time
- Maintain consistency across containers
- Ease of deployment in different environments

### PEFT (Parameter-Efficient Fine-Tuning)
- Iterate faster on subset of weights
- Maintain new versions in lightweight containers
- Reduce training time and storage

---

## Automation

### Alerting Integration
```yaml
Trigger: New data flows into application
    ↓
Action: Vector ingestion flow automatically
```

### Model Performance Thresholds
- Track degradations
- Trigger retraining pipelines
- Automated response to drift

---

## Scalability and Resource Management

### Resource Optimization
| Técnica | Aplicação |
|---------|-----------|
| **Distributed computing** | CPU, GPU, memory efficient use |
| **Data parallelism** | Split data across workers |
| **Model parallelism** | Split model across devices |
| **Pipeline parallelism** | Split pipeline stages |

### Autoscaling
- Enable on compute resources
- Support high request volumes at peak
- Scale down in off-peak hours

### Disaster Recovery
- Follow AKS resiliency best practices
- Multi-region deployments
- Automated failover

---

## Security and Compliance

### CVE Scanning
```yaml
Scan: Open-source model container images
    ↓
Detect: Common vulnerabilities
    ↓
Fix: Before deployment
```

### Microsoft Defender for Containers
- Scan images stored in Azure Container Registry
- Detect vulnerabilities in model containers

### Audit Trail
- Ingested data tracking
- Model changes tracking
- Metrics tracking
- Compliance with organizational policies

---

## Insights

### AI Pipeline Stages
```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  Training   │ → │  Fine-tune  │ → │  Inference  │
│  (High GPU) │   │  (Medium)   │   │  (Low/CPU)  │
└─────────────┘   └─────────────┘   └─────────────┘
        ↓                 ↓                 ↓
    IaC Template     IaC Template     IaC Template
      (GPU)           (Mixed)          (CPU)
```

### Container Strategy
```
Large Monolithic Container (SPOF)
    ↓ AVOID
Multiple Lightweight Containers (Recommended)
    ├── Base image (OS, runtime)
    ├── Model weights (external storage)
    ├── Dependencies (minimal)
    └── Config (ConfigMaps/Secrets)
```

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| Infrastructure as Code | Versioned templates for AI infrastructure |
| PEFT | Parameter-efficient fine-tuning for LLMs |
| CVE Scanning | Vulnerability detection in container images |
| Distributed Computing | Data/Model/Pipeline parallelism |
| Audit Trail | Compliance tracking for data and models |

---

## Referências

- AKS Resiliency: https://learn.microsoft.com/en-us/azure/aks/ha-dr-overview
- Microsoft Defender for Containers: https://learn.microsoft.com/en-us/azure/defender-for-cloud/defender-for-containers-introduction
- KAITO: https://learn.microsoft.com/en-us/azure/aks/ai-toolchain-operator