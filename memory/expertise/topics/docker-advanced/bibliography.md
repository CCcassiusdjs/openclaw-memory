# Docker Advanced - Bibliografia

## Status: researching
## Prioridade: 3
## Criado: 2026-03-10
## Atualizado: 2026-03-10

---

## 1. Documentação Oficial Docker

### Networking
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Docker Networking Overview | https://docs.docker.com/engine/network/ | Alta | pending |
| Docker Networks (Compose) | https://docs.docker.com/reference/compose-file/networks/ | Alta | pending |

### Storage
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Docker Storage Overview | https://docs.docker.com/engine/storage/ | Alta | pending |
| Docker Volumes | https://docs.docker.com/engine/storage/volumes/ | Alta | pending |
| Storage Drivers | https://docs.docker.com/engine/storage/drivers/ | Média | pending |
| Select a Storage Driver | https://docs.docker.com/engine/storage/drivers/select-storage-driver/ | Média | pending |
| BTRFS Storage Driver | https://docs.docker.com/engine/storage/drivers/btrfs-driver/ | Baixa | pending |
| ZFS Storage Driver | https://docs.docker.com/engine/storage/drivers/zfs-driver/ | Baixa | pending |

### Security
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Docker Security | https://docs.docker.com/engine/security/ | Alta | pending |
| Docker Hardened Images | https://www.docker.com/products/hardened-images/ | Alta | pending |
| Introducing Hardened Images | https://www.docker.com/blog/introducing-docker-hardened-images/ | Média | pending |
| Hardened Images for Everyone | https://www.docker.com/blog/docker-hardened-images-for-every-developer/ | Média | pending |

### Performance & Resources
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Resource Constraints | https://docs.docker.com/engine/containers/resource_constraints/ | Alta | pending |

### Multi-stage Builds
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Multi-stage Builds (Docs) | https://docs.docker.com/build/building/multi-stage/ | Alta | pending |
| Multi-stage Builds (Concepts) | https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/ | Alta | pending |
| Best Practices | https://docs.docker.com/build/building/best-practices/ | Alta | pending |

### Build & Cache
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Docker Cache | https://docs.docker.com/build/cache/ | Alta | pending |
| Optimize Cache Usage | https://docs.docker.com/build/cache/optimize/ | Alta | pending |
| Cache Storage Backends | https://docs.docker.com/build/cache/backends/ | Média | pending |

### Debugging
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Debug a Container | https://docs.docker.com/dhi/how-to/debug/ | Alta | pending |
| docker debug CLI | https://docs.docker.com/reference/cli/docker/debug/ | Alta | pending |

### Secrets Management
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Docker Swarm Secrets | https://docs.docker.com/engine/swarm/secrets/ | Alta | pending |

### Compose
| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Merge Compose Files | https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/ | Alta | pending |

---

## 2. Segurança e Hardening

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| OWASP Docker Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html | Alta | pending |
| Red Hat - Hardening Docker | https://www.redhat.com/en/blog/hardening-docker-containers-images-and-host-security-toolkit | Alta | pending |
| Bell-Soft - Docker Image Security Best Practices | https://bell-sw.com/blog/docker-image-security-best-practices-for-production/ | Alta | pending |
| SEI CMU - Hardening Docker Images | https://sei.cmu.edu/blog/an-introduction-to-hardening-docker-images/ | Média | pending |
| Medium - Docker Security Hardening | https://medium.com/@smahak59/docker-security-hardening-advanced-techniques-for-production-9a5008261c3e | Média | pending |
| Medium - Enhancing Docker Security | https://medium.com/@anshumaansingh10jan/enhancing-docker-security-comprehensive-best-practices-for-hardening-f7372bcf95bf | Baixa | pending |
| Snyk - Keeping Docker Secrets Secure | https://snyk.io/blog/keeping-docker-secrets-secure/ | Alta | pending |
| GitGuardian - 4 Ways to Store Secrets | https://blog.gitguardian.com/how-to-handle-secrets-in-docker/ | Alta | pending |

