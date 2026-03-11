# MLflow Tracing Quickstart - Resumo

**Fonte:** https://mlflow.org/docs/latest/genai/tracing/quickstart/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

Quickstart para configurar tracing em uma aplicação GenAI em menos de 10 minutos.

---

## Pré-requisitos

### Instalar uv

```bash
# Instalar uv (package manager)
curl --proto '=https' --tlsv1.2 -sSf https://setup.uv.rs | sh
```

### Iniciar MLflow Server

```bash
# Via uvx
uvx mlflow server

# Via pip
pip install mlflow
mlflow server --port 5000
```

---

## Criar Experimento

1. Navegar para http://localhost:5000
2. Click em "Create" (top right)
3. Digitar nome do experimento
4. Click em "Create"

---

## Dependências

### Python (OpenAI)

```bash
pip install --upgrade 'mlflow[genai]' openai>=1.0.0
```

### TypeScript (OpenAI)

```bash
npm install mlflow openai
```

**Nota:** Suporta OpenAI, Anthropic, Google, Bedrock e outros.

---

## Iniciar Tracing

### Python (OpenAI)

```python
import mlflow
from openai import OpenAI

# Conectar ao MLflow server
mlflow.set_tracking_uri("http://localhost:5000")

# Definir experimento
mlflow.set_experiment("My Application")

# Habilitar tracing automático
mlflow.openai.autolog()

# O trace é enviado automaticamente
client = OpenAI()
client.chat.completions.create(
    model="o4-mini",
    messages=[
        {"role": "system", "content": "You are a helpful weather assistant."},
        {"role": "user", "content": "What's the weather like in Seattle?"},
    ],
)
```

### TypeScript (OpenAI)

```typescript
import mlflow from "mlflow";
import OpenAI from "openai";

// Setup
mlflow.setTrackingUri("http://localhost:5000");
mlflow.setExperiment("My Application");

// Autolog
mlflow.openai.autolog();

// Trace automático
const client = new OpenAI();
await client.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "Hello!" }],
});
```

### OpenTelemetry

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Setup OpenTelemetry
provider = TracerProvider()
trace.set_tracer_provider(provider)

# Export para MLflow
exporter = OTLPSpanExporter("http://localhost:5000/api/2.0/mlflow/v1/traces")
provider.add_span_processor(BatchSpanProcessor(exporter))
```

---

## Ver Traces na UI

1. Abrir MLflow UI (http://localhost:5000)
2. Selecionar experimento "My Application"
3. Click na tab "Traces"
4. Ver traces criados

---

## Track Multi-Turn Conversations

### Sessions

```python
import mlflow

@mlflow.trace
def chat_completion(message: list[dict], user_id: str, session_id: str):
    """Process chat message with user and session tracking."""
    
    # Adicionar contexto ao trace
    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user": user_id,      # Link para usuário
            "mlflow.trace.session": session_id, # Agrupar conversação
        }
    )
    
    # Lógica do chat
    return generate_response(message)
```

**Benefícios:**
- Agrupar traces por usuário
- Agrupar traces por conversação
- Analisar fluxos de conversação

---

## Fluxo Completo

```
┌─────────────────────────────────────────────────────────┐
│                   Tracing Setup Flow                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Start MLflow Server                                  │
│     uvx mlflow server                                    │
│                                                          │
│  2. Create Experiment                                    │
│     mlflow.set_experiment("My Application")              │
│                                                          │
│  3. Install Dependencies                                 │
│     pip install 'mlflow[genai]' openai                   │
│                                                          │
│  4. Enable Tracing                                       │
│     mlflow.openai.autolog()                              │
│                                                          │
│  5. Run LLM Calls                                        │
│     client.chat.completions.create(...)                  │
│                                                          │
│  6. View Traces                                          │
│     MLflow UI → Traces tab                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Reference

```python
import mlflow
from openai import OpenAI

# Setup
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("my-app")

# Auto tracing
mlflow.openai.autolog()

# Run
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}],
)

# Multi-turn with sessions
@mlflow.trace
def chat(message, user_id, session_id):
    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user": user_id,
            "mlflow.trace.session": session_id,
        }
    )
    return generate_response(message)
```

---

## Conceitos Aprendidos

1. **Setup** - uvx ou pip para instalar
2. **Experiment** - Agrupar traces por aplicação
3. **Autolog** - `mlflow.<lib>.autolog()`
4. **OpenTelemetry** - Compatível com OTLP
5. **Sessions** - Agrupar traces por conversação
6. **User Tracking** - Link traces para usuários
7. **UI** - Visualizar traces na tab "Traces"

---

## Próximos Passos

- [Integrations](/docs/latest/genai/tracing/integrations/) - Lista de bibliotecas suportadas
- [Manual Tracing](/docs/latest/genai/tracing/app-instrumentation/manual-tracing/) - Decorator e context manager
- [Production](/docs/latest/genai/tracing/prod-tracing/) - Deployment em produção