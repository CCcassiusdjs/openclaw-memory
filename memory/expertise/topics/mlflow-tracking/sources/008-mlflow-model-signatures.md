# MLflow Model Signatures - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/model/signatures/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que são Model Signatures

Contrato que define o formato esperado de inputs, outputs e parameters. Garante consistência e validação automática.

---

## Componentes

| Componente | Descrição |
|------------|-----------|
| **Inputs Schema** | Estrutura e tipos dos dados de entrada |
| **Outputs Schema** | Estrutura e tipos das saídas |
| **Parameters Schema** | Parâmetros de inferência |

---

## Por que usar Signatures

1. **Consistency** - Garante formato consistente
2. **Validation** - Captura erros antes do modelo
3. **Documentation** - Documentação viva do modelo
4. **Deployment Safety** - Validação automática em deployment
5. **UI Integration** - MLflow UI mostra requirements
6. **Databricks Unity Catalog** - OBRIGATÓRIO para registro

---

## Signature Types

### Column-Based (DataFrames)

```python
from mlflow.types.schema import Schema, ColSpec

input_schema = Schema([
    ColSpec("double", "feature_1"),
    ColSpec("string", "feature_2"),
    ColSpec("long", "feature_3", required=False),  # Opcional
])

output_schema = Schema([
    ColSpec("double", "prediction")
])
```

### Tensor-Based (NumPy)

```python
from mlflow.types.schema import Schema, TensorSpec

input_schema = Schema([
    TensorSpec(np.dtype(np.float32), (-1, 28, 28, 1))  # Batch de imagens 28x28
])
```

---

## Data Types

### Primitive Types

| Python Type | MLflow Type | Exemplo |
|-------------|-------------|---------|
| str | string | "hello" |
| int | long | 42 |
| np.int32 | integer | np.int32(42) |
| float | double | 3.14 |
| np.float32 | float | np.float32(3.14) |
| bool | boolean | True |
| datetime | datetime | pd.Timestamp("2023-01-01") |
| bytes | binary | b"data" |

### Composite Types

```python
# Arrays (Lists/NumPy)
{"simple_list": ["a", "b", "c"]}
{"nested_array": [[1, 2], [3, 4]]}

# Objects (Dictionaries)
{"user_profile": {"name": "Alice", "age": 30}}

# Optional Fields
pd.DataFrame({
    "required_field": [1, 2, 3],
    "optional_field": [1.0, None, 3.0],  # None torna opcional
})
```

---

## Type Hints (MLflow 2.20.0+)

```python
from typing import List, Dict, Optional
import pydantic
import mlflow.pyfunc

class Message(pydantic.BaseModel):
    role: str
    content: str
    metadata: Optional[Dict[str, str]] = None

class CustomModel(mlflow.pyfunc.PythonModel):
    def predict(self, model_input: List[Message]) -> List[str]:
        # Signature inferida automaticamente!
        return [msg.content for msg in model_input]

with mlflow.start_run():
    mlflow.pyfunc.log_model(
        name="chat_model",
        python_model=CustomModel(),
        input_example=[{"role": "user", "content": "Hello"}]
    )
```

**Benefícios:**
- Validação automática em runtime
- Schema inference automática
- Type safety
- IDE support melhorado
- Documentação auto-gerada

---

## Criando Signatures

### Automatic Inference

```python
from mlflow.models import infer_signature

# Mais simples - inferir automaticamente
predictions = model.predict(X_test)
signature = infer_signature(X_test, predictions)

mlflow.sklearn.log_model(model, name="model", signature=signature)
```

### Manual Creation

```python
from mlflow.models import ModelSignature
from mlflow.types.schema import Schema, ColSpec

input_schema = Schema([
    ColSpec("double", "feature_1"),
    ColSpec("string", "feature_2"),
])

output_schema = Schema([ColSpec("double", "prediction")])

signature = ModelSignature(inputs=input_schema, outputs=output_schema)
```

### Com Input Example

