# docker service update - Docker CLI Reference

**URL:** https://docs.docker.com/reference/cli/docker/service/update/
**Lido em:** 2026-03-11
**Categoria:** Orchestration
**Prioridade:** Alta

---

## Resumo

Referência completa do comando `docker service update` para atualização de serviços Swarm.

---

## Descrição

Atualiza um serviço com parâmetros especificados. Parâmetros são os mesmos de `docker service create`.

### Comportamento:
- Tasks só são recriadas se mudança exige
- `--force` força recriação mesmo sem mudanças
- Útil para rolling restart

---

## Principais Opções

### Atualização de Imagem

```bash
# Atualizar imagem
docker service update --image nginx:latest myservice

# Forçar recriação
docker service update --force myservice
```

### Escalonamento

```bash
# Alterar número de replicas
docker service update --replicas 5 myservice
```

### Resources

```bash
# Limites
docker service update --limit-cpu 2 --limit-memory 512M myservice

# Reservas
docker service update --reserve-cpu 1 --reserve-memory 256M myservice
```

### Variáveis de Ambiente

```bash
# Adicionar
docker service update --env-add MYVAR=value myservice

# Remover
docker service update --env-rm MYVAR myservice
```

### Ports

```bash
# Adicionar porta
docker service update --publish-add published=8080,target=80 myservice

# Remover porta
docker service update --publish-rm 80 myservice
```

### Networks

```bash
# Adicionar network
docker service update --network-add my-network myservice

# Remover network
docker service update --network-rm my-network myservice
```

### Mounts

```bash
# Adicionar mount
docker service update --mount-add type=volume,src=data,dst=/data myservice

# Remover mount
docker service update --mount-rm /data myservice
```

### Secrets

```bash
# Adicionar secret
docker service update --secret-add source=ssh-2,target=/ssh myservice

# Remover secret
docker service update --secret-rm ssh-1 myservice
```

### Placement

```bash
# Adicionar constraint
docker service update --constraint-add node.labels.region==east myservice

# Remover constraint
docker service update --constraint-rm node.labels.region==east myservice

# Adicionar preference
docker service update --placement-pref-add 'spread=node.labels.datacenter' myservice
```

---

## Rolling Update Parameters

### Flags de Update:

| Flag | Descrição |
|------|-----------|
| `--update-delay` | Delay entre updates |
| `--update-parallelism` | Tasks simultâneas (default: 1) |
| `--update-failure-action` | pause/continue/rollback |
| `--update-max-failure-ratio` | Taxa de falha tolerada |
| `--update-monitor` | Tempo de monitoramento (default: 30s) |
| `--update-order` | start-first/stop-first |

---

## Rollback

### Manual:

```bash
# Voltar para versão anterior
docker service update --rollback myservice

# Rollback instantâneo
docker service update --rollback --update-delay 0s myservice
```

### Rollback Parameters:

| Flag | Default | Descrição |
|------|---------|-----------|
| `--rollback-delay` | 0s | Delay entre rollbacks |
| `--rollback-parallelism` | 1 | Tasks em paralelo |
| `--rollback-failure-action` | pause | Ação em falha |
| `--rollback-max-failure-ratio` | 0 | Taxa tolerada |
| `--rollback-monitor` | 5s | Tempo de monitoramento |

### Auto-Rollback:

```bash
# Configurar auto-rollback em falha
docker service create \
  --update-failure-action=rollback \
  --update-max-failure-ratio=0.3 \
  myservice
```

---

## Health Check

```bash
docker service update \
  --health-cmd "curl -f http://localhost/health || exit 1" \
  --health-interval 30s \
  --health-timeout 5s \
  --health-retries 3 \
  myservice
```

---

## Restart Policy

```bash
docker service update \
  --restart-condition on-failure \
  --restart-delay 10s \
  --restart-max-attempts 5 \
  --restart-window 1m \
  myservice
```

---

## Logging

```bash
docker service update \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  myservice
```

---

## Examples

### Rolling Restart

```bash
# Restart gradual (1 task por vez, 30s delay)
docker service update --force --update-parallelism 1 --update-delay 30s myservice
```

### Add Mounts and Ports

```bash
docker service update \
  --mount-add type=volume,src=other-volume,target=/somewhere-else \
  --publish-add published=8080,target=80 \
  myservice
```

### Update Network with Alias

```bash
docker service update \
  --network-rm my-network \
  --network-add name=my-network,alias=web1 \
  myservice
```

---

## Jobs (replicated-job/global-job)

### Limitações:
- Update para jobs para tasks em progresso
- Cria novo set de tasks
- Jobs não podem ser rolled out/back
- Force update para re-executar

```bash
# Re-executar job
docker service update --force myjob
```

---

## Key Takeaways

1. **--force:** Recria tasks mesmo sem mudanças (rolling restart)
2. **Rollback:** Manual ou automático
3. **Templates:** Suportado para hostname, env, mount
4. **Jobs:** Comportamento diferente de services
5. **Parallelism:** Controla velocidade de updates