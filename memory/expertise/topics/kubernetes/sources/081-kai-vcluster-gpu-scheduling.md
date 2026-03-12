# GPU Scheduling with NVIDIA KAI and vCluster

**Fonte:** vCluster Blog - https://www.vcluster.com/blog/gpu-scheduling-with-nvidia-kai-and-vcluster
**Data:** 2025
**Tópico:** KAI Scheduler, vCluster, GPU Scheduling Isolation, Multi-tenant
**Status:** Lido

---

## Resumo Executivo

Artigo explorando como combinar NVIDIA KAI Scheduler com vCluster para testar e deployar scheduling de GPU de forma segura e isolada, sem arriscar produção.

---

## O Problema do Scheduling de GPU

### Cenário Atual
- Clusters Kubernetes com recursos GPU preciosos
- Múltiplos times dependendo das GPUs
- Scheduler atual funciona, mas KAI promete melhor alocação

### Desafio
- Testar novo scheduler em produção é arriscado
- "Mudar pneus com carro em movimento"
- Um erro pode parar tudo

### Tipos de Workload GPU

| Workload | Exemplo | Uso de GPU |
|----------|---------|------------|
| **Model Training** | Fine-tuning LLMs, Deep Learning | 100% por horas/dias |
| **Stable Diffusion** | Image generation | ~50% GPU |
| **LLM Inference** | ChatGPT API, Claude API | 25-75% dependendo do modelo |
| **Video Processing** | Transcoding, streaming | Variável 20-80% |
| **CUDA Development** | Jupyter notebooks, testing | Frequentemente < 20% |
| **Batch Processing** | Scientific computing | Picos para 100% |

### Observação
A maioria dos workloads não usa 100% da GPU o tempo todo. Mas Kubernetes tradicional trata GPUs como recursos indivisíveis.

---

## NVIDIA KAI Scheduler

### O que é
- Open-sourced em Janeiro 2025
- Scheduler Kubernetes para otimização de GPU workloads
- Enterprise-grade GPU management

### Capacidades-Chave

| Feature | Benefício |
|---------|-----------|
| **Fractional GPU allocation** | Compartilhar GPU entre workloads |
| **Queue-based scheduling** | Gestão hierárquica de recursos |
| **Topology awareness** | Otimização para hardware layout |
| **Fair sharing** | Prevenir monopolização de recursos |

### Como Funciona
- KAI garante máxima utilização sem colisões
- Alocação fracionária permite uso eficiente
- Queue-based permite multi-tenancy

---

## Problemas de Upgrade de Scheduler

### Desafios Atuais
- Scheduler único controla todo cluster
- Mudanças afetam todos workloads
- Sem isolamento entre times
- Rollback demora horas

### Modos de Falha

| Modo de Falha | Impacto | Tempo de Recuperação | Custo |
|---------------|---------|---------------------|-------|
| **Scheduler bug** | Pods pending | 2-4 horas | Alto |
| **CRD conflicts** | Namespace corruption | 6+ horas | Crítico |
| **Version mismatch** | Random pod failures | 1-2 dias | Muito Alto |
| **Resource leak** | GPU exhaustion | 4-8 horas | Crítico |

### Custo de Downtime
- Enterprise downtime: $100k-1M+ por hora
- Testar em produção é arriscado

---

## vCluster para Teste Isolado

### O que é vCluster
- Kubernetes virtual rodando dentro de namespace do cluster existente
- Não é novo cluster EKS/GKE
- Cluster virtual dentro da infra existente

### Componentes
- **API Server**: Handle Kubernetes API calls independentemente
- **Syncer**: Sincronização bidirecional com host cluster
- **SQLite/etcd**: State isolation completo
- **Virtual Scheduler**: Decisões de scheduling independentes

