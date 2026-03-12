# W&B Experiments Tracking - Resumo

**Fonte:** https://docs.wandb.ai/guides/track
**Tipo:** Documentation
**Data:** 2026-03-12

---

## 🎯 O que é W&B Experiments?

**Weights & Biases** é uma plataforma para **rastrear experimentos ML** com poucas linhas de código:
- Visualização interativa
- Comparação de runs
- Exportação para Python

## 📋 Como Funciona

### Workflow Básico
```python
import wandb

# 1. Iniciar run
with wandb.init(entity="", project="my-project-name") as run:
    # 2. Salvar hyperparameters
    run.config.learning_rate = 0.01
    
    # 3. Training loop
    for epoch in range(num_epochs):
        # Log métricas
        run.log({"loss": loss, "accuracy": acc})
    
    # 4. Salvar artefatos
    run.log_artifact(model)
```

## 🔧 Componentes Principais

| Componente | Descrição |
|------------|-----------|
| **Run** | Single experiment execution |
| **Config** | Hyperparameters dictionary |
| **Log** | Metrics over time |
| **Artifact** | Model outputs, datasets |

## 📊 Features

### Tracking
- Hyperparameters (`run.config`)
- Metrics over time (`run.log()`)
- Artifacts (`run.log_artifact()`)

### Visualization
- Interactive dashboard
- Compare multiple runs
- Export to Python

### Integrations
- Keras, PyTorch, TensorFlow
- Scikit-learn, XGBoost
- Many more frameworks

## 🚀 Quickstart

### Instalação
```bash
pip install wandb
```

### Login
```python
wandb.login()
```

### Run Básico
```python
with wandb.init(project="my-project") as run:
    run.config.epochs = 10
    run.config.lr = 0.001
    
    for epoch in range(10):
        # Training...
        run.log({"loss": loss, "acc": acc})
```

## 💡 Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **Run** | Execução única de experimento |
| **Config** | Parâmetros de configuração |
| **Log** | Métricas ao longo do tempo |
| **Artifact** | Outputs salvos (modelos, datasets) |
| **Workspace** | Dashboard interativo |
| **Entity** | User ou team |

## 📊 Dashboard

O dashboard W&B permite:
- Visualizar métricas em tempo real
- Comparar múltiplas runs
- Filtrar e agrupar experiments
- Exportar dados para análise

## 🔗 Referências Cruzadas

- Alternativa a: MLflow Tracking (031-034)
- Complementa: MLflow Model Registry (016-020)
- Relacionado a: Neptune, Comet

---

**Conceitos aprendidos:** 10
**Relevância:** Alta (experiment tracking popular)