# MLflow Evaluation & Monitoring - Resumo

**Fonte:** https://mlflow.org/docs/latest/genai/eval-monitor/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Visão Geral

MLflow oferece capabilities de evaluation e monitoring para medir, melhorar e manter qualidade de aplicações GenAI durante todo o lifecycle: development → production.

**Core Tenet:** Evaluation-Driven Development

---

## Evaluation-Driven Development

Prática emergente para construir aplicações LLM/Agentic de alta qualidade:
1. Definir dataset de teste
2. Criar função de predição
3. Definir scorers (métricas)
4. Rodar evaluation
5. Analisar resultados na UI
6. Iterar

---

## Quick Example

```python
import os
import openai
import mlflow
from mlflow.genai.scorers import Correctness, Guidelines

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Definir dataset de QA
dataset = [
    {
        "inputs": {"question": "Can MLflow manage prompts?"},
        "expectations": {"expected_response": "Yes!"},
    },
    {
        "inputs": {"question": "Can MLflow create a taco for my lunch?"},
        "expectations": {
            "expected_response": "No, unfortunately, MLflow is not a taco maker."
        },
    },
]

# 2. Definir prediction function
def predict_fn(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# 3. Rodar evaluation
results = mlflow.genai.evaluate(
    data=dataset,
    predict_fn=predict_fn,
    scorers=[
        # Built-in LLM judge
        Correctness(),
        # Custom criteria using LLM judge
        Guidelines(name="is_english", guidelines="The answer must be in English"),
    ],
)
```

---

## Scorers

### Built-in Scorers

| Scorer | Descrição |
|--------|-----------|
| **Correctness** | Avalia se resposta está correta |
| **Guidelines** | Avalia se segue guidelines customizadas |
| **Relevance** | Avalia relevância da resposta |
| **Groundedness** | Avalia se resposta está grounded no contexto |
| **Coherence** | Avalia coerência da resposta |
| **Safety** | Avalia segurança da resposta |

### Custom Scorers

```python
from mlflow.genai.scorers import Guidelines

# Custom guideline scorer
is_english = Guidelines(
    name="is_english",
    guidelines="The answer must be in English"
)

# Adicionar à evaluation
results = mlflow.genai.evaluate(
    data=dataset,
    predict_fn=predict_fn,
    scorers=[Correctness(), is_english],
)
```

---

## Evaluation Dataset

### Formato

```python
dataset = [
    {
        "inputs": {"question": "...", "context": "..."},
        "expectations": {"expected_response": "..."},
    },
    ...
]
```

### Campos

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `inputs` | ✅ | Input para o modelo |
| `expectations` | ❌ | Output esperado (para comparison) |

---

## Viewing Results

### MLflow UI

```bash
mlflow server --port 5000
```

1. Abrir experimento
2. Tab "Runs"
3. Click no run de evaluation
4. Ver resultados e métricas

### Programmatic Access

```python
# Ver resultados
print(results.metrics)

# Ver scoring details
for result in results.scores:
    print(f"Question: {result.inputs['question']}")
    print(f"Predicted: {result.predicted}")
    print(f"Correctness: {result.scores['correctness']}")
```

---

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│               Evaluation-Driven Development              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Define Dataset                                       │
│     [{"inputs": {...}, "expectations": {...}}]           │
│                                                          │
│  2. Create Prediction Function                           │
│     def predict_fn(inputs): return response              │
│                                                          │
│  3. Define Scorers                                       │
│     [Correctness(), Guidelines(...), ...]                │
│                                                          │
│  4. Run Evaluation                                       │
│     results = mlflow.genai.evaluate(...)                  │
│                                                          │
│  5. Analyze in UI                                        │
│     MLflow UI → Runs → Evaluation Run                    │
│                                                          │
│  6. Iterate                                              │
│     Update model/prompt → Re-evaluate                    │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## Quick Reference

```python
import mlflow
from mlflow.genai.scorers import Correctness, Guidelines

# Dataset
dataset = [
    {"inputs": {"question": "..."}, "expectations": {"expected_response": "..."}},
]

# Prediction function
def predict_fn(inputs):
    return model.predict(inputs["question"])

# Evaluation
results = mlflow.genai.evaluate(
    data=dataset,
    predict_fn=predict_fn,
    scorers=[
        Correctness(),
        Guidelines(name="concise", guidelines="Answer must be concise"),
    ],
)

# Results
print(results.metrics)
for score in results.scores:
    print(score)
```

---

## Conceitos Aprendidos

1. **Evaluation-Driven Development** - Prática core para LLM/Agentic apps
2. **Built-in Scorers** - Correctness, Guidelines, Relevance, etc.
3. **Custom Scorers** - Guidelines com critérios customizados
4. **Dataset Format** - inputs + expectations
5. **Programmatic Results** - metrics + scores
6. **UI Analysis** - Visualização de resultados