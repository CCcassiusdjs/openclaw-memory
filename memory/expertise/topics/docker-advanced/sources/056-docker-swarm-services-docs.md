# Deploy Services to a Swarm - Docker Docs

**URL:** https://docs.docker.com/engine/swarm/services/
**Lido em:** 2026-03-11
**Categoria:** Orchestration
**Prioridade:** Alta

---

## Resumo

Documentação oficial completa sobre criação e gerenciamento de serviços Docker Swarm.

---

## Conceito Declarativo

Swarm services são **declarativos**: você define o estado desejado, Docker mantém.

### Estado inclui:
- Image name e tag
- Número de containers (replicas)
- Ports expostos
- Auto-start policy
- Comportamento de restart
- Resource constraints
- Placement preferences

---

## Comandos Básicos

### Criar Serviço

```bash
# Serviço simples (nome aleatório)
docker service create nginx

# Com nome específico
docker service create --name my_web nginx

# Com comando
docker service create --name helloworld alpine ping docker.com

# Com tag específica
docker service create --name helloworld alpine:3.6 ping docker.com

# Com porta publicada
docker service create --name my_web --publish 8080:80 nginx

# Com replicas
docker service create --name my_web --replicas 3 nginx

# Modo global (um por node)
docker service create --name myservice --mode global alpine top
```

### Listar Serviços

```bash
docker service ls
```

### Remover Serviço

```bash
docker service remove my_web
```

---

## Image Version Resolution

### Tag Resolution:
1. **Tag específica:** `ubuntu:16.04` → resolved to digest
2. **`latest`:** Convenção, resolve para digest atual
3. **Digest direto:** `ubuntu@sha256:xxx` → sempre mesma versão

### Importante:
- Image é resolvida para digest **no momento da criação**
- Workers usam o digest, não a tag
- Atualizar imagem requer `docker service update --image`

### Com Content Trust:
- Client resolve tag para digest antes de enviar ao manager
- Verifica assinatura da imagem

---

## Publish Ports

### Dois Métodos:

#### 1. Routing Mesh (Padrão)
- Porta publicada em **todos** os nodes
- Routing mesh redireciona para task
- Não precisa saber qual node tem task

```bash
docker service create \
  --name my_web \
  --replicas 3 \
  --publish published=8080,target=80 \
  nginx
```

#### 2. Host Mode (Direct)
- Porta no node onde task roda
- Bypass do routing mesh
- Controle total de routing

```bash
docker service create \
  --mode global \
  --publish mode=host,target=80,published=8080 \
  --name=nginx \
  nginx:latest
```

### Limitações do Host Mode:
- `mode=host` + `published=<PORT>` → só 1 task por node
- Sem `--mode=global` → difícil saber onde estão as tasks

---

## Overlay Networks

### Criar e Conectar:

```bash
# Criar overlay network
docker network create --driver overlay my-network

# Conectar serviço na criação
docker service create \
  --replicas 3 \
  --network my-network \
  --name my-web \
  nginx

# Adicionar network a serviço existente
docker service update --network-add my-network my-web

# Remover network
docker service update --network-rm my-network my-web
```

### Comportamento:
- Network é estendida para cada node que roda o serviço
- Todos os manager nodes têm acesso à network

---

## Services Types

### Replicated vs Global

| Tipo | Comportamento |
|------|---------------|
| **Replicated** | N replicas em nodes disponíveis |
| **Global** | 1 task por node no cluster |

```bash
# Replicated (padrão)
docker service create --replicas 3 nginx

# Global
docker service create --mode global nginx
```

---

## Resource Constraints

### Reserve Resources:

```bash
# Reservar CPU e memória
docker service create \
  --reserve-memory 512M \
  --reserve-cpu 1 \
  nginx
```

### Comportamento:
- Se nenhum node satisfaz requisitos → serviço fica **pending**
- OOME (Out Of Memory Exception) pode matar containers

---

## Placement Constraints

### Limitar nodes para serviço:

```bash
# Constraint por label
docker service create \
  --constraint node.labels.region==east \
  nginx

# Múltiplos constraints (AND)
docker service create \
  --constraint node.labels.region==east \
  --constraint node.labels.type!=devel \
  nginx
```

### Operadores:
- `==` (igualdade)
- `!=` (diferença)

---

## Placement Preferences

### Spread Algorithm:

