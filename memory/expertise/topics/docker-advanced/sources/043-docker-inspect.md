# Docker Inspect - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/inspect/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Uso

```bash
docker inspect [OPTIONS] NAME|ID [NAME|ID...]
```

---

## Descrição

Retorna informação detalhada sobre objetos Docker. Por default, output em JSON array.

---

## Opções

| Opção | Descrição |
|-------|-----------|
| `-f`, `--format` | Formatar output com Go template |
| `-s`, `--size` | Mostrar tamanho total (containers) |
| `--type` | Filtrar por tipo de objeto |

---

## Tipos de Objetos

```
config|container|image|node|network|secret|service|volume|task|plugin
```

---

## Formato com Templates

### Go Templates
```bash
docker inspect --format='{{.Field}}' CONTAINER
```

### JSON
```bash
docker inspect --format='{{json .Config}}' CONTAINER
```

### Funções Template
- `{{.Field}}` - Campo direto
- `{{range .Array}}` - Iterar arrays
- `{{index .Map "key"}}` - Acessar map por chave
- `{{json .Field}}` - Converter para JSON

---

## Exemplos

### IP Address
```bash
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER
# 172.17.0.2
```

### MAC Address
```bash
docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' CONTAINER
# 02:42:ac:11:00:02
```

### Log Path
```bash
docker inspect --format='{{.LogPath}}' CONTAINER
# /var/lib/docker/containers/.../json.log
```

### Image Name
```bash
docker inspect --format='{{.Config.Image}}' CONTAINER
# nginx:alpine
```

### Port Bindings
```bash
docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{(index $conf 0).HostPort}} {{end}}' CONTAINER
# 80/tcp -> 8080
```

### Porta Específica
```bash
docker inspect --format='{{(index (index .NetworkSettings.Ports "8787/tcp") 0).HostPort}}' CONTAINER
# 8787
```

### Subseção JSON
```bash
docker inspect --format='{{json .Config}}' CONTAINER | jq
```

---

## Tamanho de Container (--size)

```bash
docker inspect --size mycontainer
```

### Campos Adicionais

| Campo | Descrição |
|-------|-----------|
| `SizeRootFs` | Tamanho total de todos os arquivos no container |
| `SizeRw` | Tamanho dos arquivos criados/modificados (vs imagem base) |

### Exemplo
```bash
docker run --name database -d redis
docker inspect --size database -f '{{ .SizeRootFs }}'
# 123125760

docker inspect --size database -f '{{ .SizeRw }}'
# 8192

docker exec database fallocate -l 1000 /newfile
docker inspect --size database -f '{{ .SizeRw }}'
# 12288
```

---

## Filtrar por Tipo

```bash
# Volume
docker inspect --type=volume myvolume

# Container
docker inspect --type=container mycontainer

# Image
docker inspect --type=image myimage
```

### Quando Usar
- Quando mesmo nome existe para diferentes tipos
- Para evitar ambiguidade

---

## Estrutura JSON Comum

### Container
```json
{
  "Id": "abc123...",
  "Created": "2024-01-01T00:00:00Z",
  "Path": "nginx",
  "Args": [],
  "State": {
    "Status": "running",
    "Running": true,
    "Paused": false,
    "Pid": 12345
  },
  "Image": "sha256:...",
  "NetworkSettings": {
    "Networks": {
      "bridge": {
        "IPAddress": "172.17.0.2",
        "MacAddress": "02:42:ac:11:00:02"
      }
    }
  },
  "Config": {
    "Image": "nginx:alpine",
    "Env": ["PATH=/usr/local/sbin:..."],
    "Cmd": ["nginx", "-g", "daemon off;"]
  },
  "HostConfig": {
    "PortBindings": {"80/tcp": [{"HostPort": "8080"}]},
    "Memory": 0,
    "CpuShares": 1024
  }
}
```

---

## Conceitos Aprendidos

1. **JSON por default** - Output estruturado
2. **Go templates** - Formatação flexível
3. **--type** - Evitar ambiguidade
4. **--size** - Tamanho do container layer
5. **index function** - Acessar campos com nomes numéricos

---

## Aplicações Práticas

1. **IP discovery** - Obter IP de container
2. **Port mapping** - Verificar portas mapeadas
3. **Volume paths** - Localizar volumes no host
4. **Environment variables** - Ver configurações
5. **Debugging** - Estado detalhado do container

---

## Referências Cruzadas

- Ver: `042-docker-exec.md`
- Ver: `006-docker-resource-limits.md`
- Relacionado: docker ps, docker stats