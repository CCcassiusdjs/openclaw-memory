# MLOps Best Practices in Azure Kubernetes Service (AKS)

**Fonte:** Microsoft Learn - https://learn.microsoft.com/en-us/azure/aks/best-practices-ml-ops
**Data:** Outubro 2024
**Tópico:** MLOps, Azure AKS, Best Practices, AI Workloads
**Status:** Lido

---

## Resumo Executivo

Melhores práticas oficiais da Microsoft para MLOps no Azure Kubernetes Service (AKS), cobrindo IaC, containerização, versionamento de modelos, automação, escalabilidade e segurança.

---

## Conceitos-Chave

### MLOps Pipeline Components
- Unstructured data store (dados brutos)
- Vector database (embeddings)
- Data ingestion e indexing framework
- Vector ingestion / model retraining workflows
- Metrics collection e alerting
- Lifecycle management tools

---

## Best Practices

### 1. Infrastructure as Code (IaC)

#### Benefícios
- Provisionamento consistente e reprodutível
- Versionamento de infraestrutura
- Custo-efetividade por tipo de job

#### Aplicações
- Inferencing: Menos recursos
- Training: Mais recursos
- Fine-tuning: Recursos especializados

#### Ferramentas
- Terraform
- Azure Bicep
- ARM templates

---

### 2. Containerization

#### Vantagens
- **Portabilidade**: Model weights + metadata + configs
- **Versioning**: Simplificado
- **Storage**: Custos reduzidos

#### Práticas Recomendadas
- Usar imagens base de registries seguros
- Evitar SPOF (Single Point of Failure)
- Containers leves com dependências específicas
- Datasets grandes fora da imagem, montados em runtime

#### KAI Toolchain Operator
- Deploy de LLMs em minutos
- Imagens otimizadas para AI

---

### 3. Model Management e Versioning

#### Práticas
- Consistência entre containers de modelo
- PEFT (Parameter-Efficient Fine-Tuning) para iteração rápida
- Lightweight containers para novos versions

#### Versionamento
- Data versioning
- Code versioning
- Model versioning
- Experiment tracking

---

### 4. Automation

#### Automações Possíveis
- Alerting → vector ingestion workflow
- Model performance thresholds → retraining pipelines
- CVE scanning em base images

#### Ferramentas
- Azure Pipelines
- GitHub Actions
- Azure DevOps

---

### 5. Scalability e Resource Management

#### Práticas
- Distributed computing
- Multiple levels of parallelism (data, model, pipeline)
- Autoscaling para peak times
- Scale down em off-peak

#### GPU Management
- Efficient allocation de CPU/GPU/Memory
- Dynamic resource management
- Cost optimization

#### Disaster Recovery
- Multi-region deployments
- Resiliency best practices
- High availability

---

### 6. Security e Compliance

#### CVE Scanning
- Microsoft Defender for Containers
- Scanning automático em registries

#### Compliance
- Audit trail de data ingestion
- Model changes tracking
- Metrics retention

#### Security Features
- Network policies
- RBAC
- Secrets management
- Multi-tenancy

---

## MLOps Pipeline Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Unstructured │  │ Vector DB    │  │ Feature Store│   │
│  │ Data Store   │  │ (Embeddings) │  │              │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
├─────────────────────────────────────────────────────────┤
│                    Processing Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Ingestion    │  │ Indexing     │  │ Retraining   │   │
│  │ Framework    │  │ Pipeline     │  │ Workflow     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
├─────────────────────────────────────────────────────────┤
│                    Model Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Model        │  │ Model        │  │ Model        │   │
│  │ Registry     │  │ Serving      │  │ Monitoring   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
├─────────────────────────────────────────────────────────┤
│                    Infrastructure (AKS)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │ Compute      │  │ Storage      │  │ Networking   │   │
│  │ (CPU/GPU)    │  │ (PV/PVC)     │  │ (Services)   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Comparação: Inner Loop vs Outer Loop

| Aspect | Inner Loop | Outer Loop |
|--------|------------|------------|
| **Owner** | Data Scientists | ML Engineers, IT Ops |
| **Activities** | EDA, Training, Tuning | Packaging, Deploying, Monitoring |
| **Environment** | Development | Production |
| **Focus** | Experimentation | Operationalization |

---

## Insights para Kubernetes

1. **IaC é obrigatório**: Infraestrutura versionada e reprodutível
2. **Containerização eficiente**: Imagens leves, datasets externos
3. **PEFT para LLMs**: Fine-tuning eficiente de grandes modelos
4. **CVE scanning crítico**: Segurança em open-source images
5. **Autoscaling inteligente**: Balancear custo e performance

---

## Palavras-Chave
`mlops` `azure-aks` `best-practices` `containerization` `infrastructure-as-code` `model-versioning` `security` `scalability`