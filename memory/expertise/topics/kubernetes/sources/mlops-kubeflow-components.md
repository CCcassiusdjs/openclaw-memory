# Kubeflow: Componentes e Arquitetura

**Fonte:** https://www.kubeflow.org/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

Kubeflow é a fundação de ferramentas para plataformas de IA em Kubernetes, oferecendo uma plataforma AI de referência componível, modular, portável e escalável.

## Componentes Principais

### Spark Operator
- Especificação e execução de aplicações Spark de forma idiomática no Kubernetes

### Notebooks
- Ambientes de desenvolvimento interativo para AI, ML e Data workloads
- Jupyter notebooks executando diretamente no cluster

### Trainer
- Fine-tuning de LLMs
- Treinamento distribuído escalável
- Suporte: PyTorch, HuggingFace, DeepSpeed, MLX, JAX, XGBoost

### Katib
- AutoML Kubernetes-native
- Hyperparameter tuning
- Early stopping
- Neural architecture search

### KServe
- Model serving padronizado
- Deploy escalável multi-framework
- Suporte GenAI e Predictive AI

### Model Registry
- Single pane of glass para modelos
- Indexação e gestão de versões
- Gap entre experimentação e produção

### Pipelines (KFP)
- Workflows ML portáteis e escaláveis
- Deploy de pipelines usando Kubernetes

### Central Dashboard
- Hub autenticado para interfaces web
- Conecta todos os componentes do ecossistema

## Arquitetura

Kubeflow é projetado para ser:
- **Componível**: Usar cada projeto independentemente ou deploy completo
- **Modular**: Componentes podem ser substituídos
- **Portável**: Roda em qualquer Kubernetes
- **Escalável**: Backed by Kubernetes-native projects

## Casos de Uso

1. **Desenvolvimento**: Notebooks interativos no cluster
2. **Treinamento**: Distribuído com Trainer
3. **AutoML**: Hyperparameter tuning com Katib
4. **Serving**: Model deployment com KServe
5. **Pipelines**: ML workflows automatizados
6. **Registry**: Gestão de modelos e versões

## Insights

- Kubeflow é a plataforma ML mais completa para Kubernetes
- Integração nativa com ecosystem Kubernetes
- Ideal para teams que precisam de ML lifecycle completo
- Complexidade inicial alta, mas poderoso uma vez configurado