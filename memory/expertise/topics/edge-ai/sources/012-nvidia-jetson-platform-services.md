# NVIDIA Jetson Platform Services Architecture

**Source:** NVIDIA Jetson Platform Services Documentation
**Authors:** NVIDIA AI-IOT Team
**Year:** 2025 (v2.0)
**Category:** Edge AI Platform Architecture
**Relevance:** ⭐⭐⭐⭐⭐ (Essential for production Jetson deployments)

---

## Summary

Jetson Platform Services provides a modular, microservices-based architecture for building production-grade Edge AI applications on NVIDIA Jetson devices. It includes AI services (DeepStream, VLM, Zero-Shot Detection) and Foundation Services (storage, networking, monitoring) with REST APIs for integration.

---

## Software Stack Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                          │
│    AI-NVR Workflow | VIA Workflow | Custom Applications     │
├─────────────────────────────────────────────────────────────┤
│                     AI SERVICES                              │
│  DeepStream | VLM Inference | Zero-Shot | GDINO | Analytics │
├─────────────────────────────────────────────────────────────┤
│                  PLATFORM SERVICES                           │
│  VST | Redis | Ingress | Storage | Networking | Monitoring │
├─────────────────────────────────────────────────────────────┤
│                    JETPACK 6.1                               │
│               Orin AGX | NX16 | NX8 | Nano                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Supported Platforms

| Platform | Support Level | Notes |
|----------|--------------|-------|
| **Orin AGX** | Full | All AI Services |
| **Orin NX16** | Full | All AI Services |
| **Orin NX8** | Partial | Most AI Services |
| **Nano 8GB** | Partial | Some AI Services experimental |

---

## AI Services

### DeepStream Perception Service

| Feature | Description |
|---------|-------------|
| **Purpose** | Optimized video analytics pipelines |
| **SDK** | NVIDIA DeepStream SDK |
| **Models** | PeopleNet, YOLO (v8s) |
| **Capability** | Multi-stream object detection and tracking |

### VLM Inference Service

| Feature | Description |
|---------|-------------|
| **Purpose** | Streaming inference with VILA VLM |
| **Model** | VILA-7b |
| **Capability** | Video Q&A, summarization, prompt-based alerts |
| **Platforms** | AGX, NX16, Nano (experimental) |

### Zero-Shot Detection Inference Service

| Feature | Description |
|---------|-------------|
| **Purpose** | Open-world object detection |
| **Model** | Nano OWL (generative AI) |
| **Capability** | Detect large collection of classes without training |
| **Platforms** | AGX, NX16, Nano (experimental) |

### Grounding DINO (GDINO)

| Feature | Description |
|---------|-------------|
| **Purpose** | Open-vocabulary object detection |
| **Model** | Grounding DINO |
| **Capability** | Limitless category detection via generative AI |
| **Platforms** | AGX |

### VLM Video Summarization

| Feature | Description |
|---------|-------------|
| **Purpose** | API-based video summarization |
| **Method** | Natural language interfaces |
| **Platforms** | AGX |

### Analytics AI Service

| Feature | Description |
|---------|-------------|
| **Purpose** | Spatio-temporal analysis |
| **Capabilities** | Line crossing, ROI counting, trajectories, heatmaps |
| **Platforms** | AGX, NX16, NX8, Nano |

---

## Foundation Services

| Service | Purpose |
|---------|---------|
| **VST (Video Storage Toolkit)** | Camera discovery, video storage, hardware-accelerated decode |
| **Redis (Message Bus)** | Shared message bus and storage for microservices |
| **Ingress (API Gateway)** | Standard mechanism to present microservice APIs |
| **Storage** | Provision external storage, allocate to microservices |
| **Networking** | Manage network interfaces for IP cameras |
| **Monitoring** | Visualize system utilization and metrics |
| **Firewall** | Control ingress and egress network traffic |

---

## Reference Workflows

### AI-NVR (AI Network Video Recorder)

- Real-time analytics on multiple streams
- Deep learning + computer vision + streaming analytics
- Traditional NVR capabilities (capture, storage, streaming)
- Containerized deployment via docker-compose

### VIA (Video Insights Agent)

- Real-time video summarization using generative AI
- Chat with video capability
- REST API integration

---

## Deployment Architecture

### Containerized Microservices

```
┌─────────────────────────────────────────────────────────┐
│                    DOCKER COMPOSE                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ AI Service  │  │ AI Service  │  │ AI Service │       │
│  │ Container   │  │ Container   │  │ Container  │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ Foundation  │  │ Foundation  │  │ Foundation  │       │
│  │ Service     │  │ Service     │  │ Service     │       │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
└─────────────────────────────────────────────────────────┘
```

### REST API Integration

- All AI Services expose REST APIs
- Clients interact via HTTP
- API Gateway (Ingress) for external access
- Mobile app demonstrates remote API usage

---

## Disaggregation Philosophy

The software stack can be installed in a disaggregated, piecemeal manner:

1. **Full Stack:** All AI Services + Foundation Services
2. **Custom Inference:** VST for video ingestion + custom AI software
3. **VST Only:** Video storage without AI Services
4. **Analytics Only:** Analytics Service with custom video source

---

## Key Insights

1. **Modular Architecture:** Microservices allow piecemeal deployment
2. **REST APIs:** Standard interface for all AI Services
3. **Containerized:** Docker Compose for packaging and deployment
4. **Foundation Services:** System-level functionality out of the box
5. **Generative AI:** VLM and zero-shot detection on edge

---

## Practical Applications

| Use Case | Services Used |
|----------|---------------|
| **Smart Security** | DeepStream + Analytics + VST |
| **Video Q&A** | VLM Inference Service |
| **Flexible Detection** | Zero-Shot + GDINO |
| **Video Analytics Dashboard** | Analytics AI Service + Monitoring |

---

## Next Steps

- [ ] Deploy AI-NVR reference workflow
- [ ] Test VLM Inference Service
- [ ] Explore custom AI Service integration
- [ ] Study VST for camera discovery