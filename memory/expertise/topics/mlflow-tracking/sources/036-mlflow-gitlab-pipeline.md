# MLflow GitLab Model Registry Pipeline - Tutorial

**Fonte:** TUT-002 - Build an ML App Pipeline with GitLab Model Registry Using MLflow  
**URL:** https://about.gitlab.com/blog/build-an-ml-app-pipeline-with-gitlab-model-registry-using-mlflow/  
**Tipo:** Tutorial  
**Data:** Setembro 2024  
**Status:** completed

---

## Resumo

Tutorial completo de pipeline MLOps com GitLab Model Registry e MLflow: environment setup, training at merge request, model registration, Docker deployment.

---

## Why MLOps?

### ML Lifecycle Challenges
- Large datasets handling
- Various models experimentation
- Continuous model updates
- Model drift management
- Reproducibility and scalability

### GitLab MLOps Features
- Source code management
- CI/CD pipelines automation
- Tracking and collaboration tools
- Merge requests and code reviews
- Model Registry integration

---

## Prerequisites

- Basic knowledge of GitLab pipelines
- Basic knowledge of MLflow
- Kubernetes cluster
- Dockerfile

---

## Environment Variables Setup

```bash
export MLFLOW_TRACKING_URI="<your gitlab endpoint>/api/v4/projects/<your project id>/ml/mlflow"
export MLFLOW_TRACKING_TOKEN="<your_access_token>"
```

**Note**: Remove `mlflow.set_tracking_uri()` from training code when using environment variables.

---

## Training and Logging at Merge Request

### MLflow Logging in Code

```python
import mlflow

# Log parameters
mlflow.log_params(params)

# Log metrics
mlflow.log_metrics(metrics_data)

# Log artifacts
mlflow.log_artifact(artifacts)

# Set experiment
mlflow.set_experiment("experiment_name")
```

### Pipeline Trigger
- Trigger manually in merge requests
- Observe report generated as MR Note
- View candidate details in Analyze > Model Experiments

---

## Registering the Best Candidate

### Get Run Information

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get source candidate run
source_candidate = client.get_run(source_candidate_id)
params = {k: v for k, v in source_candidate.data.params.items()}
metrics = {k: v for k, v in source_candidate.data.metrics.items()}
```

### Register Model Version

```python
# Create model version
model_version = client.get_model_version(model_name, version)
run_id = model_version.run_id

# Log params and metrics to registered model
for name, value in params.items():
    client.log_param(run_id, name, value)

for name, value in metrics.items():
    client.log_metric(run_id, name, value)

# Register artifacts
mlflow.log_artifact("model.pkl")
```

### Semantic Versioning
- Use semantic versioning for model versions
- Create steps as separate stages and components
- Reusable across projects

---

## CI/CD Components

### Why Use Components?
- Structured environment for ML workflows
- Reusability across projects
- Standardized scripts, models, datasets
- Reduce redundancy

### Example Component Structure

```yaml
# templates/register-candidate.yml
spec:
  inputs:
    model_name:
      type: string
    source_run_id:
      type: string
---
register_candidate:
  script:
    - python register_candidate.py --model-name $[[ inputs.model_name ]] --run-id $[[ inputs.source_run_id ]]
```

---

## Dockerize and Deploy

### Build Docker Image

```dockerfile
FROM python:3.9

# Copy model artifact
COPY model.pkl /app/model.pkl
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### Deploy to Container Registry

```yaml
docker_build:
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

### Access and Deploy
- Docker image available in GitLab Container Registry
- Deploy to Kubernetes cluster
- Use any deployment method (helm, kubectl, etc.)

---

## Pipeline Flow

```
1. Set Environment Variables
   └─> MLFLOW_TRACKING_URI, MLFLOW_TRACKING_TOKEN

2. Train at Merge Request
   └─> log_params(), log_metrics(), log_artifact()

3. Register Best Candidate
   └─> Create model version, log params/metrics/artifacts

4. Dockerize
   └─> Build image with model artifact

5. Deploy
   └─> Push to Container Registry, deploy to cluster
```

---

## Resources

- [Model experiments](https://docs.gitlab.com/ee/user/project/ml/experiment_tracking/)
- [MLflow client compatibility](https://docs.gitlab.com/ee/user/project/ml/experiment_tracking/mlflow_client.html)
- [CI/CD components](https://docs.gitlab.com/ee/ci/components/)
- [GitLab Container Registry](https://about.gitlab.com/blog/next-generation-gitlab-container-registry-goes-ga/)

---

## Concepts Adicionados

- GitLab Model Registry integration
- MLflow environment variables pattern
- Semantic versioning for models
- CI/CD components reusability
- Docker build with model artifacts
- Container Registry deployment
- MR-based model training

---

**Lido em:** 2026-03-11  
**Tempo estimado:** 20 min