### Arquitetura
```
┌─────────────────────────────────────────────────┐
│            Host Kubernetes Cluster               │
│  ┌───────────────────────────────────────────┐  │
│  │ Namespace: team-a                         │  │
│  │ ┌─────────────────────────────────────┐   │  │
│  │ │ vCluster                            │   │  │
│  │ │ ┌──────────────┐ ┌──────────────┐   │   │  │
│  │ │ │ Virtual API  │ │ Syncer       │   │   │  │
│  │ │ │ Server       │ │              │   │   │  │
│  │ │ └──────────────┘ └──────────────┘   │   │  │
│  │ │ ┌──────────────┐ ┌──────────────┐   │   │  │
│  │ │ │ KAI Scheduler│ │ SQLite/etcd  │   │   │  │
│  │ │ └──────────────┘ └──────────────┘   │   │  │
│  │ └─────────────────────────────────────┘   │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │ GPU Nodes (shared physical resources)     │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## Workflow de Teste Isolado

### Passos
1. Criar vCluster com virtual scheduler enabled
2. Instalar KAI Scheduler dentro do vCluster
3. Deploy test workloads com fractional GPU requests
4. Observar comportamento em isolamento completo
5. Se falhar: deletar vCluster em 40 segundos

### Benefícios

| Benefício | Tempo | Risco |
|-----------|-------|-------|
| **Testar scheduler upgrades** | 4h → 5min | 100% → 0% |
| **Rollback bad changes** | 2h → 30s | Crítico → Zero |
| **A/B test versions** | Impossible → Easy | Alto → Zero |
| **Per-team schedulers** | Days → Minutes | Complexo → Simple |
| **GPU sharing validation** | Weeks → Hours | Alto → Zero |

---

## Multi-Team Scheduler Support

### Cenário
- ML team: quer testar KAI v0.9.3
- Research team: precisa da versão estável v0.7.11
- Com scheduler único: times precisam coordenar e comprometer

### Solução com vCluster
- Cada team opera seu próprio virtual cluster
- Versões diferentes de KAI em cada vCluster
- Autonomia completa sem interferência

### Arquitetura Multi-Team
```
┌─────────────────────────────────────────────────┐
│            Host Cluster                          │
│  ┌────────────────┐ ┌────────────────┐          │
│  │ vCluster ML    │ │ vCluster       │          │
│  │ KAI v0.9.3     │ │ Research       │          │
│  │                │ │ KAI v0.7.11     │          │
│  └────────────────┘ └────────────────┘          │
│                                                  │
│  Impacto no Host: NONE                           │
│  Isolamento: COMPLETO                            │
└─────────────────────────────────────────────────┘
```

---

## Syncer: Conectando Virtual e Host

### Funções
- Sincroniza recursos entre virtual e host cluster
- Traduz recursos virtuais para host resources
- Gerencia lifecycle de recursos
- Garante boundaries de isolamento

### Comportamento
- Workloads GPU scheduleados pelo KAI dentro do vCluster
- Rodam em GPU nodes físicos do host cluster
- Decisões de scheduling isoladas no vCluster

---

## Benefícios Combinados

### Tempo
- Setup to first test: 5min (vs 4+ hours)
- Version switching: 30s (vs 2+ hours)
- Team onboarding: Minutes (vs days)

### Risco
- Blast radius: Namespace único (vs cluster inteiro)
- Rollback complexity: Delete command (vs procedimentos complexos)
- Testing freedom: Complete (vs severely limited)

---

## Casos de Uso

### 1. Validar KAI Features
- Fractional GPU allocation
- Queue-based scheduling
- Topology awareness

### 2. A/B Testing
- Comparar versões do scheduler
- Medir performance

### 3. Team Autonomy
- Times com necessidades diferentes
- Isolamento de configurações

---

## Recursos Técnicos

### Setup Guide
- [Complete Setup Guide](https://vclusterlabs-experiments.github.io/vcluster-kai-demo/)
- Configuração de vCluster com virtual scheduler
- Instalação do KAI Scheduler
- Sample GPU workloads com fractional allocation
- Multi-team setup examples
- Troubleshooting tips

---

## Insights para Kubernetes

1. **vCluster isola scheduler**: Testa KAI sem risco ao production
2. **Rollback instantâneo**: Delete vCluster em segundos
3. **Multi-versão**: Times podem usar versões diferentes
4. **GPU sharing seguro**: Valida fractional allocation isoladamente
5. **Zero blast radius**: Erros ficam no namespace/vCluster

---

## Palavras-Chave
`kai-scheduler` `vcluster` `gpu-scheduling` `isolation` `multi-tenant` `nvidia` `testing`