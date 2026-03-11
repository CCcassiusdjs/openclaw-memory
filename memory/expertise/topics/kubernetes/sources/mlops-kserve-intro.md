# KServe: Introdução ao Model Serving em Kubernetes

**Fonte:** https://kserve.github.io/website/  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

KServe é a plataforma open-source padrão para servir modelos de ML em Kubernetes, oferecendo suporte unificado para IA Generativa e Preditiva.

## Conceitos-Chave

### Arquitetura
- **Control Plane**: Gerencia ciclo de vida dos modelos, tracking de revisões, canary rollouts, A/B testing
- **Data Plane**: Protocolo de inferência padronizado para servidores de modelos (request/response APIs)
- **InferenceService**: CRD principal para deployment de modelos com autoscaling automático
- **Inference Graph**: Pipelines para pre/post processing, ensembles, workflows multi-modelo

### Features Principais

#### Generative AI
- Backends otimizados: vLLM e llm-d
- Protocolo OpenAI-compatible
- GPU acceleration com gerenciamento de memória otimizado
- Model caching inteligente
- KV cache offloading para CPU/disk
- Autoscaling baseado em requests
- Suporte nativo a Hugging Face

#### Predictive AI
- Multi-framework: TensorFlow, PyTorch, scikit-learn, XGBoost, ONNX
- Routing inteligente entre predictor, transformer, explainer
- Canary rollouts e inference pipelines
- Scale-to-zero
- Model explainability integrado
- Monitoring avançado (payload logging, drift detection, adversarial detection)

## Exemplo de Uso

```yaml
apiVersion: "serving.kserve.io/v1beta1"
kind: "InferenceService"
metadata:
  name: "llm-service"
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      resources:
        limits:
          cpu: "6"
          memory: 24Gi
          nvidia.com/gpu: "1"
      storageUri: "hf://meta-llama/Llama-3.1-8B-Instruct"
```

## Quick Start

```bash
# Instalar KServe
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.11.0/kserve.yaml

# Deploy modelo
kubectl apply -f inference-service.yaml

# Fazer inferência
curl -v -H "Host: qwen-llm.default.example.com" \
  http://localhost:8080/openai/v1/chat/completions -d @./prompt.json
```

## Empresas que Usam

Bloomberg, IBM, Red Hat, NVIDIA, AMD, Cisco, Gojek, Wikimedia, Naver, Zillow, Intuit, entre outras.

## Insights

- KServe é o padrão de fato para model serving em Kubernetes
- Unified platform para GenAI e Predictive AI
- CRD simplifica deployment com autoscaling, networking e health checks automáticos
- Suporte a scale-to-zero reduz custos
- Integrations com Kubeflow para ML lifecycle completo