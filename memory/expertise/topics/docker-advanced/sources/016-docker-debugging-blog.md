# Docker Debugging - Docker Blog

**Fonte:** https://www.docker.com/blog/how-to-fix-and-debug-docker-containers-like-a-superhero/
**Tipo:** Blog Post (Docker Official)
**Lido em:** 2026-03-10
**Status:** completed

---

## Ferramentas de Debugging

### 1. CLI Visibility

**Container ls com format:**
```bash
# JSON format com jq
docker container ls --all --format '{{ json . }}' | jq -C

# Python json.tool
docker container ls --all --format '{{ json . }}' | python3 -m json.tool --json-lines

# Tabela expandida
docker container ls --all --format 'table {{ .Names }}\t{{ .Status }}\t{{ .Command }}' --no-trunc
```

### 2. Logs

```bash
# Últimos 100 logs
docker logs --tail 100 [container ID]

# Todos os logs
docker logs [container ID]

# Processos ativos
docker top [container ID]
```

**Logs Explorer Extension:**
- Browse logs with filters
- Advanced search
- Real-time log viewing

### 3. Entrypoint Issues

**Permissões:**
```bash
# Verificar permissões
ls -l entrypoint.sh

# Corrigir
chmod 774 entrypoint.sh
```

**Entrypoint vazio:**
- `--entrypoint` limpa CMD default
- Redefinir comando:
```bash
docker run -d -v ./entrypoint.sh:/entrypoint.sh --entrypoint /entrypoint.sh --name v7 httpd:2.4 httpd-foreground
```

### 4. Container Content Inspection

**Copiar arquivos:**
```bash
docker cp v8:/usr/local/apache2/bin/httpd ./var/v8-httpd
```

**Diff de mudanças:**
```bash
docker container diff v8
```

**Hexdump:**
```bash
hexdump -C -n 100 ./var/v8-httpd
```

### 5. Docker Desktop (nsenter1)

```bash
docker run --rm --privileged --pid=host alpine:3.16.2 nsenter -t 1 -m -u -i -n -p -- sh -c "cd \"$(docker container inspect v8 --format '{{ .GraphDriver.Data.UpperDir }}')\" && find ."
```

### 6. Docker Build Errors

```bash
# Build com progress plain
docker build $PWD/[source] --tag "mytag" --progress plain

# Sem cache
docker build --no-cache -t mytag .
```

### 7. Docker Compose Errors

```bash
# Listar serviços
docker compose --project-directory $PWD ps

# Logs
docker compose logs

# Ver compose file
cat docker-compose.yml
```

---

## Docker Debug Tool

**Docker Desktop 4.33+:**
- GA release of Docker Debug
- Language-independent toolbox
- Debug local and remote containers
- Works even when container fails to launch
- Available in Pro, Teams, Business subscriptions

```bash
docker debug [container]
```

---

## Best Practices

1. **Usar --no-trunc** para ver comandos completos
2. **JSON format** para melhor legibilidade
3. **Logs** sempre primeiro passo
4. **Container diff** para ver mudanças
5. **Progress plain** em builds
6. **Docker Debug** para troubleshooting avançado

## Próximos Passos
- [ ] Instalar Docker Debug
- [ ] Praticar com containers problemáticos
- [ ] Usar Logs Explorer Extension