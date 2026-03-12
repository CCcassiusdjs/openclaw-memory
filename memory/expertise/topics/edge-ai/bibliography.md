# Edge AI & Edge Computing - Bibliography

**Topic ID:** edge-ai
**Priority:** 2
**Status:** researching
**Created:** 2026-03-12
**Last Updated:** 2026-03-12

---

## Overview

Edge AI refers to the deployment of artificial intelligence models directly on edge devices (smartphones, IoT devices, embedded systems, edge servers) rather than relying solely on cloud computing. This enables real-time processing, reduced latency, enhanced privacy, and lower bandwidth costs.

---

## Key Concepts

1. **Edge AI vs. Cloud AI** - Local inference vs. centralized processing
2. **TinyML** - Running ML on ultra-low-power microcontrollers
3. **Model Optimization** - Quantization, pruning, knowledge distillation
4. **Hardware Accelerators** - NPU, TPU, FPGA, Edge TPU
5. **Federated Learning** - Privacy-preserving distributed training
6. **Edge Inference Frameworks** - TensorFlow Lite, ONNX Runtime, OpenVINO

---

## Academic Papers & Surveys

### Comprehensive Surveys

| # | Title | Authors | Year | Source | Relevance |
|---|-------|---------|------|--------|-----------|
| 1 | [Edge Computing with Artificial Intelligence: A Machine Learning Perspective](https://dl.acm.org/doi/pdf/10.1145/3555802) | Hua et al. | 2023 | ACM Computing Surveys | ⭐⭐⭐⭐⭐ |
| 2 | [Deep Learning With Edge Computing: A Review](https://www.cs.ucr.edu/~jiasi/pub/deep_edge_review.pdf) | Chen & Ran | 2019 | Proceedings of the IEEE | ⭐⭐⭐⭐⭐ |
| 3 | [Optimizing Edge AI: A Comprehensive Survey on Data, Model, and System Strategies](https://arxiv.org/html/2501.03265v1/) | - | 2024 | arXiv | ⭐⭐⭐⭐⭐ |
| 4 | [Edge AI in Practice: A Survey and Deployment Framework for Neural Networks on Embedded Systems](https://www.mdpi.com/2079-9292/14/24/4877) | - | 2025 | MDPI Electronics | ⭐⭐⭐⭐⭐ |
| 5 | [Artificial Intelligence and Machine Learning for EDGE Computing](https://www.sciencedirect.com/book/9780128240540/artificial-intelligence-and-machine-learning-for-edge-computing) | Pandey (Ed.) | 2021 | Elsevier Book | ⭐⭐⭐⭐ |
| 6 | [A Review on TinyML: State-of-the-art and Prospects](https://www.sciencedirect.com/science/article/pii/S1319157821003335) | - | 2021 | ScienceDirect | ⭐⭐⭐⭐ |

### Model Optimization & Compression

| # | Title | Authors | Year | Source | Relevance |
|---|-------|---------|------|--------|-----------|
| 7 | [Advanced Quantization and Pruning Methods for Optimizing Deep Learning Models on Edge Devices](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5713386) | Godwin | 2025 | SSRN | ⭐⭐⭐⭐⭐ |
| 8 | [PQK: Model Compression via Pruning, Quantization, and Knowledge Distillation](https://arxiv.org/abs/2106.14681) | - | 2021 | arXiv | ⭐⭐⭐⭐⭐ |
| 9 | [Edge AI: Evaluation of Model Compression Techniques for CNNs](https://arxiv.org/html/2409.02134v1) | - | 2024 | arXiv | ⭐⭐⭐⭐ |
| 10 | [Constrained Edge AI Deployment: Fine-Tuning vs. Distillation for LLM Compression](https://arxiv.org/html/2505.18166v1) | - | 2025 | arXiv | ⭐⭐⭐⭐ |
| 11 | [Exploring Knowledge Distillation for Model Compression in Edge Environments](https://link.springer.com/chapter/10.1007/978-3-031-96196-0_12) | Springer | 2024 | Springer | ⭐⭐⭐⭐ |

### Federated Learning for Edge

| # | Title | Authors | Year | Source | Relevance |
|---|-------|---------|------|--------|-----------|
| 12 | [A Review on Federated Learning Architectures for Privacy-Preserving AI](https://www.mdpi.com/2079-9292/14/13/2512) | - | 2025 | MDPI Electronics | ⭐⭐⭐⭐⭐ |
| 13 | [Survey: Federated Learning Data Security and Privacy-Preserving in Edge-IoT](https://link.springer.com/article/10.1007/s10462-024-10774-7) | - | 2024 | Springer | ⭐⭐⭐⭐⭐ |
| 14 | [Towards Robust and Privacy-Preserving Federated Learning in Edge Computing](https://www.sciencedirect.com/science/article/abs/pii/S1389128624001531) | - | 2024 | ScienceDirect | ⭐⭐⭐⭐ |
| 15 | [Edge Computing and Federated Learning for Privacy-Preserving IoT Analytics](https://link.springer.com/article/10.1186/s13638-025-02545-x) | - | 2025 | Springer | ⭐⭐⭐⭐ |
| 16 | [Federated Learning for Privacy-Preserving Edge AI](https://www.researchgate.net/publication/392040839_Federated_Learning_for_Privacy-Preserving_Edge_AI) | - | 2025 | ResearchGate | ⭐⭐⭐⭐ |

### TinyML

| # | Title | Authors | Year | Source | Relevance |
|---|-------|---------|------|--------|-----------|
| 17 | [MTR200519 MITRE Technical Report: TinyML for Ubiquitous Edge AI](https://arxiv.org/pdf/2102.01255) | - | 2021 | arXiv/MITRE | ⭐⭐⭐⭐⭐ |
| 18 | [TinyML: Enabling of Inference Deep Learning Models on Ultra-Low-Power IoT Edge Devices](https://www.mdpi.com/2072-666X/13/6/851) | - | 2022 | MDPI Micromachines | ⭐⭐⭐⭐ |
| 19 | [Deploying TinyML for Energy-Efficient Object Detection](https://www.nature.com/articles/s41598-025-27818-9) | - | 2025 | Nature Scientific Reports | ⭐⭐⭐⭐ |

---

## Official Documentation & Frameworks

### TensorFlow Lite / LiteRT

| # | Resource | Description | URL |
|---|----------|-------------|-----|
| 20 | Google AI Edge - LiteRT | Official TensorFlow Lite (now LiteRT) documentation | https://ai.google.dev/edge/litert |
| 21 | Model Optimization | Quantization and pruning for LiteRT models | https://ai.google.dev/edge/litert/conversion/tensorflow/quantization/model_optimization |
| 22 | Edge TPU Guide | Running models on Google Coral Edge TPU | https://coral.ai/docs/ |

### ONNX Runtime

| # | Resource | Description | URL |
|---|----------|-------------|-----|
| 23 | ONNX Runtime Docs | Official documentation for cross-platform inference | https://onnxruntime.ai/docs/ |
| 24 | Deploy on IoT/Edge | Edge deployment tutorial | https://onnxruntime.ai/docs/tutorials/iot-edge/ |
| 25 | ONNX Runtime Inference | Main inference page | https://onnxruntime.ai/inference |
| 26 | Mobile Training | On-device training capabilities | https://onnxruntime.ai/docs/get-started/training-on-device.html |

### Intel OpenVINO

| # | Resource | Description | URL |
|---|----------|-------------|-----|
| 27 | OpenVINO Toolkit | Intel's edge AI optimization toolkit | https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/overview.html |
| 28 | OpenVINO GitHub | Open source repository | https://github.com/openvinotoolkit/openvino |
| 29 | OpenVINO for AI PC | Deployment on Intel AI PCs | https://www.intel.com/content/www/us/en/developer/tools/openvino-toolkit/ai-pc.html |
| 30 | Hugging Face Integration | Deploy HF models with OpenVINO | https://huggingface.co/blog/deploy-with-openvino |

### NVIDIA Jetson

| # | Resource | Description | URL |
|---|----------|-------------|-----|
| 31 | NVIDIA Jetson Platform | Official Jetson documentation | https://developer.nvidia.com/embedded-computing |
| 32 | Getting Started with Edge AI on Jetson | LLMs, VLMs, and Foundation Models for Robotics | https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics |
| 33 | Jetson Platform Services | Modular microservices architecture | https://docs.nvidia.com/jetson/jps/moj-overview.html |
| 34 | Edge Impulse Jetson Docs | Deployment guide for Jetson | https://docs.edgeimpulse.com/docs/edge-ai-hardware/gpu/nvidia-jetson |

### Edge Impulse

| # | Resource | Description | URL |
|---|----------|-------------|-----|
| 35 | Edge Impulse Platform | End-to-end edge ML development | https://edgeimpulse.com/ |
| 36 | TinyML Frameworks Guide | Top frameworks and hardware | https://www.dfrobot.com/blog-13921.html |

---

## Hardware Accelerators

### NPU vs TPU vs GPU vs FPGA

| # | Resource | Topic | URL |
|---|----------|-------|-----|
| 37 | [NPU vs TPU: Key Differences](https://www.wevolver.com/article/npu-vs-tpu) | Comparison of AI accelerators | Wevolver |
| 38 | [Choosing the Right AI Accelerator](https://www.gateworks.com/choosing-the-right-ai-accelerator-npu-or-tpu-for-edge-and-cloud-applications/) | Gateworks guide | Gateworks |
| 39 | [CPU vs GPU vs TPU vs NPU: AI Hardware Architecture Guide 2025](https://www.thepurplestruct.com/blog/cpu-vs-gpu-vs-tpu-vs-npu-ai-hardware-architecture-guide-2025) | Comprehensive comparison | The Purplestruct |
| 40 | [NPU vs GPU for Edge AI](https://www.onlogic.com/blog/npus-vs-gpus-for-edge-ai/) | OnLogic guide | OnLogic |
| 41 | [AI-Specific Chips: TPUs, NPUs, and FPGAs Explained](https://blog.deyvos.com/posts/ai-specific-chips-tpus-npus-fpgas-explained/) | Deyvos Labs | Deyvos Labs |
| 42 | [Top 15 Edge AI Chip Makers](https://research.aimultiple.com/edge-ai-chips/) | Industry overview | Aimultiple |
| 43 | [Top 15 Hardware Accelerators for AI and Edge Computing](https://www.wonderfulpcb.com/blog/top-15-hardware-accelerators-ai-edge-computing/) | Hardware overview | Wonderful PCB |

---

## Books & Comprehensive Resources

| # | Title | Authors | Year | Publisher | Access |
|---|-------|---------|------|-----------|--------|
| 44 | Fog and Edge Computing: Principles and Paradigms | Buyya & Srirama | 2019 | Wiley | [PDF](https://soclibrary.futa.edu.ng/books/Fog%20and%20edge%20computing%20principles%20and%20paradigms%20by%20Buyya,%20Rajkumar%20Srirama,%20Satish%20Narayana%20(z-lib.org).pdf) |
| 45 | Edge Computing: Fundamentals, Advances and Applications | Kumari et al. | 2022 | CRC Press | [PDF](https://lib.zu.edu.pk/ebookdata/Engineering/Electrical%20Engineering%20Technology/Edge%20Computing_%20Fundamentals,%20Advances%20and%20Applications%20(Advances%20in%20Industry%204.0%20and%20Machine%20Learning)-CRC%20Press%20(2022)%20by%20K.%20Anitha%20Kumari..pdf) |
| 46 | Deep Learning on Edge Computing Devices | ScienceDirect | 2022 | Elsevier | [Link](https://www.sciencedirect.com/book/9780323857833/deep-learning-on-edge-computing-devices) |
| 47 | Machine Learning for Edge Computing: Frameworks, Patterns and Best Practices | Singh, Kukreja, Gandomani | 2023 | Routledge | [Link](https://www.routledge.com/Machine-Learning-for-Edge-Computing-Frameworks-Patterns-and-Best-Practices/Singh-Kukreja-Gandomani/p/book/9780367694326) |

---

## Tutorials & Courses

| # | Resource | Provider | Description | URL |
|---|----------|----------|-------------|-----|
| 48 | Edge AI for Beginners | Microsoft | Comprehensive course covering fundamentals, models, inference, optimization | [GitHub](https://github.com/microsoft/edgeai-for-beginners) |
| 49 | How to Build, Optimize, and Deploy AI Models at the Edge | Wevolver | Practical deployment guide | [Wevolver](https://www.wevolver.com/article/how-to-build-optimize-and-deploy-ai-models-at-the-edge) |
| 50 | Edge AI Inference Guide | Mirantis | Enterprise edge inference use cases | [Mirantis](https://www.mirantis.com/blog/ai-focused-edge-inference-use-cases-and-guide-for-enterprise/) |
| 51 | Deploying AI Models at the Edge: Best Practices | Promwad | Challenges and best practices | [Promwad](https://promwad.com/news/edge-ai-model-deployment) |
| 52 | Azure IoT Edge ML Inference | Microsoft | Azure-specific guide | [Microsoft Learn](https://learn.microsoft.com/en-us/azure/architecture/guide/iot/machine-learning-inference-iot-edge) |
| 53 | Edge AI Best Practices | DAC.digital | 5 best practices for deployment | [DAC.digital](https://dac.digital/edge-ai-best-practices/) |

---

## Industry Applications

| # | Domain | Key Applications | Source |
|---|--------|-----------------|--------|
| 54 | Smart Manufacturing | Predictive maintenance, quality inspection, industrial automation | [MDPI](https://www.mdpi.com/2624-6511/8/6/211) |
| 55 | Autonomous Vehicles | Real-time perception, sensor fusion, decision making | [ASUS IoT](https://iot.asus.com/resources/casestudies/autonomous-vehicle-pe-8000g/) |
| 56 | Smart Healthcare | Patient monitoring, diagnostics, medical imaging | [Advantech](https://www.advantech.com/en-us/resources/industry-focus/edge-ai) |
| 57 | Smart Cities | Traffic management, surveillance, public safety | [MDPI Smart Cities](https://www.mdpi.com/2624-6511/8/6/211) |
| 58 | Industrial IoT | Machine monitoring, environmental sensors, production lines | [Syslogic](https://www.syslogic.com/blog/edge-intelligence-ai-powered-data-processing-directly-at-the-edge) |
| 59 | Smart Agriculture | Precision farming, crop monitoring, livestock tracking | [Syslogic](https://www.syslogic.com/blog/edge-intelligence-ai-powered-data-processing-directly-at-the-edge) |

---

## Model Optimization Techniques

### Quantization

| # | Resource | Description |
|---|----------|-------------|
| 60 | [Google AI Edge - Quantization](https://ai.google.dev/edge/litert/conversion/tensorflow/quantization/model_optimization) | Official quantization documentation |
| 61 | [Pruning and Quantization in Computer Vision - Ultralytics](https://www.ultralytics.com/blog/pruning-and-quantization-in-computer-vision-a-quick-guide) | YOLO-specific optimization guide |
| 62 | [How Quantization and Pruning Work for Edge AI](https://medium.com/@thekzgroupllc/how-quantization-and-pruning-actually-work-and-why-they-matter-for-edge-ai-8ee7a239466f) | Medium article explaining concepts |
| 63 | [Qualcomm: Optimizing AI Model for the Edge](https://www.qualcomm.com/developer/blog/2025/06/optimizing-your-ai-model-for-the-edge) | 5 techniques for optimization |

### Knowledge Distillation

| # | Resource | Description |
|---|----------|-------------|
| 64 | [Model Compression Techniques Guide 2025](https://createbytes.com/insights/model-compression-techniques-guide) | Comprehensive guide |
| 65 | [Model Compression: Quantization, Pruning & Distillation](https://medium.com/@amitkharche/model-compression-techniques-quantization-pruning-distillation-for-real-world-deployment-229f57e2c807) | Medium tutorial |
| 66 | [Model Compression Techniques for Edge AI](https://moschip.com/blog/model-compression-techniques-for-edge-ai/) | Moschip guide |

---

## Frameworks Comparison

| Framework | Best For | Hardware Support | Key Features |
|-----------|----------|------------------|--------------|
| **TensorFlow Lite (LiteRT)** | Mobile/Embedded | ARM, Edge TPU, Mobile GPUs | Post-training quantization, delegate system |
| **ONNX Runtime** | Cross-platform | CPU, GPU, NPU, FPGA | Universal format, graph optimizations |
| **OpenVINO** | Intel hardware | Intel CPU, GPU, NPU, VPU | Model optimizer, auto-device selection |
| **PyTorch Mobile** | Mobile deployment | Android, iOS | Eager execution, TorchScript |
| **TensorRT** | NVIDIA GPUs | NVIDIA GPUs, Jetson | FP16/INT8 optimization, layer fusion |
| **Core ML** | Apple devices | iPhone, iPad, Mac, Apple Watch | Neural Engine acceleration |

---

## Source Priority for Reading

### Phase 1: Foundations (High Priority)
1. Edge Computing with AI: A ML Perspective (ACM Survey) - #1
2. Deep Learning With Edge Computing: A Review - #2
3. Edge AI for Beginners (Microsoft Course) - #48
4. Google AI Edge documentation - #20-22
5. ONNX Runtime documentation - #23-26

### Phase 2: Model Optimization (Medium Priority)
1. Advanced Quantization and Pruning Methods - #7
2. PQK: Model Compression - #8
3. Optimizing Edge AI: Comprehensive Survey - #3
4. Qualcomm: Optimizing AI Model for the Edge - #63

### Phase 3: Hardware & Deployment (Medium Priority)
1. NPU vs TPU Guide - #37
2. NVIDIA Jetson documentation - #31-34
3. OpenVINO Toolkit - #27-30
4. Top 15 Edge AI Chip Makers - #42

### Phase 4: Federated Learning & Privacy (Lower Priority)
1. Federated Learning Architectures Survey - #12
2. Privacy-Preserving Federated Learning - #13-16

### Phase 5: Applications (Contextual)
1. Smart Manufacturing/Cities - #54-59
2. Autonomous Vehicles - #55

---

## Notes

- **Total Sources Catalogued:** 66+
- **Primary Sources (Must Read):** 15
- **Documentation Sources:** 15
- **Hardware/Industry Sources:** 20+
- **Book-Length Resources:** 4

---

## Next Steps

1. Read ACM Survey "Edge Computing with AI: A ML Perspective"
2. Complete Microsoft Edge AI for Beginners course
3. Study TensorFlow Lite/LiteRT documentation
4. Review model optimization techniques (quantization, pruning)
5. Explore ONNX Runtime and OpenVINO for cross-platform deployment