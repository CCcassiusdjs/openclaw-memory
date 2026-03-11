# MLflow Tracking Tutorial - 10 Minutes

**Fonte:** TUT-001 - Experiment Tracking with MLflow in 10 Minutes  
**URL:** https://towardsdatascience.com/experiment-tracking-with-mlflow-in-10-minutes-f7c2128b8f2c/  
**Tipo:** Tutorial  
**Data:** 2024  
**Status:** completed

---

## Resumo

Tutorial introdutório sobre MLflow Tracking para cientistas de dados. Cobre instalação, uso básico com Python, conceitos fundamentais (experiment, run), e interface web para visualização de resultados.

---

## Conceitos-Chave

### Componentes do MLflow
1. **MLflow Tracking**: registro e consulta de experimentos (código, dados, config, hiperparâmetros, métricas, resultados)
2. **MLflow Projects**: formato de empacotamento de código para runs reprodutíveis
3. **MLflow Models**: formato de empacotamento de modelos (batch e real-time scoring)
4. **MLflow Model Registry**: store centralizado com APIs e UI para gerenciar lifecycle

### Terminologias Importantes
- **Experiment**: usado para agrupar e comparar runs; geralmente é configuração de nível de projeto
- **Run**: execução individual; múltiplos runs podem pertencer ao mesmo experiment
- **Experiment ID vs Experiment Name**: não confundir!
- **Run ID vs Run Name**: inicializar com mesmo nome cria runs diferentes; mesmo ID armazena junto

### APIs de Tracking

```python
import mlflow

# Track parameters
mlflow.log_param("max_depth", 20)

# Track metrics
mlflow.log_metric("rmse", 0.5)

# Track artifact
mlflow.log_artifact("/path/graph.png", "myGraph")

# Track model (framework-specific)
mlflow.sklearn.log_model(model, "myModel")
mlflow.keras.log_model(model, "myModel")
mlflow.pytorch.log_model(model, "myModel")
```

### Querying com MLflow

```python
# Buscar runs de um experiment
runs = mlflow.search_runs(experiment_ids=[experiment_id])

# Obter melhor run por métrica
best_run = mlflow.search_runs(
    experiment_ids=[experiment_id],
    order_by=["metrics.rmse ASC"]
).iloc[0]

# Recuperar artefatos
model_path = mlflow.artifacts.download_artifacts(
    run_id=best_run.run_id,
    artifact_path="myModel"
)
```

### Interface Web

```bash
# Iniciar UI
mlflow ui

# Acessar em
http://localhost:5000
```

Features da UI:
- View experiments no painel lateral
- Runs em formato de tabela
- Metadata: runtime, status, lifecycle stage
- Artifacts: MLmodel, conda.yaml, requirements.txt
- Search bar para query por parâmetros/métricas
- Comparação gráfica de runs

---

## Fluxo de Trabalho Típico

1. Definir `EXPERIMENT_NAME`
2. `mlflow.set_experiment(EXPERIMENT_NAME)` → retorna `EXPERIMENT_ID`
3. Iniciar run: `with mlflow.start_run():`
4. Log params, metrics, model dentro do contexto
5. Query via código ou UI

---

## Dicas Práticas

- Se usar MLflow em múltiplas partes do código para mesmo run, recuperar `run_id` e inicializar com ele
- `mlruns/` folder é criado automaticamente no repositório
- Tags podem ser adicionadas manualmente na UI
- Description pode ser editada na UI sem código
- Search bar suporta filtros complexos por params/metrics

---

## Conceitos Adicionados

- Experiment vs Run terminology
- Query patterns for runs
- UI features for run comparison
- Model artifact structure (MLmodel, conda.yaml, requirements.txt)

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 15 min