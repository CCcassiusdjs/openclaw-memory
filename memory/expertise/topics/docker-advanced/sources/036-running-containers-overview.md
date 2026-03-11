# Running Containers - Documentação Oficial

**Fonte:** https://docs.docker.com/engine/containers/run/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Forma Geral

```bash
docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

---

## Image References

### Formato
```
[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]
```

| Componente | Descrição |
|------------|-----------|
| `HOST` | Registry (default: docker.io) |
| `PORT` | Porta do registry (opcional) |
| `NAMESPACE` | Usuário/organização (default: library) |
| `REPOSITORY` | Nome da imagem |
| `TAG` | Versão (default: latest) |

### Exemplos
```bash
# Tag específica
docker run ubuntu:24.04

# Digest específico
docker run alpine@sha256:9cacb71397b640eca97488cf08582ae4e4068513101088e9f96c9814bfda95e0

# Registry privado
docker run myregistry:5000/team/app:2.0
```

---

## Foreground e Background

### Foreground (Default)
```bash
docker run nginx
# Ocupa o terminal
```

### Background (Detached)
```bash
docker run -d nginx
# Retorna container ID

# Ver logs
docker logs -n 5 <container_id>

# Re-attach
docker attach <container_id>
```

### Flags de Attach
| Flag | Descrição |
|------|-----------|
| `-d`, `--detach` | Rodar em background |
| `-a`, `--attach` | Attach stdin/stdout/stderr |
| `-t`, `--tty` | Alocar pseudo-TTY |
| `-i`, `--interactive` | Manter stdin aberto |

---

## Container Identification

### Tipos de Identificador
| Tipo | Exemplo |
|------|---------|
| UUID longo | `f78375b1c487e03c9438c729345e54db9d20cfa2ac1fc3494b6eb60872e74778` |
| UUID curto | `f78375b1c487` |
| Nome | `evil_ptolemy` |

### Nome Customizado
```bash
docker run --name my-container nginx
# Pode usar o nome como referência
docker logs my-container
```

### Filtrar por Imagem
```bash
# Containers rodando nginx:alpine
docker ps -q --filter ancestor=nginx:alpine
```

---

## Container Networking

### Criar Rede Customizada
```bash
docker network create my-net
docker run -d --name web --network my-net nginx:alpine
docker run -rm -it --network my-net busybox

# DNS por nome de container
ping web  # Funciona na rede customizada
```

### Benefícios
- DNS automático por nome
- Isolamento de rede
- Containers se comunicam por nome

---

## Filesystem Mounts

### Volume Mounts
```bash
# Criar e usar volume
docker run --mount source=my_volume,target=/foo busybox echo "hello" > /foo/hello.txt

# Dados persistem
docker run --mount source=my_volume,target=/bar busybox cat /bar/hello.txt
```

### Bind Mounts
```bash
# Montar diretório do host
docker run -it --mount type=bind,source=.,target=/foo busybox

# Leitura e escrita no host
echo "hello from container" > /foo/hello.txt
```

### Diferenças
| Volume | Bind Mount |
|--------|------------|
| Gerenciado pelo Docker | Diretório do host |
| Melhor para persistência | Melhor para compartilhar |
| Portável | Depende do host |

---

## Exit Codes

| Code | Significado |
|------|-------------|
| 125 | Erro do Docker daemon |
| 126 | Comando não pode ser invocado |
| 127 | Comando não encontrado |
| Outros | Exit code do comando do container |

### Exemplos
```bash
# 125: Flag inválida
docker run --foo busybox; echo $?
# flag provided but not defined: --foo

# 126: Não executável
docker run busybox /etc; echo $?
# Container command '/etc' could not be invoked

# 127: Não encontrado
docker run busybox foo; echo $?
# Container command 'foo' not found

# Exit code do comando
docker run busybox /bin/sh -c 'exit 3'; echo $?
# 3
```

---

## Runtime Constraints

### Memory
| Opção | Formato | Mínimo |
|-------|---------|--------|
| `--memory` | `<number>[b\|k\|m\|g]` | 6m |
| `--memory-swap` | `<number>[b\|k\|m\|g]` | - |
| `--kernel-memory` | `<number>[b\|k\|m\|g]` | 4m |

### CPU
| Opção | Formato |
|-------|---------|
| `--cpus` | Float (ex: 0.5, 1.5) |
| `--cpu-shares` | Inteiro (default: 1024) |
| `--cpuset-cpus` | Lista (ex: 0-3, 1,3) |

### Block IO
| Opção | Formato |
|-------|---------|
| `--blkio-weight` | 10-1000 |
| `--device-read-bps` | `<device>:<rate>` |
| `--device-write-iops` | `<device>:<count>` |

---

## Runtime Privilege

### Capabilities

#### Default (mantidas)
| Capability | Descrição |
|------------|-----------|
| CHOWN | Mudar UIDs e GIDs |
| DAC_OVERRIDE | Bypass de permissões |
| KILL | Bypass de permissões para signals |
| MKNOD | Criar arquivos especiais |
| NET_BIND_SERVICE | Bind em portas < 1024 |
| SETUID/SETGID | Manipular UIDs/GIDs |

#### Não Default (adicionar)
| Capability | Descrição |
|------------|-----------|
| NET_ADMIN | Operações de rede |
| SYS_ADMIN | Operações administrativas |
| SYS_PTRACE | Trace de processos |

### Exemplos
```bash
# Adicionar capability específica
docker run --cap-add=NET_ADMIN ubuntu ip link add dummy0

# Usar todas menos uma
docker run --cap-add=ALL --cap-drop=MKNOD ubuntu

# Privileged (todas capabilities + devices)
docker run --privileged ubuntu
```

---

## Overriding Image Defaults

### Comando e Argumentos
```bash
# Override CMD
docker run ubuntu echo "custom command"

# ENTRYPOINT + CMD
docker run --entrypoint /bin/sh ubuntu -c "echo hello"
```

### Variáveis de Ambiente
```bash
docker run -e MY_VAR=value ubuntu
docker run --env-file .env ubuntu
```

### Ports
```bash
docker run -p 8080:80 nginx
docker run -P nginx  # Publica todas as portas EXPOSE
```

---

## Conceitos Aprendidos

1. **Image reference** - Host, port, namespace, repo, tag
2. **Detached mode** - `-d` para background, `attach` para re-conectar
3. **Exit codes** - 125 (Docker), 126 (invoke), 127 (not found)
4. **Custom networks** - DNS por nome de container
5. **Capabilities** - Fine-grained control sobre privilégios

---

## Aplicações Práticas

1. **Development** - Bind mounts para hot reload
2. **Production** - Volumes para persistência
3. **Networking** - Redes customizadas para microserviços
4. **Resource limits** - Multi-tenant isolation
5. **Security** - Capabilities ao invés de privileged

---

## Referências Cruzadas

- Ver: `001-docker-run-reference.md`
- Ver: `035-resource-constraints.md`
- Ver: `002-docker-volumes.md`
- Relacionado: Docker networks, storage, security