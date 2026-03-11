# MLflow GenAI - Visão Geral

**Fonte:** DOC-015 - MLflow GenAI Documentation  
**URL:** https://mlflow.org/docs/latest/genai/  
**Tipo:** Documentação Oficial  
**Data:** 2025  
**Status:** completed

---

## Resumo

Visão geral do MLflow GenAI: plataforma open-source all-in-one para aplicações GenAI com observabilidade, avaliações, AI gateway, prompt management e tracking.

---

## Key Features

### Open Source
- 20K+ GitHub Stars
- 50M+ monthly downloads
- Part of Linux Foundation
- Vendor-neutral infrastructure

### OpenTelemetry
- Tracing fully compatible with OpenTelemetry
- No vendor lock-in
- Easy integration with existing observability stack

### All-in-one Platform
- Complete GenAI journey: experimentation to production
- Track prompts, evaluate quality, deploy models, monitor
- Single unified platform

---

## Core Capabilities

### Observability
- Comprehensive tracing
- Captures prompts, retrievals, tool calls, model responses
- Debug complex workflows with confidence
- OpenTelemetry-compatible tracing SDK

### Evaluations
- LLM-as-a-judge metrics
- Mimic human expertise for quality assessment
- Pre-built judges for common metrics:
  - Hallucination detection
  - Relevance scoring
  - Custom judges for business needs

### Prompt Management & Optimization
- Version, compare, iterate on prompts
- MLflow UI for prompt management
- Reuse prompts across versions
- Rich lineage tracking

### Running Anywhere
- Local environment
- On-premises clusters
- Cloud platforms (AWS SageMaker, Azure ML)
- Managed services (Databricks, Nebius)

---

## Quick Start

### Start Demo from UI
1. Click "Start Demo" button on MLflow UI top page

### Start Demo from CLI
```bash
uvx mlflow demo
```
No running MLflow server required.

---

## Framework Integration

- 30+ integrations
- Extensible APIs
- Works with any GenAI framework or model provider
- Adapts to your tech stack

---

## GenAI Journey with MLflow

```
Experimentation → Evaluation → Deployment → Monitoring
      ↓                ↓             ↓            ↓
   Tracing         LLM Judges    Model Registry  Tracing
   Prompts         Metrics       Serving         Metrics
   Artifacts       Lineage       Endpoints       Alerts
```

---

## Resources

- [Databricks MLflow 3 GenAI](https://docs.databricks.com/aws/en/mlflow3/genai/)
- [AWS SageMaker AI](https://aws.amazon.com/sagemaker-ai/experiments/)
- [Azure ML](https://learn.microsoft.com/en-us/azure/machine-learning/concept-mlflow)
- [Nebius Managed MLflow](https://nebius.com/services/managed-mlflow/docs/latest/ml/tracking/)

---

## Concepts Adicionados

- GenAI observability with OpenTelemetry
- LLM-as-a-judge evaluation metrics
- Prompt versioning and lineage
- Pre-built judges (hallucination, relevance)
- Custom judge development
- 30+ framework integrations

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 10 min