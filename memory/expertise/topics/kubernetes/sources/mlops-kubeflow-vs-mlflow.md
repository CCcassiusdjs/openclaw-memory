# Kubeflow vs MLflow: Comparação Completa

**Fonte:** https://valohai.com/blog/kubeflow-vs-mlflow/  
**Data:** 2026-03-11  
** Status:** Lido

## Resumo Executivo

Kubeflow e MLflow são as duas plataformas open-source mais populares para ML, mas com abordagens fundamentalmente diferentes.

## Kubeflow - Componentes

### Notebooks
- Criação e gestão de Jupyter notebooks em ambientes corporativos
- Notebook containers/pods diretamente no cluster

### TensorFlow Training
- Job operator customizado para TensorFlow
- Suporte a outros frameworks via operators (maturidade variável)

### Pipelines
- Workflows multi-step em containers Docker
- Orchestration de ML pipelines

### Deployment
- Modelos servidos em Kubernetes via addons externos

## MLflow - Componentes

### Tracking
- API e UI para logging de parâmetros, métricas, versões de código
- Visualização de runs

### Projects
- Empacotamento padrão de código de data science
- Git repository com descriptor de dependências

### Models
- Distribuição de modelos em várias flavors
- Ferramentas de deployment multi-plataforma

### Registry
- Model store centralizado
- Versioning, stage transitions, lineage, annotations

## Comparação

| Aspecto | Kubeflow | MLflow |
|---------|----------|--------|
| **Abordagem** | Container orchestration | Python tracking app |
| **Setup** | Complexo (weeks-months) | Simples (days-weeks) |
| **Manutenção** | Requerded | Baixa |
| **Escalabilidade** | Alta (Kubernetes-native) | Limitada |
| **Reprodutibilidade** | Total (orchestrates tudo) | Parcial (tracking only) |
| **Pipelines** | Nativo (KFP) | Via extensions |
| **Deployment** | Kubernetes-serving | Multi-cloud (Sagemaker, etc) |
| **Target User** | Platform teams | Data scientists |

## Diferenças Fundamentais

### Orchestration vs Tracking
- **Kubeflow**: Tudo acontece DENTRO do sistema (Kubernetes infrastructure)
- **MLflow**: Treinamento acontece ONDE você quiser, MLflow apenas rastreia

### Complexidade vs Facilidade
- **Kubeflow**: Complexo de setup, mas garante reprodutibilidade total
- **MLflow**: Fácil de adotar, single service, mas menos controle

### Scale
- **Kubeflow**: Built for large-scale pipelines e HPO na cloud
- **MLflow**: Melhor para experiment tracking local/remoto

## Quando Usar Cada

### Kubeflow
- Teams grandes com infra Kubernetes
- Production ML systems complexos
- Pipelines end-to-end
- Necessidade de orquestração completa

### MLflow
- Data scientists organizando experimentos
- Projetos menores
- Rápida adoção sem infra complexa
- Model versioning simples

## Insights

- Kubeflow é sobre **infrastructure orchestration** + experiment tracking
- MLflow é sobre **experiment tracking** + model versioning
- Podem ser complementares: usar MLflow para tracking, Kubeflow para orchestration
- Valohai é alternativa managed que combina benefícios de ambos