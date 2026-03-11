# MLflow Prompt Registry - Resumo

**Fonte:** https://mlflow.org/docs/latest/genai/prompt-registry/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é Prompt Registry

Ferramenta para versionar, trackear e reutilizar prompts em aplicações GenAI. Mantém consistência e melhora colaboração.

---

## Benefícios

| Benefício | Descrição |
|-----------|-----------|
| **Version Control** | Git-inspired commit-based versioning |
| **Aliasing** | A/B testing, rollbacks, deployment pipelines |
| **Lineage** | Integração com MLflow Tracking e Evaluation |
| **Collaboration** | Registry centralizado para toda organização |

---

## Getting Started

### Criar Prompt

```python
import mlflow

# Registrar prompt
mlflow.genai.register_prompt(
    name="summarization-prompt",
    template="Summarize the following in {{num_sentences}} sentences: {{text}}",
    commit_message="Initial version",
)
```

### Carregar e Usar

```python
import mlflow
import openai

# Carregar prompt
prompt = mlflow.genai.load_prompt("prompts:/summarization-prompt/2")

# Formatar e usar
client = openai.OpenAI()
response = client.chat.completions.create(
    messages=[{
        "role": "user",
        "content": prompt.format(num_sentences=1, text=target_text)
    }],
    model="gpt-4o-mini",
)
```

---

## Prompt Object

### Atributos

| Atributo | Descrição |
|----------|-----------|
| **Name** | Identificador único |
| **Template** | Texto com variáveis `{{variable}}` |
| **Version** | Número sequencial |
| **Commit Message** | Descrição das mudanças |
| **Tags** | Key-value pairs para categorização |
| **Alias** | Referência mutável (ex: `@production`) |
| **is_text_prompt** | True = text, False = chat |
| **response_format** | Schema esperado de resposta |
| **model_config** | Configuração do modelo |

---

## Prompt Types

### Text Prompts

```python
template = "Hello {{name}}, how are you today?"
```

### Chat Prompts

```python
template = [
    {"role": "system", "content": "You are a helpful {{style}} assistant."},
    {"role": "user", "content": "{{question}}"},
]
```

### Jinja2 Prompts

```python
template = """\
Hello {% if name %}{{ name }}{% else %}Guest{% endif %}!

{% if items %}
Here are your items:
{% for item in items %}
- {{ item }}
{% endfor %}
{% endif %}
"""

prompt = mlflow.genai.register_prompt(
    name="greeting-prompt",
    template=template,
)

result = prompt.format(name="Alice", items=["Book", "Pen"])
```

---

## Model Configuration

### Uso Básico

```python
from mlflow.entities.model_registry import PromptModelConfig

config = PromptModelConfig(
    model_name="gpt-4-turbo",
    temperature=0.5,
    max_tokens=2000,
    top_p=0.95,
    frequency_penalty=0.2,
    presence_penalty=0.1,
    stop_sequences=["END", "\n\n"],
)

mlflow.genai.register_prompt(
    name="creative-prompt",
    template="Write a creative story about {{topic}}",
    model_config=config,
)
```

### Parâmetros Suportados

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `model_name` | str | Nome do modelo |
| `temperature` | float | Sampling temperature (0.0-2.0) |
| `max_tokens` | int | Máximo de tokens |
| `top_p` | float | Nucleus sampling (0.0-1.0) |
| `top_k` | int | Top-k sampling |
| `frequency_penalty` | float | Penalty por frequência |
| `presence_penalty` | float | Penalty por presença |
| `stop_sequences` | list[str] | Sequências de parada |
| `extra_params` | dict | Parâmetros provider-specific |

---

## Aliases

```python
# Criar alias
mlflow.genai.set_prompt_alias(
    name="summarization-prompt",
    version=2,
    alias="production",
)

# Carregar por alias
prompt = mlflow.genai.load_prompt("prompts:/summarization-prompt@production")
```

**Alias Reservado:** `@latest` carrega a versão mais recente.

---

## Tags

### Prompt-level Tags

```python
# Set
mlflow.genai.set_prompt_tag("summarization-prompt", "language", "en")

# Get
tags = mlflow.genai.get_prompt_tags("summarization-prompt")

# Delete
mlflow.genai.delete_prompt_tag("summarization-prompt", "language")
```

### Version-level Tags

```python
# Set
mlflow.genai.set_prompt_version_tag("summarization-prompt", 1, "author", "alice")

# Get
prompt = mlflow.genai.load_prompt("prompts:/summarization-prompt/1")
print(prompt.tags)

# Delete
mlflow.genai.delete_prompt_version_tag("summarization-prompt", 1, "author")
```

---

## Caching

### Comportamento Default

| Tipo | TTL |
|------|-----|
| **Version-based** | Infinite (imutável) |
| **Alias-based** | 60 segundos |

### Customizar TTL

```python
# Custom TTL: 5 minutos
prompt = mlflow.genai.load_prompt(
    "prompts:/summarization-prompt/1",
    cache_ttl_seconds=300,
)

# Bypass cache
prompt = mlflow.genai.load_prompt(
    "prompts:/summarization-prompt@production",
    cache_ttl_seconds=0,
)
```

### Environment Variables

```bash
# Alias TTL
export MLFLOW_ALIAS_PROMPT_CACHE_TTL_SECONDS=300

# Version TTL
export MLFLOW_VERSION_PROMPT_CACHE_TTL_SECONDS=3600
```

---

## Search Prompts

```python
import mlflow

# Fluent API
prompts = mlflow.genai.search_prompts(filter_string="task='summarization'")

# Client API (paginação)
from mlflow.tracking import MlflowClient

client = MlflowClient()
all_prompts = []
token = None

while True:
    page = client.search_prompts(
        filter_string="task='summarization'",
        max_results=50,
        page_token=token,
    )
    all_prompts.extend(page)
    token = page.token
    if not token:
        break
```

---

## Integration com LangChain

```python
import mlflow
from langchain.prompts import PromptTemplate

# Carregar prompt do MLflow
prompt = mlflow.genai.load_prompt("question_answering")

# Converter para single brace format (LangChain)
langchain_prompt = PromptTemplate.from_template(
    prompt.to_single_brace_format()
)
```

---

## Response Format

```python
from pydantic import BaseModel

class SummaryResponse(BaseModel):
    summary: str
    key_points: list[str]
    word_count: int

# Registrar com response_format
mlflow.genai.register_prompt(
    name="structured-summary",
    template="Summarize: {{text}}",
    response_format=SummaryResponse,
)
```

---

## Quick Reference

```python
import mlflow

# Register
mlflow.genai.register_prompt(
    name="my-prompt",
    template="Hello {{name}}!",
    model_config={"temperature": 0.7},
)

# Load
prompt = mlflow.genai.load_prompt("prompts:/my-prompt@latest")

# Format
formatted = prompt.format(name="World")

# Alias
mlflow.genai.set_prompt_alias("my-prompt", version=1, alias="production")

# Search
prompts = mlflow.genai.search_prompts(filter_string="task='qa'")

# Model Config
mlflow.genai.set_prompt_model_config(
    name="my-prompt",
    version=1,
    model_config={"temperature": 0.8},
)
```

---

## Conceitos Aprendidos

1. **Prompt Registry** - Versionamento de prompts
2. **Versioning** - Git-inspired commits
3. **Aliases** - Referências mutáveis para deployment
4. **Prompt Types** - Text, Chat, Jinja2
5. **Model Config** - Configuração de modelo acoplada
6. **Caching** - TTL configurável
7. **Search** - Busca por tags e filtros
8. **LangChain Integration** - Single brace format
9. **Response Format** - Pydantic models para validação