---

## 3. Performance e Otimização

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Last9 - Docker Performance Metrics | https://last9.io/blog/docker-container-performance-metrics/ | Alta | pending |
| TowardsDev - Docker Performance Tuning | https://towardsdev.com/docker-performance-tuning-resource-bottleneck-identification-and-cpu-memory-i-o-optimization-cf021ede8b81 | Média | pending |
| LoadForge - Resource Allocation | https://loadforge.com/guides/best-practices-for-docker-container-resource-allocation | Média | pending |
| OneUptime - High-Throughput Optimization | https://oneuptime.com/blog/post/2026-02-08-how-to-optimize-docker-for-high-throughput-applications/view | Média | pending |
| OneUptime - Configure Resource Limits | https://oneuptime.com/blog/post/2026-02-02-docker-resource-limits/view | Média | pending |
| PhoenixNAP - Limit Memory and CPU | https://phoenixnap.com/kb/docker-memory-and-cpu-limit | Média | pending |
| Medium - Chapter 11 Performance Optimization | https://praneethreddybilakanti.medium.com/chapter-11-docker-performance-optimization-b71755efe2c4 | Baixa | pending |

---

## 4. Multi-stage Builds e Dockerfile Patterns

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| iximiuz Labs - Multi-stage Builds | https://labs.iximiuz.com/tutorials/docker-multi-stage-builds | Alta | pending |
| Docker Blog - Advanced Dockerfiles | https://www.docker.com/blog/advanced-dockerfiles-faster-builds-and-smaller-images-using-buildkit-and-multistage-builds/ | Alta | pending |
| Blacksmith - Multi-stage Builds | https://www.blacksmith.sh/blog/understanding-multi-stage-docker-builds | Média | pending |
| Spacelift - Docker Multistage Builds | https://spacelift.io/blog/docker-multistage-builds | Média | pending |
| OneUptime - Multi-stage Builds | https://oneuptime.com/blog/post/2026-02-02-docker-multi-stage-builds/view | Média | pending |
| 2coffee - Layer Caching | https://2coffee.dev/en/articles/understanding-layer-caching-when-building-docker-image-for-better-dockerfile-writing | Alta | pending |
| Netdata - Layer Caching in CI | https://www.netdata.cloud/academy/docker-layer-caching/ | Alta | pending |
| Close.com - Reducing Image Size | https://making.close.com/posts/reduce-docker-image-size/ | Média | pending |
| Bunnyshell - Layer Caching CI/CD | https://www.bunnyshell.com/blog/docker-layer-caching-speed-up-cicd-builds/ | Média | pending |
| Overcast - 13 Docker Caching Strategies | https://overcast.blog/13-docker-chaching-strategies-you-should-know-b6b37e556781 | Média | pending |
| Blacksmith - Faster Builds | https://www.blacksmith.sh/blog/how-to-optimize-dockerfile-faster-docker-builds | Média | pending |
| DevOpsCube - Reduce Image Size | https://devopscube.com/reduce-docker-image-size/ | Média | pending |
| Blacksmith - GitHub Actions Cache | https://www.blacksmith.sh/blog/cache-is-king-a-guide-for-docker-layer-caching-in-github-actions | Baixa | pending |

---

## 5. BuildKit e Buildx

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| GitHub - moby/buildkit | https://github.com/moby/buildkit | Alta | pending |
| SparkFabrik - BuildKit Deep Dive | https://tech.sparkfabrik.com/en/blog/docker-cache-deep-dive/ | Alta | pending |
| DEV - Buildx and BuildKit Caching | https://dev.to/siddhantkcode/accelerating-ci-pipelines-with-docker-buildx-and-buildkit-caching-50g4 | Média | pending |
| AugmentedMind - Advanced BuildKit Caching | https://www.augmentedmind.de/2023/11/19/advanced-buildkit-caching/ | Média | pending |
| Earthly - Speed Up with BuildKit | https://earthly.dev/blog/build-buildkit-cache/ | Média | pending |
| Medium - BuildKit Optimization | https://medium.com/@vasanthancomrads/advanced-docker-buildkit-optimization-techniques-b469552b831e | Baixa | pending |
| GitLab - Docker Layer Caching | https://docs.gitlab.com/ci/docker/docker_layer_caching/ | Média | pending |

