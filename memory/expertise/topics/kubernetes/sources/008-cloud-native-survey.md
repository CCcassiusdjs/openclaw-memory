# Cloud-Native Computing: A Survey from the Perspective of Services

**Source:** arxiv.org/html/2306.14402v1
**Type:** Survey Paper
**Priority:** Medium
**Date:** 2023

---

## Summary

Este survey apresenta um roadmap de pesquisa para cloud-native computing do ponto de vista de serviços. Os autores decompõem o ciclo de vida de aplicações cloud-native em quatro estados: building, orchestration, operation e maintenance.

## Key Concepts

### Cloud-Native Definition (CNCF)
- Coleção de tecnologias que quebram aplicações em microserviços
- Empacotamento em containers leves
- Deploy e orquestração em clusters de servidores

### Core Characteristics
1. **Containerização** - Isolamento de recursos via Linux kernel namespaces/cgroups
2. **Microserviços** - Arquitetura desacoplada com comunicação via REST/messaging
3. **Orquestração** - Kubernetes como padrão de fato (origem: Google Borg)
4. **DevOps/CI/CD** - Entrega contínua com automação

### Life-Cycle States
- **Building**: Desenvolvimento de microserviços, containerização
- **Orchestration**: Kubernetes, scheduling, scaling
- **Operation**: Monitoramento, logging, service mesh
- **Maintenance**: Updates, fault tolerance, security

## Architecture Insights

### Hierarchical Infrastructure
- Clusters: nodes conectados via LAN
- OS-level virtualization (VMs/containers)
- Cluster managers: Kubernetes, Mesos, Docker Swarm, YARN

### Kubernetes Ecosystem
- **Helm**: Package management
- **Istio**: Service mesh com Envoy proxy
- **Prometheus/Grafana**: Monitoring
- **Kibana**: Logging

## Research Domains

### Foundation Layer
- Resource virtualization
- Elastic provisioning
- Security functions
- Performance optimization
- Efficiency tools

### Performance Metrics (3 levels)
1. **Infrastructure**: CPU, memory, network throughput
2. **Platform**: Scheduling latency, throughput
3. **Software**: Response time, availability

## Key Findings

- Cloud-native é a abordagem dominante para aplicações web modernas
- Kubernetes é o orquestrador padrão (de facto standard)
- Service mesh (Istio) é essencial para microserviços complexos
- Monitoramento e observabilidade são críticos

## Connections to Other Topics

- **Microservices Architecture**: Padrão arquitetural base
- **Service Mesh**: Istio para traffic management
- **Container Orchestration**: Kubernetes como core
- **DevOps/CI/CD**: Automação de deploy

## Quotes

> "Cloud-native computing, as the most influential development principle for web applications, has already attracted increasingly more attention in both industry and academia."

> "Kubernetes, originated from Google's Borg cluster manager, is the most popular open-source container orchestration software."

## Personal Notes

Este survey é importante para entender o contexto macro de cloud-native. Fornece uma taxonomia clara dos componentes e suas relações. A visão de ciclo de vida (building → orchestration → operate → maintenance) ajuda a organizar o aprendizado.