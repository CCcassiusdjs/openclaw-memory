# Getting Started with Edge AI on NVIDIA Jetson: LLMs, VLMs, and Foundation Models for Robotics

**Source:** NVIDIA Developer Blog
**Authors:** NVIDIA AI-IOT Team
**Year:** 2025
**Category:** Hardware Platform & Deployment
**Relevance:** ⭐⭐⭐⭐⭐ (Essential for NVIDIA Jetson deployment)

---

## Summary

Comprehensive guide for deploying advanced AI models (LLMs, VLMs, Foundation Models) on NVIDIA Jetson edge devices. Covers hardware selection, model deployment, and robotics applications with practical tutorials.

---

## Hardware Platform Overview

### Jetson Device Selection

| Device | Memory | Model Size Target | Use Case |
|--------|--------|-------------------|----------|
| **Jetson Orin Nano Super** | 8GB | Up to 4B parameters | Fast specialized AI, SLMs |
| **Jetson AGX Orin** | 64GB | 4B-20B parameters | Medium models, multi-camera |
| **Jetson AGX Thor** | 128GB | 20B-120B+ parameters | Largest workloads, frontier models |

### Model Recommendations by Hardware

**Jetson Orin Nano (8GB):**
- Llama 3.2 3B
- Phi-3
- VILA-2.7B
- Qwen2.5-VL-3B
- Gemma-3/4B

**Jetson AGX Orin (64GB):**
- gpt-oss-20b
- Llama 3.1 70B (quantized)
- LLaVA-13B
- Qwen2.5-VL-7B
- Phi-3.5-Vision

**Jetson AGX Thor (128GB):**
- Llama 3.2 Vision 70B
- 120B-class models
- Multiple concurrent models

---

## Tutorial 1: Personal AI Assistant (LLMs + VLMs)

### Key Advantages of Local Execution

1. **Complete Privacy**
   - Prompts never leave device
   - Proprietary code stays local
   - Camera feeds remain private

2. **Zero Network Latency**
   - Instant response time
   - No API rate limits
   - Consistent performance

### Deployment Example: gpt-oss-20b on AGX Orin

**vLLM Inference Engine:**
```bash
docker run --rm -it \
  --network host \
  --shm-size=16g \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  --runtime=nvidia \
  --name=vllm \
  -v $HOME/data/models/huggingface:/root/.cache/huggingface \
  -v $HOME/data/vllm_cache:/root/.cache/vllm \
  ghcr.io/nvidia-ai-iot/vllm:latest-jetson-orin

vllm serve openai/gpt-oss-20b
```

**Performance:** 40 tokens/sec generation speed

**Open WebUI Integration:**
```bash
docker run -d \
  --network=host \
  -v ${HOME}/open-webui:/app/backend/data \
  -e OPENAI_API_BASE_URL=http://0.0.0.0:8000/v1 \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

### Vision Language Models (VLMs)

**Capabilities:**
- Scene reasoning (not just object detection)
- Answer visual queries: "Is the 3D print failing?"
- Multi-camera support
- Live video analysis

**Live VLM WebUI Setup:**
```bash
# Install ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull VLM-compatible model
ollama pull gemma3:4b

# Clone and start Live VLM WebUI
git clone https://github.com/nvidia-ai-iot/live-vlm-webui.git
cd live-vlm-webui
./scripts/start_container.sh
```

**Access:** `https://localhost:8090`

---

## Tutorial 2: Robotics with Foundation Models

### Architectural Shift in Robotics

**Traditional Approach:**
- Hard-coded logic
- Separate perception pipelines
- Explicit coding for every edge case
- Manual tuning required

**New Paradigm: End-to-End Imitation Learning**
- Foundation models (NVIDIA Isaac GR00T N1)
- Vision-Language-Action (VLA) models
- Learn policies from demonstration
- Natural language commands: "Open the drawer"

### VLA Model Architecture

```
┌─────────────────────────────────────────────────────┐
│                    VLA MODEL                        │
├─────────────────────────────────────────────────────┤
│  INPUT:                                             │
│  - Continuous visual data (camera streams)         │
│  - Natural language commands                        │
├─────────────────────────────────────────────────────┤
│  PROCESSING:                                        │
│  - Multimodal context integration                   │
│  - Scene understanding                              │
├─────────────────────────────────────────────────────┤
│  OUTPUT:                                            │
│  - Joint positions                                  │
│  - Motor velocities                                │
│  - Next timestep actions                            │
└─────────────────────────────────────────────────────┘
```

### Data Challenge & Solution

**Challenge:** Physical interaction data is expensive and slow to acquire

**Solution:** Simulation-based training

**NVIDIA Isaac Sim:**
- Generate synthetic training data
- Physics-accurate virtual environment
- Hardware-in-loop (HIL) testing
- Validate before physical deployment

### Deployment Workflow

1. **Simulate** → Isaac Sim generates synthetic data
2. **Train** → Foundation model learns policies
3. **Validate** → HIL testing with Jetson + RTX GPU
4. **Deploy** → Optimized policy to edge
5. **Optimize** → TensorRT for sub-30ms latency

---

## Key Technologies

| Technology | Purpose | Benefit |
|------------|---------|---------|
| **vLLM** | Inference engine | Efficient LLM serving |
| **TensorRT** | Model optimization | Low latency (<30ms) |
| **Isaac Sim** | Simulation | Synthetic training data |
| **Isaac GR00T N1** | Foundation model | Robotics policies |
| **Open WebUI** | User interface | Chat interface |

---

## Performance Benchmarks

| Model | Hardware | Speed | Notes |
|-------|----------|-------|-------|
| gpt-oss-20b | AGX Orin | 40 tokens/sec | Full precision |
| VILA-2.7B | Orin Nano | Real-time | Basic VLM |
| LLaVA-13B | AGX Orin | Real-time | High-resolution |
| Robotics VLA | AGX Orin | <30ms latency | Sub-30ms for control loops |

---

## Practical Deployment Patterns

### Pattern 1: Private Coding Assistant
- Run LLM locally for code generation
- No API costs, complete privacy
- Instant responses

### Pattern 2: Smart Security System
- VLM with live camera feed
- Detect anomalies, answer queries
- "Is something unusual happening?"

### Pattern 3: Wildlife Monitor
- Outdoor camera + VLM
- Identify species, behavior
- Edge processing, low power

### Pattern 4: Autonomous Robot
- VLA model for manipulation
- Simulation training → Real deployment
- Sub-30ms control loop

---

## Key Insights

1. **Hardware selection matters:** Memory determines model size
2. **Privacy is built-in:** Data never leaves device
3. **Latency is critical:** <30ms for robotics control
4. **Simulation bridges data gap:** Synthetic training is essential
5. **TensorRT optimization:** Enables heavy transformer policies at edge

---

## Related Resources

- [Jetson AI Lab](https://www.jetson-ai-lab.com)
- [Isaac Lab Evaluation Tasks](https://github.com/isaac-sim/IsaacLabEvalTasks)
- [Live VLM WebUI](https://github.com/nvidia-ai-iot/live-vlm-webui)
- [Vision Search and Summarization (VSS)](https://docs.nvidia.com/vss)

---

## Next Steps

- [ ] Deploy vLLM on Jetson for testing
- [ ] Study TensorRT optimization techniques
- [ ] Explore Isaac Sim for simulation
- [ ] Compare performance across model sizes