---

## 6. Docker Compose Avançado

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| GeeksforGeeks - Docker Compose Override | https://www.geeksforgeeks.org/devops/docker-compose-override/ | Média | pending |
| StackOverflow - Override Files | https://stackoverflow.com/questions/73053037/docker-compose-override-not-taking-additional-yml-into-account | Baixa | pending |
| OneUptime - Override Files | https://oneuptime.com/blog/post/2026-01-25-docker-compose-override-files/view | Média | pending |
| DEV - Compose Override Tips | https://dev.to/aless10/tips-and-tricks-for-docker-compose-leveraging-the-override-feature-4hj0 | Baixa | pending |
| Frank Wiles - Compose Overrides | https://frankwiles.com/til/easy-compose-overrides/ | Baixa | pending |
| LibreChat - Docker Override | https://www.librechat.ai/docs/configuration/docker_override | Baixa | pending |
| Reddit - Environment Configuration | https://www.reddit.com/r/docker/comments/14k1cv8/whats_the_most_elegant_way_to_change_your/ | Baixa | pending |

---

## 7. Orchestration: Swarm vs Kubernetes

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| The Decipherist - Docker Swarm vs Kubernetes 2026 | https://thedecipherist.com/articles/docker_swarm_vs_kubernetes/ | Alta | pending |
| Last9 - Kubernetes vs Docker Swarm | https://last9.io/blog/kubernetes-vs-docker-swarm/ | Média | pending |
| Keitaro - Container Orchestration | https://www.keitaro.com/insights/2024/05/23/container-orchestration-kubernetes-vs-docker-swarm/ | Média | pending |
| ResearchGate - Comparative Analysis | https://www.researchgate.net/publication/387028160_Comparative_Analysis_of_Container_Orchestration_Platforms_Kubernetes_vs_Docker_Swarm | Média | pending |
| blackMORE Ops - 2025 Comparison | https://www.blackmoreops.com/kubernetes-vs-docker-swarm-2025-comparison/ | Média | pending |
| CircleCI - Docker Swarm vs Kubernetes | https://circleci.com/blog/docker-swarm-vs-kubernetes/ | Baixa | pending |
| BMC - Container Orchestration Tools | https://www.bmc.com/blogs/kubernetes-vs-docker-swarm/ | Baixa | pending |
| ThinkSys - Which to Choose 2025 | https://thinksys.com/devops/docker-swarm-vs-kubernetes-comparison/ | Baixa | pending |
| Northflank - Docker Swarm vs Kubernetes | https://northflank.com/blog/docker-swarm-vs-kubernetes | Baixa | pending |
| ImaginaryCloud - We Have a Favourite | https://www.imaginarycloud.com/blog/docker-swarm-vs-kubernetes | Baixa | pending |

---

## 8. Logging, Monitoring e Observability

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Dash0 - Mastering Docker Logs | https://www.dash0.com/guides/mastering-docker-logs | Alta | pending |
| New Relic - Docker Logs Guide | https://newrelic.com/blog/infrastructure-monitoring/docker-logs | Média | pending |
| DEV - Logging and Monitoring | https://dev.to/adityapratapbh1/logging-and-monitoring-in-a-docker-environment-1lha | Baixa | pending |
| Tigera - Container Monitoring | https://www.tigera.io/learn/guides/container-security-best-practices/docker-container-monitoring/ | Média | pending |
| Qovery - Docker Monitoring Tools | https://www.qovery.com/blog/the-best-tool-for-monitoring-your-docker-container | Média | pending |
| Lumigo - Docker Monitoring Tools | https://lumigo.io/container-monitoring/docker-monitoring-9-tools-to-know-metrics-and-best-practices/ | Média | pending |
| Sematext - Container Monitoring Tools | https://sematext.com/blog/docker-container-monitoring/ | Média | pending |
| CleanStart - Container Monitoring | https://www.cleanstart.com/guide/container-monitoring | Baixa | pending |
| Observo - Log Management for Containers | https://www.observo.ai/post/log-management-for-containers | Baixa | pending |

