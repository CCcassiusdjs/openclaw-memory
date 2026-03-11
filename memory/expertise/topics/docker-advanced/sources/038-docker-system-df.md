# Docker System DF - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/system/df/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Uso

```bash
docker system df [OPTIONS]
```

---

## Descrição

Mostra uso de disco pelo Docker daemon.

---

## Opções

| Opção | Descrição |
|-------|-----------|
| `--format` | Formato de saída (table, json, template) |
| `-v`, `--verbose` | Informação detalhada |

---

## Output Padrão

```console
$ docker system df

TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE
Images              5                   2                   16.43 MB            11.63 MB (70%)
Containers          2                   0                   212 B               212 B (100%)
Local Volumes       2                   1                   36 B                0 B (0%)
```

### Campos
| Campo | Descrição |
|-------|-----------|
| TYPE | Images, Containers, Local Volumes, Build Cache |
| TOTAL | Quantidade total |
| ACTIVE | Quantidade em uso |
| SIZE | Tamanho total |
| RECLAIMABLE | Espaço recuperável |

---

## Output Verboso

```console
$ docker system df -v

Images space usage:

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE                SHARED SIZE         UNIQUE SIZE         CONTAINERS
my-curl             latest              b2789dd875bf        6 minutes ago       11 MB               11 MB               5 B                 0
my-jq               latest              ae67841be6d0        6 minutes ago       9.623 MB            8.991 MB            632.1 kB            0
<none>              <none>              a0971c4015c1        6 minutes ago       11 MB               11 MB               0 B                 0
alpine              latest              4e38e38c8ce0        9 weeks ago         4.799 MB            0 B                 4.799 MB            1
alpine              3.3                 47cf20d8c26c        9 weeks ago         4.797 MB            4.797 MB            0 B                 1

Containers space usage:

CONTAINER ID        IMAGE               COMMAND             LOCAL VOLUMES       SIZE                CREATED             STATUS                      NAMES
4a7f7eebae0f        alpine:latest       "sh"                1                   0 B                 16 minutes ago      Exited (0) 5 minutes ago    hopeful_yalow
f98f9c2aa1ea        alpine:3.3          "sh"                1                   212 B               16 minutes ago      Exited (0) 48 seconds ago   anon-vol

Local Volumes space usage:

NAME                                                               LINKS               SIZE
07c7bdf3e34ab76d921894c2b834f073721fccfbbcba792aa7648e3a7a664c2e   2                   36 B
my-named-vol                                                       0                   0 B
```

---

## Tamanhos de Imagens

| Campo | Descrição |
|-------|-----------|
| **SHARED SIZE** | Espaço compartilhado com outras imagens (layers comuns) |
| **UNIQUE SIZE** | Espaço único da imagem |
| **SIZE** | SHARED + UNIQUE (tamanho virtual) |

### Exemplo
```
Imagem A: 11 MB shared + 5 B unique = 11 MB total
Imagem B: 11 MB shared + 0 B unique = 11 MB total
          (compartilha todas as layers com A)
```

---

## Reclaimable Space

- **Images**: Imagens não usadas por containers
- **Containers**: Containers parados (container layer writable)
- **Volumes**: Volumes não linkados a containers
- **Build Cache**: Cache de builds não usado

### Limpar Espaço
```bash
# Ver quanto pode recuperar
docker system df

# Recuperar tudo
docker system prune -a

# Recuperar apenas imagens
docker image prune -a

# Recuperar apenas volumes
docker volume prune
```

---

## Formato JSON

```bash
$ docker system df --format json
{"Type":"Images","TotalCount":5,"Active":2,"Size":17196611,"ReclaimableSize":12194206}
...
```

### Go Template
```bash
$ docker system df --format "table {{.Type}}\t{{.TotalCount}}\t{{.Size}}"
TYPE                TOTAL               SIZE
Images              5                   16.43 MB
Containers          2                   212 B
Local Volumes       2                   36 B
```

---

## Notas

- Networks não são mostradas porque não consomem disco
- Reclaimable depende de containers ativos
- Build Cache aparece se configurado

---

## Conceitos Aprendidos

1. **SHARED SIZE** - Layers compartilhadas entre imagens
2. **UNIQUE SIZE** - Layers únicas da imagem
3. **Reclaimable** - Espaço recuperável
4. **Verbose** - Detalhes por item individual
5. **Format templates** - Go templates para output

---

## Aplicações Práticas

1. **Disk cleanup** - Identificar espaço recuperável
2. **Cost analysis** - Estimar storage costs
3. **Layer sharing** - Entender otimização de imagens
4. **Automation** - Parse JSON para monitoring

---

## Referências Cruzadas

- Ver: `007-docker-build-cache.md`
- Ver: `002-docker-volumes.md`
- Relacionado: docker system prune, image prune, volume prune