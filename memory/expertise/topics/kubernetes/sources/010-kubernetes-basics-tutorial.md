# Learn Kubernetes Basics - Official Tutorial

**Source:** kubernetes.io/docs/tutorials/kubernetes-basics/
**Type:** Official Documentation
**Priority:** High
**Date:** 2026

---

## Summary

Tutorial oficial do Kubernetes que cobre os fundamentos do sistema de orquestração de containers. Focado em iniciantes, ensina deploy, scaling e debugging de aplicações containerizadas.

## Learning Objectives

1. Deploy a containerized application on a cluster
2. Scale the deployment
3. Update the containerized application with a new software version
4. Debug the containerized application

## What Kubernetes Provides

### Core Value Proposition
- **High Availability**: Applications available 24/7
- **Continuous Deployment**: Multiple deploys per day without downtime
- **Container Orchestration**: Automatic scheduling, scaling, self-healing

### Production Features
- Declarative configuration
- Automation of deployment, scaling, and management
- Built on Google's 15 years of production experience

## Tutorial Structure

### Key Modules
1. **Create Cluster** - Using Minikube
2. **Deploy App** - Using kubectl
3. **Explore** - Pods, nodes, services
4. **Scale** - Replicas, deployments
5. **Update** - Rolling updates, rollbacks

## Core Concepts Introduced

### Cluster
- Set of machines (nodes) running containerized applications
- Managed by Kubernetes control plane

### Deployment
- Declarative way to manage application state
- Handles replica creation and updates

### Service
- Abstraction for network access to pods
- Load balancing built-in

## Key Takeaways

- Kubernetes is designed for production workloads
- Declarative configuration is the core paradigm
- Automation handles most operational tasks
- Built-in self-healing capabilities

## Personal Notes

Este é o ponto de entrada ideal para iniciantes. A abordagem hands-on com Minikube permite experimentação segura. Os conceitos fundamentais são apresentados de forma progressiva e prática.