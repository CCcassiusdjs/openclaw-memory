# MLflow Models - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/model/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que são MLflow Models

Formato padrão para empacotar modelos de ML que podem ser usados em diferentes downstream tools: real-time serving via REST API, batch inference no Spark, etc. Define convenção de "flavors" para interoperabilidade.

---

## Storage Format

```
model/
├── MLmodel              # YAML com flavors suportados
├── model.pkl            # Modelo serializado
├── conda.yaml           # Ambiente Conda
├── python_env.yaml      # Ambiente Python
├── requirements.txt     # Dependências pip
├── input_example.json   # Exemplo de input (opcional)
├── serving_input_example.json  # Payload REST (opcional)
└── environment_variables.txt   # Variáveis de ambiente (opcional)
```

### MLmodel File (YAML)

```yaml
time_created: 2018-05-25T17:28:53.35
run_id: abc123
signature: {...}

flavors:
  sklearn:
    sklearn_version: 0.19.1
    pickled_model: model.pkl
  python_function:
    loader_module: mlflow.sklearn
```

---

## Built-In Flavors

| Flavor | Descrição |
|--------|-----------|
| **python_function** | Interface genérica Python (default) |
| **sklearn** | Scikit-learn models |
| **pytorch** | PyTorch models |
| **tensorflow** | TensorFlow/Keras models |
| **xgboost** | XGBoost models |
| **lightgbm** | LightGBM models |
| **catboost** | CatBoost models |
| **keras** | Keras models |
| **onnx** | ONNX models |
| **spark** | Spark MLlib models |
| **h2o** | H2O models |
| **statsmodels** | Statsmodels models |
| **prophet** | Prophet models |
| **transformers** | HuggingFace Transformers |

---

## Python Function (pyfunc)

Interface genérica para qualquer modelo Python:

```python
import mlflow.pyfunc

# Carregar como pyfunc
model = mlflow.pyfunc.load_model("models:/my_model/1")

# Predizer
predictions = model.predict(data)
```

### Scoring Methods

| Método | Descrição |
|--------|-----------|
| `predict(data, params=None)` | Scoring síncrono |
| `predict_stream(data, params=None)` | Scoring streaming (gerador) |

### Input Types Suportados

- pandas.DataFrame
- pandas.Series
- numpy.ndarray
- csc_matrix, csr_matrix
- List[Any]
- Dict[str, Any]
- str

---

## Model API

```python
from mlflow.models import Model

# Criar modelo
model = Model()

# Adicionar flavor
model.add_flavor("sklearn", sklearn_version="1.0", pickled_model="model.pkl")

# Salvar localmente
model.save("/path/to/model")

# Logar como artifact
model.log()

# Carregar
loaded = Model.load("/path/to/model")
```

---

## Models From Code (MLflow 2.12.2+)

Feature experimental para definir modelos diretamente de scripts Python:

```python
# my_model.py
import mlflow
from mlflow.models import set_model

class MyModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input):
        return model_input

# Registra o modelo
set_model(MyModel())
```

```python
# script principal
import mlflow

with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        python_model="my_model.py",  # Caminho do arquivo
        name="my_model",
    )
```

**Benefícios:**
- Bypass pickle/cloudpickle (segurança)
- Modelos que não precisam de treinamento
- Aplicações que usam serviços externos (LangChain)

**Limitações:**
- Não suporta imports de arquivos externos
- Apenas LangChain, LlamaIndex, PythonModel

---

## Environment Variables

MLflow registra variáveis de ambiente usadas durante inferência:

```python
import os
os.environ["OPENAI_API_KEY"] = "..."

class MyModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input, params=None):
        api_key = os.environ.get("OPENAI_API_KEY")
        ...
```

Arquivo `environment_variables.txt`:
```
# Variáveis de ambiente usadas durante inferência
OPENAI_API_KEY
```

---

## Loading Models

```python
# Por URI
model = mlflow.pyfunc.load_model("models:/my_model/1")

# Por run ID
model = mlflow.pyfunc.load_model("runs:/<run-id>/model")

# Por versão
model = mlflow.pyfunc.load_model("models:/my_model@champion")
```

---

## Model Config (MLflow 2.12+)

```python
# Carregar com configuração
model = mlflow.pyfunc.load_model(
    model_uri,
    model_config={"temperature": 0.93, "use_gpu": True}
)

# Inspecionar configuração
print(model.model_config)
```

---

## Custom Python Models

```python
import mlflow.pyfunc

class CustomModel(mlflow.pyfunc.PythonModel):
    def predict(self, context, model_input, params=None):
        # Lógica customizada
        return model_input * 2

# Logar
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        name="custom_model",
        python_model=CustomModel(),
        input_example={"data": [1, 2, 3]}
    )
```

---

## R Function (crate)

```r
library(mlflow)
library(carrier)

model <- lm(Sepal.Width ~ Sepal.Length, data = iris)

crate_model <- crate(
    function(new_obs) stats::predict(model, data.frame("Sepal.Length" = new_obs)),
    model = model
)

model_path <- mlflow_log_model(model = crate_model, artifact_path = "iris_prediction")
```

---

## Conceitos Aprendidos

1. **Model Format** - Diretório com MLmodel + artifacts
2. **Flavors** - Convenção para interoperabilidade
3. **pyfunc** - Interface genérica Python
4. **Models From Code** - Definir modelos via script (segurança)
5. **Environment Variables** - Registro automático para inferência
6. **Model Config** - Configuração em tempo de carga
7. **Custom Models** - PythonModel para lógica customizada

---

## Notas para Implementação

- Usar pyfunc como interface padrão para deployment
- Models from code para segurança (evitar pickle malicioso)
- Sempre definir signature e input_example
- Logar variáveis de ambiente necessárias
- Usar Model Registry para versionamento