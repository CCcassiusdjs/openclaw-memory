# Docker Swarm vs Kubernetes - 2026

**Fonte:** https://thedecipherist.com/articles/docker_swarm_vs_kubernetes/
**Tipo:** Análise Comparativa
**Lido em:** 2026-03-10
**Status:** completed

---

## TL;DR do Autor

- 10 anos rodando Swarm em produção
- 24 containers, 2 continentes, 2 VPS de $83/ano cada
- Zero crashes, zero data loss, zero security breaches
- Kubernetes resolve problemas do 1%, 99% paga "complexity tax"

---

## Argumentos Principais

### 1. VHS vs Beta
- K8s ganhou não por ser melhor, mas por:
  - Google open-source
  - Cloud providers com managed services
  - Indústria de certificações
  - Recurring revenue

### 2. Docker vs Kubernetes
- Docker: cria containers (88% market share)
- Kubernetes: orquestra containers (92% share)
- Swarm: orquestração nativa do Docker
- K8s roda Docker containers - competição é Swarm vs K8s

### 3. O Problema 80%
Se você já sabe Docker:
- **Swarm:** 80% do conhecimento já existe (compose files, CLI, networking)
- **K8s:** 0% do conhecimento aplica - tudo novo

### 4. Comparação YAML

| Métrica | Compose | Swarm | Kubernetes |
|---------|---------|-------|------------|
| Arquivos | 1 | 1 | 4-6 |
| Linhas YAML | 27 | 42 | 170+ |
| Conceitos novos | 0 | 5 | 25+ |
| Tempo aprendizado | - | 1 tarde | semanas-meses |

---

## Exemplo Prático: Node.js + MongoDB

### Docker Compose (27 linhas)
```yaml
services:
  api:
    image: myapp/api:latest
    ports:
      - "3000:3000"
    environment:
      - MONGO_URI=mongodb://mongo:27017/mydb
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      - mongo
    networks:
      - app-network

  mongo:
    image: mongo:7
    volumes:
      - mongo-data:/data/db
    networks:
      - app-network

volumes:
  mongo-data:

networks:
  app-network:
```

### Docker Swarm (42 linhas)
Adicionar apenas:
```yaml
deploy:
  replicas: 2
  resources:
    limits:
      memory: 128M
  restart_policy:
    condition: on-failure
  update_config:
    parallelism: 1
    delay: 10s
```

5 conceitos novos: deploy, replicas, resources, placement, overlay.

### Kubernetes (170+ linhas, 4-6 arquivos)
Arquivos necessários:
1. api-deployment.yaml
2. api-service.yaml
3. mongo-statefulset.yaml
4. mongo-service.yaml
5. ingress.yaml
6. hpa.yaml (opcional)

25+ conceitos novos: Deployment, StatefulSet, Pod, Service, Ingress, HPA, apiVersion, kind, metadata, spec, selector, matchLabels, livenessProbe, readinessProbe, requests, limits, volumeClaimTemplates, etc.

---

## O que Swarm Faz Bem

### Self-Healing
- Rolling updates automáticos
- Rollback em falha de healthcheck
- Restart policies

### Rolling Deployments
```yaml
update_config:
  parallelism: 2        # Atualiza 2 por vez
  delay: 10s            # Delay entre batches
  failure_action: rollback
```

### Resource Limits
```yaml
resources:
  limits:
    memory: 128M
```

### Placement Constraints
```yaml
placement:
  constraints:
    - node.role == manager
```

---

## O que K8s Tem que Swarm Não Tem

1. **Autoscaling** (HPA) - Swarm não tem nativo
2. **Network Policies** - Namespace isolation
3. **Multi-tenant isolation** - Resource quotas
4. **Custom admission controllers** - Webhooks
5. **Pod scheduling granular** - Affinity/anti-affinity

**Nota do autor:** Script de autoscaling para Swarm pode ser mais inteligente que HPA do K8s.

---

## Custos

| Métrica | Swarm | Kubernetes |
|---------|-------|------------|
| VPS mínimo | 2x $83/ano | 3+ nodes |
| Custo anual | $166 | $1000+ |
| Complexidade | Baixa | Alta |
| Tempo manutenção | Minutos | Horas |

---

## Veredito do Autor

**Use Kubernetes se:**
- Precisa de autoscaling nativo
- Multi-tenant com isolamento
- Network policies granulares
- Time dedicado a DevOps
- Budget para infra complexa

**Use Swarm se:**
- Já conhece Docker
- Menos de 100 containers
- Budget limitado
- Quer simplicidade
- Time pequeno

---

## Minha Conclusão

Artigo interessante mas **enviesado**. O autor tem 10 anos de investimento em Swarm. K8s é complexo mas:
- Comunidade maior
- Mais ferramentas
- Certificações
- Managed services (EKS, GKE, AKS)
- Auto-scaling real

**Veredito:** Swarm é válido para 80% dos casos. K8s é overkill para muitos projetos.

## Próximos Passos
- [ ] Avaliar caso a caso (projeto específico)
- [ ] Considerar K8s se escala > 100 containers
- [ ] Swarm para projetos pequenos/médios