# MLflow Autologging - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/tracking/autolog/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## O que é Autologging

Feature que loga automaticamente métricas, parâmetros e modelos sem código explícito. Basta:

```python
import mlflow
mlflow.autolog()

with mlflow.start_run():
    model.fit(X_train, y_train)  # MLflow loga automaticamente
```

---

## O que é Logado Automaticamente

1. **Metrics** - Métricas pré-selecionadas baseadas no modelo/library
2. **Parameters** - Hiperparâmetros + defaults
3. **Model Signature** - Schema de input/output
4. **Artifacts** - Model checkpoints
5. **Dataset** - Dataset usado para treino (se aplicável)

---

## Customização

```python
mlflow.autolog(
    log_model_signatures=False,
    extra_tags={"YOUR_TAG": "VALUE"},
)
```

---

## Bibliotecas Suportadas

### Keras/TensorFlow
- Training/validation loss, user metrics
- Optimizer name, learning rate
- Model summary, TensorBoard logs
- EarlyStopping callback metrics

### LightGBM
- User-specified metrics
- lightgbm.train parameters
- Feature importance, input example
- Early stopping metrics

### PyTorch (via Lightning)
- Training loss, validation loss, test accuracy
- Optimizer params
- Model summary, checkpoints
- EarlyStopping callback support

### Scikit-learn
- Training score
- estimator.get_params()
- Fitted estimator
- GridSearchCV: parent run + child runs
- Best params, search results CSV

### XGBoost
- User-specified metrics
- xgboost.train parameters
- Feature importance, input example
- Early stopping metrics

### Outros
- **Paddle** - metrics, params, model signature
- **PySpark ML** - post-training metrics, fitted estimator
- **Spark** - datasource info (path, version, format)
- **Statsmodels** - metrics, params, model

---

## Behavior

| Situação | Autolog cria run? | Autolog termina run? |
|----------|-------------------|---------------------|
| Run inexistente | ✅ Sim | ✅ Sim (após training) |
| Run existente | ❌ Não (usa atual) | ❌ Não (deixa aberto) |

---

## Library-Specific Autolog

```python
# Habilitar apenas para PyTorch
mlflow.pytorch.autolog()

# Desabilitar para sklearn, manter para outros
mlflow.sklearn.autolog(disable=True)
mlflow.autolog()
```

---

## GridSearchCV Behavior (sklearn)

Estrutura hierárquica automática:
```
Parent run
├── Child run 1 (param combination 1)
├── Child run 2 (param combination 2)
└── Child run 3 (param combination 3)
```

Parent run contém:
- Training score
- Best parameter combination
- Fitted parameter search estimator
- Search results CSV

Child runs contêm:
- CV test score
- Parameter combination

---

## Conceitos Aprendidos

1. **Zero-setup logging** - Uma linha para logging completo
2. **Framework-specific** - Cada framework loga diferentes métricas
3. **Run management** - Autolog cria/termina runs automaticamente se necessário
4. **Hierarchical runs** - GridSearchCV cria parent + child runs
5. **Selective autolog** - Habilitar/desabilitar por framework
6. **Model artifacts** - Checkpoints e modelos salvos automaticamente

---

## Notas para Implementação

- Sempre usar `mlflow.autolog()` como primeira linha
- Combinar com logging manual para customizações
- Verificar compatibilidade da versão do framework
- Usar `extra_tags` para metadados adicionais
- Para hyperparameter search, usar sklearn autolog (hierquia automática)