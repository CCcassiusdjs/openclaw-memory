# MLflow Tracking APIs - Resumo

**Fonte:** https://mlflow.org/docs/latest/ml/tracking/tracking-api/  
**Tipo:** Documentação Oficial  
**Status:** completed  
**Lido em:** 2026-03-11

---

## Conceitos Principais

### Dois Métodos de Tracking

1. **Autologging** - Zero setup, logging automático
   - Uma linha: `mlflow.autolog()`
   - Captura: parâmetros, métricas, artefatos, modelos, visualizações
   - Suporta: sklearn, xgboost, lightgbm, pytorch, keras/tensorflow, spark, statsmodels

2. **Manual Logging** - Controle total
   - `mlflow.start_run()`, `mlflow.log_param()`, `mlflow.log_metric()`, `mlflow.log_artifact()`
   - Ideal para loops de treinamento customizados

### Core API Functions

**Setup & Configuration:**
- `mlflow.set_tracking_uri()` - Conectar ao tracking server
- `mlflow.get_tracking_uri()` - Obter URI atual
- `mlflow.create_experiment()` - Criar novo experimento
- `mlflow.set_experiment()` - Definir experimento ativo

**Run Management:**
- `mlflow.start_run()` - Iniciar run (context manager)
- `mlflow.end_run()` - Finalizar run
- `mlflow.active_run()` - Obter run ativo
- `mlflow.last_active_run()` - Último run completado

**Data Logging:**
- `mlflow.log_param()` / `mlflow.log_params()` - Parâmetros
- `mlflow.log_metric()` / `mlflow.log_metrics()` - Métricas
- `mlflow.log_input()` - Dataset info
- `mlflow.set_tag()` / `mlflow.set_tags()` - Metadados

**Artifact Management:**
- `mlflow.log_artifact()` - Log arquivo único
- `mlflow.log_artifacts()` - Log diretório inteiro
- `mlflow.get_artifact_uri()` - URI do artifact

### MLflow 3 - Logged Model Management (NOVO)

- `mlflow.initialize_logged_model()` - Criar modelo em estado PENDING
- `mlflow.create_external_model()` - Modelos armazenados fora do MLflow
- `mlflow.finalize_logged_model()` - Atualizar status para READY/FAILED
- `mlflow.get_logged_model()` - Recuperar modelo por ID
- `mlflow.last_logged_model()` - Último modelo logado
- `mlflow.search_logged_models()` - Buscar modelos
- `mlflow.set_active_model()` - Definir modelo ativo para trace linking

### Hierarchical Runs (Parent/Child)

```python
with mlflow.start_run(run_name="parent") as parent:
    mlflow.log_param("search_strategy", "random")
    
    for lr in [0.001, 0.01, 0.1]:
        with mlflow.start_run(nested=True, run_name=f"lr_{lr}") as child:
            mlflow.log_param("learning_rate", lr)
            # ... training ...
```

### System Tags (Automáticos)

| Tag | Descrição |
|-----|-----------|
| `mlflow.source.name` | Arquivo/notebook fonte |
| `mlflow.source.type` | Tipo (NOTEBOOK, JOB, LOCAL) |
| `mlflow.user` | Usuário que criou |
| `mlflow.source.git.commit` | Git commit hash |
| `mlflow.parentRunId` | ID do pai (nested runs) |

### Precise Metric Tracking

- `step` - Iteração/epoch customizado
- `timestamp` - Timestamp em millisegundos
- Pode logar com gaps (1, 5, 75, -20)

---

## Conceitos Aprendidos

1. **Autologging** - Uma linha para logging automático completo
2. **Run Hierarchy** - Runs aninhados para hyperparameter sweeps
3. **Model Lifecycle (MLflow 3)** - Estados PENDING → READY/FAILED
4. **External Models** - Modelos fora do MLflow podem ser trackeados
5. **System Tags** - Tags automáticas para contexto de execução
6. **Step/Timestamp** - Controle fino de métricas ao longo do tempo

---

## Notas para Implementação

- Usar `mlflow.autolog()` como padrão inicial
- Combinar autolog + manual para customizações
- Parent/child runs para hyperparameter tuning
- Tags para organização e filtros
- Model Registry para versionamento de modelos em produção