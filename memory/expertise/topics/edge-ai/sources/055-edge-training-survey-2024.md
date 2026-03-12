# Training Machine Learning Models at the Edge: A Survey (2024)

**Source:** https://arxiv.org/html/2403.02619v3
**Type:** Academic Survey (arXiv)
**Date:** October 2024
**Relevance:** ⭐⭐⭐⭐⭐

## Summary

Comprehensive survey on edge learning - training ML models directly on edge devices. Covers distributed learning (federated, split), on-device fine-tuning (transfer, incremental), model compression, and optimization techniques for resource-constrained environments.

## Key Concepts

### Edge Learning vs Edge Inference

| Aspect | Edge Inference | Edge Learning |
|--------|---------------|---------------|
| **Focus** | Running pre-trained models | Training models on device |
| **Resources** | Lower requirements | Higher requirements |
| **Use Case** | Prediction | Adaptation, customization |
| **Challenge** | Optimization | Memory + compute constraints |

### Why Edge Learning?

**Cloud Computing Limitations:**
- High latency
- Bandwidth overhead
- Privacy/security concerns
- Network dependency

**Edge Learning Benefits:**
- Reduced latency
- Lower bandwidth
- Improved data privacy
- Operational resilience
- Real-time decision-making

### Four Categories of Edge Learning Techniques

1. **Distributed/Collaborative Learning**
   - Federated learning
   - Split learning
   - Multi-device training

2. **Fine-Tuning Methods**
   - Transfer learning
   - Incremental learning
   - On-device adaptation

3. **Model Compression**
   - Quantization
   - Knowledge distillation
   - Pruning

4. **Other Optimization Techniques**
   - Memory optimization
   - Compute scheduling
   - Gradient checkpointing

## Requirements for Edge Learning

| Requirement | Description | Challenge |
|-------------|-------------|-----------|
| **Computational Efficiency** | High performance with minimal compute | Limited CPU/GPU |
| **Memory Efficiency** | Fit within device memory | KB-MB scale |
| **Energy Efficiency** | Minimize power consumption | Battery constraints |
| **Data Efficiency** | Learn from limited data | Non-IID, sparse |
| **Privacy Preservation** | Keep data local | Security requirements |
| **Adaptability** | Handle changing conditions | Concept drift |

## Distributed Learning Methods

### Federated Learning
- Train local models on devices
- Share model updates (not data)
- Server aggregates updates
- Distribute improved model

### Split Learning
- Split model across device and server
- Device processes initial layers
- Server processes remaining layers
- Share intermediate activations

### Challenges
- Heterogeneous devices
- Communication overhead
- Non-IID data distribution
- Stragglers and failures

## On-Device Learning Methods

### Transfer Learning
- Pre-train on cloud
- Fine-tune on edge
- Adapt to specific tasks

### Incremental Learning
- Learn new classes over time
- Avoid catastrophic forgetting
- Continual adaptation

### Knowledge Distillation
- Large teacher model
- Small student model
- Transfer knowledge efficiently

## Model Compression for Training

| Technique | Training Benefit | Trade-off |
|-----------|-----------------|-----------|
| **Quantization** | Reduced memory for gradients | Precision loss |
| **Pruning** | Fewer parameters to update | Sparse updates |
| **Distillation** | Smaller model to train | Requires teacher |
| **Low-rank** | Efficient gradient computation | Expressiveness |

## Metrics for Edge Learning

### Performance Metrics
- Training time
- Memory usage
- Energy consumption
- Communication overhead
- Final accuracy

### Efficiency Metrics
- FLOPS per parameter
- Memory per gradient
- Samples per second
- Energy per sample

### Quality Metrics
- Convergence rate
- Generalization gap
- Privacy guarantees
- Robustness to drift

## Tools and Frameworks

| Framework | Focus | Platform |
|-----------|-------|----------|
| **TensorFlow Lite** | Mobile inference + training | Android, iOS, MCU |
| **PyTorch Mobile** | Mobile ML | Android, iOS |
| **Flower** | Federated learning | Multi-platform |
| **FedML** | Federated learning | Cloud + edge |
| **FATE** | Privacy-preserving ML | Enterprise |

## Applications

### Healthcare
- Privacy-preserving diagnosis
- Personalized treatment
- Wearable monitoring

### Manufacturing
- Predictive maintenance
- Quality control
- Process optimization

### Agriculture
- Crop monitoring
- Pest detection
- Irrigation control

### Space
- Satellite data processing
- On-orbit analysis
- Reduced ground communication

## Key Takeaways

1. **Edge Learning vs Inference** - Training is more resource-intensive than inference
2. **Four Categories** - Distributed, fine-tuning, compression, optimization
3. **Requirements** - Compute, memory, energy, data efficiency all critical
4. **Distributed Learning** - Federated/split learning enable collaboration
5. **On-Device Learning** - Transfer/incremental learning enable adaptation
6. **Compression** - Essential for training on resource-constrained devices

## Related Topics

- Federated learning architectures
- On-device fine-tuning techniques
- Model compression for training
- Edge learning benchmarks
- Privacy-preserving ML