```bash
# Spread por datacenter
docker service create \
  --replicas 9 \
  --placement-pref 'spread=node.labels.datacenter' \
  redis:7.4.0

# Spread múltiplo (hierarquia)
docker service create \
  --replicas 9 \
  --placement-pref 'spread=node.labels.datacenter' \
  --placement-pref 'spread=node.labels.rack' \
  redis:7.4.0
```

### Comportamento:
- **Best-effort:** não falha se label não existe
- Nodes sem label recebem tasks proporcionalmente
- Processados em ordem

---

## Rolling Updates

### Configurar Update Behavior:

```bash
docker service create \
  --replicas 10 \
  --update-delay 10s \
  --update-parallelism 2 \
  --update-failure-action continue \
  alpine
```

### Flags:

| Flag | Descrição |
|------|-----------|
| `--update-delay` | Tempo entre updates (ex: 10m30s) |
| `--update-parallelism` | Tasks atualizadas simultaneamente |
| `--update-failure-action` | pause/continue |
| `--update-max-failure-ratio` | Fração de falhas toleradas |
| `--update-monitor` | Tempo para monitorar após update (default: 30s) |

---

## Rollback

### Manual Rollback:

```bash
# Voltar para versão anterior
docker service update --rollback my_web

# Rollback instantâneo
docker service update --rollback --update-delay 0s my_web
```

### Auto-Rollback:

```bash
docker service create --name=my_redis \
  --replicas=5 \
  --rollback-parallelism=2 \
  --rollback-monitor=20s \
  --rollback-max-failure-ratio=.2 \
  redis:latest
```

### Flags de Rollback:

| Flag | Default | Descrição |
|------|---------|-----------|
| `--rollback-delay` | 0s | Delay entre rollbacks |
| `--rollback-failure-action` | pause | Ação em falha |
| `--rollback-max-failure-ratio` | 0 | Taxa de falha tolerada |
| `--rollback-monitor` | 5s | Tempo de monitoramento |
| `--rollback-parallelism` | 1 | Tasks em paralelo |

---

## Secrets

### Usar secrets gerenciados:

```bash
docker service create --secret my_secret nginx
```

---

## Volumes e Bind Mounts

### Volume Mounts:

```bash
# Volume existente
docker service create \
  --mount src=volume-name,dst=/container/path \
  nginx

# Com driver específico
docker service create \
  --mount type=volume,src=data,dst=/data,volume-driver=nfs \
  nginx
```

### Bind Mounts:

```bash
# Read-write
docker service create \
  --mount type=bind,src=/host/path,dst=/container/path \
  nginx

# Read-only
docker service create \
  --mount type=bind,src=/host/path,dst=/container/path,readonly \
  nginx
```

### Cuidado com Bind Mounts:
- Path deve existir em **todos** os nodes
- Não é portável
- Scheduler pode mover containers entre nodes

---

## Templates

### Variáveis dinâmicas:

```bash
docker service create --name hosttempl \
  --hostname="{{.Node.ID}}-{{.Service.Name}}" \
  busybox top
```

### Placeholders Disponíveis:

| Placeholder | Descrição |
|-------------|-----------|
| `.Service.ID` | Service ID |
| `.Service.Name` | Service name |
| `.Service.Labels` | Service labels |
| `.Node.ID` | Node ID |
| `.Node.Hostname` | Node hostname |
| `.Task.Name` | Task name |
| `.Task.Slot` | Task slot |

### Flags Suportadas:
- `--hostname`
- `--mount`
- `--env`

---

## gMSA (Windows)

### Para Active Directory authentication:

```bash
# Criar config com credspec
docker config create credspec credspec.json

# Usar no serviço
docker service create --credential-spec="config://credspec" <image>
```

---

## Isolation Mode (Windows)

### Tipos:
- `default`: Usa config do daemon
- `process`: Processo separado (só Windows Server)
- `hyperv`: VM isolada (mais overhead)

```bash
docker service create --isolation hyperv nginx
```

---

## Key Takeaways

1. **Declarativo:** Define estado desejado, Docker mantém
2. **Routing Mesh:** Porta em todos os nodes automaticamente
3. **Placement:** Constraints (hard) + Preferences (soft)
4. **Rolling Updates:** Configurável com delay e parallelism
5. **Auto-Rollback:** Proteção contra deployments falhos
6. **Templates:** Variáveis dinâmicas para hostname, env, mounts