---

## 9. Debugging e Troubleshooting

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| Docker Blog - Debug Like a Superhero | https://www.docker.com/blog/how-to-fix-and-debug-docker-containers-like-a-superhero/ | Alta | pending |
| Lumigo - Docker Debugging Tips | https://lumigo.io/container-monitoring/docker-debugging-common-scenarios-and-7-practical-tips/ | Alta | pending |
| DEV - Mastering Docker Debugging | https://dev.to/docker/mastering-docker-debugging-a-guide-to-docker-desktop-and-cli-tools-for-troubleshooting-containers-5a8d | Média | pending |
| xcubeLabs - Debugging Containers | https://www.xcubelabs.com/blog/product-engineering-blog/debugging-and-troubleshooting-docker-containers/ | Média | pending |
| DEV - Debug Applications in Docker | https://dev.to/addwebsolutionpvtltd/how-to-debug-applications-running-in-docker-containers-4ego | Baixa | pending |
| Martin Heinz - Debug Images Collection | https://martinheinz.dev/blog/104 | Média | pending |

---

## 10. Secrets Management e Vault Integration

| Fonte | URL | Prioridade | Status |
|-------|-----|------------|--------|
| HashiCorp - Securing Container Secrets | https://www.hashicorp.com/en/resources/securing-container-secrets-vault | Alta | pending |
| HashiCorp Developer - Integrate with Docker | https://developer.hashicorp.com/hcp/docs/vault-secrets/retrieve-secrets/docker | Alta | pending |
| OneUptime - How to Use Vault with Docker | https://oneuptime.com/blog/post/2026-02-02-vault-docker/view | Média | pending |
| StackOverflow - Vault with Docker-Compose | https://stackoverflow.com/questions/60552381/how-to-store-and-retrieve-secrets-from-hashicorp-vault-using-docker-compose | Baixa | pending |
| HashiCorp Discuss - Secrets for docker-compose | https://discuss.hashicorp.com/t/secrets-for-docker-compose-services/6265 | Baixa | pending |
| DevOps SE - Passing Secrets to Container | https://devops.stackexchange.com/questions/3902/passing-secrets-to-a-docker-container | Baixa | pending |
| GitHub - docker-compose-secrets | https://github.com/KNIF/docker-compose-secrets | Baixa | pending |

---

## Categorias de Tópicos

### Alta Prioridade (ler primeiro)
1. Documentação oficial de networking, storage, security
2. OWASP Docker Security Cheat Sheet
3. Resource Constraints e Performance
4. Multi-stage Builds
5. BuildKit e Cache Optimization
6. Docker Debug

### Média Prioridade
1. Compose Override patterns
2. Orchestration comparison (Swarm vs K8s)
3. Monitoring e Observability
4. Secrets com Vault

### Baixa Prioridade (referência)
1. Blog posts e artigos secundários
2. Reddit discussions
3. Tutoriais básicos

---

## Próximos Passos

1. [ ] Ler documentação oficial de networking
2. [ ] Ler documentação oficial de storage
3. [ ] Estudar OWASP Docker Security Cheat Sheet
4. [ ] Praticar multi-stage builds
5. [ ] Configurar BuildKit em projeto
6. [ ] Estudar Docker Debug

---

## Notas de Progresso

### 2026-03-10
- Bibliografia inicial criada com 70+ fontes organizadas
- Categorização por prioridade e tópico
- Fontes verificadas e URLs validadas