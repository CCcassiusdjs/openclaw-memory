# MLflow GenAI - Resumo

**Fonte:** https://mlflow.org/docs/latest/genai/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é MLflow GenAI

Plataforma open-source all-in-one para aplicações GenAI e Agentes. Oferece:
- Observabilidade end-to-end
- Avaliações
- AI Gateway
- Prompt management & otimização
- Tracking

---

## Características Principais

### Open Source
- 20K+ GitHub Stars
- 50M+ downloads mensais
- Parte da Linux Foundation
- Vendor-neutral

### OpenTelemetry
- Tracing compatível com OpenTelemetry
- Sem vendor lock-in
- Integração com stack existente

### All-in-one Platform
- Track prompts
- Avaliar qualidade
- Deploy modelos
- Monitorar performance

### Observabilidade Completa
- Tracing de prompts, retrievals, tool calls, responses
- Debug de workflows complexos

### Evaluation & Monitoring
- LLM judges
- Métricas customizadas
- Avaliação sistemática de mudanças

### Framework Integration
- 30+ integrações
- APIs extensíveis
- Adapta ao seu stack

---

## Componentes

### Observability
Debug e iteração em aplicações GenAI com tracing:
- Captura execução completa
- Prompts, retrievals, tool calls
- OpenTelemetry-compatible

### Evaluations
- LLM-as-a-judge metrics
- Pre-built judges (hallucination, relevance)
- Custom judges para necessidades específicas

### Prompt Management & Optimization
- Version e compare prompts
- UI para iteração
- Reuse prompts across versions
- Lineage de versões

### Running Anywhere
- Local
- On-premises
- Cloud platforms
- Managed services (Databricks, AWS SageMaker, Azure ML, Nebius)

---

## Quick Start

### Demo via CLI
```bash
uvx mlflow demo
```

### Demo via UI
Clicar em "Start Demo" na UI do MLflow.

---

## Conceitos Aprendidos

1. **GenAI Platform** - MLflow expandido para suportar LLMs e agentes
2. **Tracing** - OpenTelemetry-compatible, sem vendor lock-in
3. **LLM Judges** - Avaliação automática de qualidade
4. **Prompt Management** - Versionamento e iteração de prompts
5. **Observabilidade** - Debug completo de workflows complexos
6. **Integrações** - 30+ frameworks suportados

---

## Integrações com Cloud

| Plataforma | Link |
|------------|------|
| Databricks | docs.databricks.com/aws/en/mlflow3/genai/ |
| AWS SageMaker | aws.amazon.com/sagemaker-ai/experiments/ |
| Azure ML | learn.microsoft.com/en-us/azure/machine-learning/ |
| Nebius | nebius.com/services/managed-mlflow/ |