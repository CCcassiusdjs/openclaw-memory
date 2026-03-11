# MLflow Autologging - Guia Completo

**Fonte:** DOC-010 - MLflow Blog: Autolog  
**URL:** https://mlflow.org/blog/mlflow-autolog  
**Tipo:** Blog Oficial  
**Data:** 2024  
**Status:** completed

---

## Resumo

Guia detalhado sobre mlflow.autolog() - funcionalidade de logging automático para métricas, parâmetros e artefatos sem necessidade de código manual. Suporta múltiplas bibliotecas ML (PyTorch, sklearn, XGBoost, etc).

---

## Conceitos-Chave

### O que é Autologging

`mlflow.autolog()` instrui MLflow a capturar dados essenciais automaticamente, sem necessidade de especificar manualmente. É ponto de entrada acessível para capacidades de logging do MLflow.

```python
import mlflow
mlflow.autolog()
```

### O que é Capturado Automaticamente

1. **Metrics**: medidas de treinamento e avaliação (accuracy, F1 score, etc.)
2. **Parameters**: hiperparâmetros (learning rate, n_estimators, etc.)
3. **Artifacts**: arquivos importantes (modelos treinados)
4. **Metadata**: versões de software, git commit hash, nome do arquivo

### Dois Modos de Uso

#### 1. mlflow.autolog() - Broad Approach
```python
mlflow.autolog()  # Habilita para TODAS as bibliotecas suportadas
```
- Ideal para prototyping e exploração
- One-size-fits-all
- Não requer `mlflow.start_run()` - cria run automaticamente

#### 2. Library-specific autolog() - Fine-grained
```python
mlflow.sklearn.autolog()
mlflow.pytorch.autolog(log_every_n_epoch=10, log_every_n_step=100)
mlflow.xgboost.autolog()
```
- Controle mais fino por biblioteca
- Argumentos específicos: `log_every_n_epoch`, `log_every_n_step`
- Configuração customizada por framework

### Exemplo Completo

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import datasets

# Dados
X, y = datasets.make_classification(n_samples=1000, class_sep=0.5, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

# Autolog habilitado
mlflow.autolog()

# Treinamento - run é criado automaticamente
clf = RandomForestClassifier(n_estimators=200, max_depth=10)
clf.fit(X_train, y_train)
clf.score(X_val, y_val)

# Recuperar último run
mlflow.last_active_run()
```

### Métricas Automaticamente Logadas (sklearn)

```python
{
  'RandomForestClassifier_score_X_val': 0.72,
  'training_accuracy_score': 0.99625,
  'training_f1_score': 0.9962547564333545,
  'training_log_loss': 0.3354604497935824,
  'training_precision_score': 0.9962921348314606,
  'training_recall_score': 0.99625,
  'training_roc_auc': 0.9998943433719795
}
```

### Parâmetros Automaticamente Logados (sklearn)

```python
{
  'bootstrap': 'True',
  'ccp_alpha': '0.0',
  'class_weight': 'None',
  'criterion': 'gini',
  'max_depth': '10',
  'max_features': 'sqrt',
  'max_leaf_nodes': 'None',
  # ... todos os hiperparâmetros
}
```

### Tags Automaticamente Logadas

```python
{
  'estimator_class': 'sklearn.ensemble._forest.RandomForestClassifier',
  'estimator_name': 'RandomForestClassifier',
  'mlflow.autologging': 'sklearn'
}
```

---

## Configuração e Customização

### Argumentos de Controle

```python
# Desabilitar logging de datasets
mlflow.autolog(log_datasets=False)

# Desabilitar logging de models
mlflow.autolog(log_models=False)

# sklearn: limitar runs de hyperparameter search
mlflow.sklearn.autolog(max_tuning_runs=5)

# PyTorch: frequência de logging
mlflow.pytorch.autolog(log_every_n_epoch=10, log_every_n_step=100)
```

### Combinação de autologs

```python
# Autolog para todas EXCETO sklearn
mlflow.autolog()
mlflow.sklearn.autolog(disable=True)
```

Library-specific sempre sobrepõe `mlflow.autolog()`, independente da ordem.

---

## Quando NÃO Usar Autologging

1. **Poucas métricas específicas**: autolog gera mais dados do que necessário
2. **Frameworks não suportados**: precisa logging manual
3. **Valores customizados**: nem todo valor pode ser capturado automaticamente
4. **Controle fino**: logging manual para casos específicos

---

## Bibliotecas Suportadas

- Scikit-learn
- PyTorch
- TensorFlow/Keras
- XGBoost
- LightGBM
- CatBoost
- Spark MLlib
- FastAI
- Statsmodels
- Transformers (HuggingFace)

---

## Conceitos Adicionados

- Automatic run creation without start_run()
- Library-specific autolog configuration
- Training vs evaluation metrics logging
- Hyperparameter search nested runs
- git commit hash and software version metadata
- log_models and log_datasets arguments

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 20 min