# LLM Inference on Kubernetes: vLLM and Triton

**Fonte:** Multiple sources (2025-2026)  
**Data:** 2026-03-11  
**Status:** Lido

## Resumo Executivo

vLLM e Triton Inference Server são as principais soluções para serving de LLMs em Kubernetes, cada um com strengths específicos.

## vLLM: High-Performance LLM Serving

### O que é
- Engine otimizada para LLM inference
- High-throughput, low-latency
- Open-source, cloud-agnostic

### Features Principais
| Feature | Descrição |
|---------|-----------|
| **PagedAttention** | Memory management eficiente |
| **Continuous Batching** | Dynamic batch sizes |
| **KV Cache** | Optimized caching |
| **Distributed Inference** | Multi-GPU support |
| **OpenAI-compatible API** | Easy integration |

### Integração com KServe
```yaml
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: llm-service
spec:
  predictor:
    model:
      modelFormat:
        name: huggingface
      resources:
        limits:
          nvidia.com/gpu: 1
      storageUri: "hf://meta-llama/Llama-3.1-8B-Instruct"
```

### KServe v0.15+ Features
- First-class LLM support
- vLLM backend integration
- LLMInferenceService CRD
- llm-d integration para distributed serving

## Triton Inference Server

### O que é
- NVIDIA's inference server
- Multi-framework support
- Production-ready serving

### Features Principais
| Feature | Descrição |
|---------|-----------|
| **Multi-Framework** | TensorFlow, PyTorch, ONNX, TensorRT |
| **Model Ensembles** | Pipeline parallelism |
| **Dynamic Batching** | Automatic request batching |
| **Multi-GPU** | Scalable inference |
| **Kubernetes-native** | KServe integration |

### vLLM Backend for Triton
- Combina vLLM optimization com Triton infrastructure
- Triton gerencia serving infrastructure
- vLLM gerencia LLM-specific optimization
- Ideal para AMD GPUs com ROCm

## Comparação vLLM vs Triton

| Aspecto | vLLM | Triton |
|---------|------|--------|
| **Focus** | LLM-specific | General ML models |
| **Hardware** | Multi-vendor (NVIDIA, AMD) | NVIDIA-focused |
| **Features** | PagedAttention, continuous batching | Model ensembles, multi-framework |
| **Kubernetes** | KServe, Kaito | KServe, Helm |
| **API** | OpenAI-compatible | Custom + OpenAI |
| **Best For** | High-throughput LLM serving | Multi-model inference pipelines |

## LLM Inference Challenges on Kubernetes

### Token-by-Token Generation
- GPU occupied durante toda resposta
- Concurrency management crítico
- Batch scheduling importante

### Solutions
1. **Continuous Batching**: Dynamic batch composition
2. **KV Cache**: Reuse attention computations
3. **Prefill-Decode Disaggregation**: Separate phases
4. **Multi-LoRA Adapters**: Serve multiple adapters

## llm-d: Next-Gen LLM Serving

### O que é
- Kubernetes operator para LLM serving
- GPU scheduling otimizado
- Model lifecycle management

### Features
- SGLang integration (most advanced engine)
- vLLM support
- TensorRT-LLM support
- Triton support
- Cache-aware load balancing
- Multi-node deployment
- Prefill-decode disaggregated serving
- Multi-LoRA adapter serving

### Stack Completa
```
llm-d Operator → KServe/Kaito → vLLM/Triton/SGLang → GPU
```

## Monitoring & Observability

### Tools
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards
- **OpenTelemetry**: Distributed tracing
- **GenAI-Perf**: NVIDIA's LLM metrics tool

### Key Metrics
| Métrica | Descrição |
|---------|-----------|
| **Time-to-First-Token (TTFT)** | Latência inicial |
| **Tokens per Second** | Throughput |
| **GPU Utilization** | Resource efficiency |
| **Memory Usage** | KV cache size |
| **Queue Length** | Pending requests |

## Kaito: Kubernetes AI Toolchain Operator

### O que é
- Simplifies AI inference server installation
- Uses vLLM by default
- Kubernetes-native management

### Features
- Auto-provision GPU nodes
- Model auto-download
- Inference server setup
- Integration with Azure AKS

## Insights

- vLLM é melhor para pure LLM serving com high throughput
- Triton é melhor para multi-model inference pipelines
- KServe v0.15+ tem first-class LLM support
- llm-d é o próximo nível: operator para LLM lifecycle
- Continuous batching é crítico para efficiency
- Monitoring específico para LLM (TTFT, tokens/sec) é essencial
- Kaito simplifica deployment em Kubernetes