```python
# MLflow infere signature automaticamente
mlflow.sklearn.log_model(
    model,
    name="my_model",
    input_example=X_train.iloc[[0]],  # Signature inferida
)
```

---

## Validation Rules

### Input Validation

| Situação | Resultado |
|----------|-----------|
| Required field missing | ❌ Validation fails |
| Optional field missing | ✅ OK (ignored) |
| Extra fields | ✅ OK (ignored) |
| Type conversion safe | ✅ Auto-convert |
| Type conversion unsafe | ❌ Validation fails |

### Safe Conversions

```
int → long      ✅ (32-bit to 64-bit)
int → double    ✅ (integer to float)
float → double  ✅ (32-bit to 64-bit)
long → double   ❌ (precision loss)
string → int    ❌ (no parsing)
```

---

## Input Examples

### Benefits

1. **Signature Inference** - Auto-generate signatures
2. **Model Validation** - Verify model works during logging
3. **Dependency Detection** - Identify required packages
4. **Documentation** - Show proper input format
5. **Deployment Testing** - Validate REST payloads

### Formats

```python
import pandas as pd

# Single record
single = pd.DataFrame([{"sepal_length": 5.1, "sepal_width": 3.5}])

# Batch
batch = pd.DataFrame([
    {"feature_1": 1.0, "feature_2": "A"},
    {"feature_1": 2.0, "feature_2": "B"},
])
```

### Serving Examples

Quando você loga com `input_example`:

```python
mlflow.sklearn.log_model(model, name="model", input_example=X_sample)
```

MLflow cria automaticamente:
- `input_example.json` - Formato original
- `serving_input_example.json` - Formato REST API

---

## Best Practices

### Always Include Input Examples

```python
# ✅ Good
mlflow.sklearn.log_model(model, name="model", input_example=X_sample)

# ❌ Avoid
mlflow.sklearn.log_model(model, name="model")  # No signature/validation
```

### Test Your Signatures

```python
signature = infer_signature(X_test, y_pred)
loaded_model = mlflow.pyfunc.load_model(model_uri)

try:
    result = loaded_model.predict(X_test)
    print("✅ Signature validation passed")
except Exception as e:
    print(f"❌ Signature issue: {e}")
```

### Handle Integers with NaN

```python
# ❌ Problem: Integers with NaN become floats
df = pd.DataFrame({"int_col": [1, 2, None]})  # Type: float64

# ✅ Solution: Use consistent types
df = pd.DataFrame({"int_col": [1.0, 2.0, None]})  # Explicit float64
```

---

## Troubleshooting

### "Required input field missing"

```python
# Problem: Model expects field "age" but input only has "name"
input_data = {"name": "Alice"}  # Missing "age"

# Solution: Include all required fields or make optional
input_data = {"name": "Alice", "age": None}  # Optional field
```

### "Cannot convert type X to type Y"

```python
# Problem: String where integer expected
input_data = {"score": "85"}  # String value

# Solution: Fix types
input_data = {"score": 85}  # Integer value
```

### "Tensor shape mismatch"

```python
# Problem: Shape mismatch
input_tensor = np.random.random((10, 28, 28))  # Wrong shape

# Solution: Reshape to match signature
input_tensor = input_tensor.reshape(10, 784)  # Correct shape
```

---

## Conceitos Aprendidos

1. **Signature** - Contrato de inputs/outputs/parameters
2. **Column-Based** - Para DataFrames (tabular)
3. **Tensor-Based** - Para NumPy (deep learning)
4. **Type Hints** - Signature automática via type annotations
5. **Input Example** - Validação e documentação
6. **Validation Rules** - Safe vs unsafe conversions
7. **Serving Examples** - Payloads para REST API

---

## Key Points

- **Databricks Unity Catalog REQUIRES signatures**
- Use `infer_signature()` for automatic inference
- Always include `input_example` when logging
- Type hints (MLflow 2.20+) enable automatic validation
- Optional fields use `required=False` or `None` values