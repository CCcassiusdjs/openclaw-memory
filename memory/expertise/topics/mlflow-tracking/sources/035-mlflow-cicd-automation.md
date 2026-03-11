# MLflow CI/CD Pipeline Automation - Guia Completo

**Fonte:** GUIDE-007 - Automate MLflow Logging With CI/CD Pipelines  
**URL:** https://aicompetence.org/automate-mlflow-logging-with-ci-cd-pipelines/  
**Tipo:** Blog/Guia  
**Data:** Junho 2025  
**Status:** completed

---

## Resumo

Guia completo sobre automação de MLflow logging com CI/CD pipelines: GitHub Actions, GitLab CI, Jenkins. Configuração, melhores práticas, dynamic tagging, conditional logging, alerting.

---

## Why Automate MLflow Logging?

### Manual Logging Problems
- Tedious and error-prone
- Inconsistent across environments
- Hard to untangle later

### Benefits of Automation
- Every run, metric, parameter captured seamlessly
- Results are repeatable and trustworthy
- Single source of truth for teams

---

## Core Tracking Components

| Component | Description |
|-----------|-------------|
| **Parameters** | Hyperparameters, config values |
| **Metrics** | Performance measures (accuracy, loss) |
| **Artifacts** | Model binaries, plots, logs, HTML reports |
| **Source Code Versions** | Git commit hash linking |

---

## CI/CD Integration Pattern

### GitHub Actions Template

```yaml
name: Train and Log Model
on: [push]
jobs:
  train:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install Dependencies
        run: pip install -r requirements.txt
      - name: Run Training
        run: python train.py
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### Key Points
- Store credentials as encrypted secrets
- Pin package versions for consistency
- Dockerize training environment for reproducibility

---

## Dynamic Experiment Tagging

```python
import mlflow
import os

# Auto-tag with CI/CD environment variables
mlflow.set_tag("branch", os.getenv("GITHUB_REF"))
mlflow.set_tag("author", os.getenv("GITHUB_ACTOR"))
mlflow.set_tag("run_id", os.getenv("GITHUB_RUN_ID"))
```

### Available Environment Variables
- `GITHUB_ACTOR` - who triggered the run
- `GITHUB_REF` - branch or tag name
- `GITHUB_RUN_ID` - unique run ID

---

## Conditional Logging

### Log Only Meaningful Runs

```yaml
on:
  push:
    branches:
      - main
```

Or in script:

```python
import os

if os.getenv("GITHUB_REF") == "refs/heads/main":
    mlflow.log_metric("accuracy", accuracy)
```

### Benefits
- Keeps MLflow clean
- Reduces artifact storage
- Saves compute budget

---

## Environment-Specific Configuration

### Separate Tracking URIs

```bash
# Development
export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI_DEV

# Staging
export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI_STAGING

# Production
export MLFLOW_TRACKING_URI=$MLFLOW_TRACKING_URI_PROD
```

### Tag Runs with Environment

```python
mlflow.set_tag("environment", "prod")
```

---

## Alerting and Monitoring

### CI Tool Notifications
- GitHub Actions: email, Slack, webhooks
- GitLab CI: email, Slack, webhooks
- Jenkins: email, Slack, custom plugins

### Alert Conditions
- MLflow tracking failures
- Missing artifacts or metrics
- Failed model validation steps

### MLflow REST API Validation

```python
import requests

# Get runs from last 30 days
response = requests.get(
    f"{MLFLOW_TRACKING_URI}/api/2.0/mlflow/experiments/{experiment_id}/search",
    json={"max_results": 100}
)

# Validate runs meet baseline performance
for run in response.json()["runs"]:
    if run["data"]["metrics"]["accuracy"] < 0.8:
        send_alert(f"Run {run['info']['run_id']} failed validation")
```

---

## Model Promotion Workflow

### Promotion Triggers
- Meet performance thresholds
- Pass validation tests
- Come from trusted branches

### Automated Stage Transitions

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Promote model if accuracy > 0.95
if accuracy > 0.95:
    client.transition_model_version_stage(
        name="my-model",
        version=version,
        stage="Staging"
    )
```

---

## Best Practices

### 1. Create a Base Logging Module
```python
# mlflow_logger.py
import mlflow

def log_training_run(params, metrics, artifacts, tags=None):
    with mlflow.start_run():
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        for artifact in artifacts:
            mlflow.log_artifact(artifact)
        if tags:
            for key, value in tags.items():
                mlflow.set_tag(key, value)
```

### 2. Standardize Tags and Metrics
- Agree on common metrics across projects
- Use consistent tag naming (author, ticket_id, environment)

### 3. Clean Up Periodically
- Archive or delete older runs
- Set retention policies for artifact store

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Environment mismatch | Pin package versions, use Docker |
| Hardcoded credentials | Use secrets managers |
| Overcomplicating early | Start simple, iterate |
| Logging every run | Use conditional logging |

---

## Concepts Adicionados

- Dynamic experiment tagging with CI/CD env vars
- Conditional logging (main branch only)
- Environment-specific tracking URIs
- CI/CD alerting patterns
- Model promotion automation
- Base logging module pattern
- Performance baseline validation
- Retention policies for runs

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 25 min