# MLflow Tracing for LLM Observability - Resumo

**Fonte:** https://mlflow.org/docs/latest/genai/tracing/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é MLflow Tracing

Solução de observabilidade para aplicações LLM, 100% compatível com OpenTelemetry. Captura inputs, outputs e metadata de cada step intermediário de uma request, permitindo identificar bugs e comportamentos inesperados.

---

## Demo

### Via UI
Click em "Start Demo" na MLflow UI.

### Via CLI
```bash
uvx mlflow demo
```

---

## Use Cases no ML Lifecycle

### 1. Build & Debug
- Debug em IDE ou notebook
- Traces mostram o que acontece sob as abstrações
- Navegação seamless entre IDE, notebook e MLflow UI

### 2. Human Feedback
- Coleta de feedback humano em traces
- Análise de qualidade de responses

### 3. Evaluation
- Avaliação automática de traces
- Métricas de qualidade

### 4. Production Monitoring
- Monitoring em produção
- Async logging para performance

### 5. Dataset Collection
- Coleta de dados de traces
- Construção de datasets para fine-tuning

---

## O que torna MLflow Tracing Único

| Feature | Descrição |
|---------|-----------|
| **Open Source** | 100% FREE, sem SaaS costs |
| **OpenTelemetry** | Vendor lock-in free |
| **Framework Agnostic** | 20+ bibliotecas suportadas |
| **End-to-End** | Version tracking + evaluation |
| **Strong Community** | 20K+ GitHub Stars, 20MM+ downloads |

---

## Getting Started

### One-line Auto Tracing

```python
import mlflow

mlflow.openai.autolog()  # OpenAI
mlflow.anthropic.autolog()  # Anthropic
mlflow.langchain.autolog()  # LangChain
# ... e outras bibliotecas
```

---

## Flexível e Customizável

### Manual Tracing

```python
# Decorator
@mlflow.trace
def my_function():
    ...

# Context manager
with mlflow.start_span():
    ...
```

### Features Avançadas

| Feature | Descrição |
|---------|-----------|
| **Multi-threading** | Instrumentar apps multi-threaded |
| **Async support** | Suporte nativo para async |
| **Sessions** | Agrupar e filtrar traces |
| **PII Masking** | Redact dados sensíveis |
| **Sampling** | Controlar throughput |
| **Distributed Tracing** | Propagar contexto entre serviços |

---

## Production Readiness

### Async Logging

```python
# Logging em background
mlflow.enable_async_logging()
```

Trace logging é feito em background, sem impactar performance da aplicação.

### Production Tracing SDK

```bash
# SDK lightweight (95% menor footprint)
pip install mlflow-tracing
```

O package `mlflow-tracing` é otimizado para produção:
- 95% menor footprint
- Dependências mínimas
- Full tracing capabilities

---

## Quick Reference

```python
import mlflow

# Setup
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-app")

# Auto tracing
mlflow.openai.autolog()

# Manual tracing
@mlflow.trace
def my_function():
    ...

# Context manager
with mlflow.start_span("operation"):
    ...

# Update trace
mlflow.update_current_trace(
    metadata={"key": "value"}
)

# Async logging
mlflow.enable_async_logging()
```

---

## Conceitos Aprendidos

1. **OpenTelemetry Compatible** - Sem vendor lock-in
2. **One-line Autolog** - `mlflow.<lib>.autolog()`
3. **Manual Tracing** - Decorator `@mlflow.trace`
4. **Production SDK** - `mlflow-tracing` package lightweight
5. **Async Logging** - Background logging sem impacto
6. **Sessions** - Agrupar traces por conversação
7. **PII Masking** - Redact dados sensíveis
8. **Distributed Tracing** - Propagar contexto entre serviços
9. **Framework Agnostic** - 20+ bibliotecas suportadas