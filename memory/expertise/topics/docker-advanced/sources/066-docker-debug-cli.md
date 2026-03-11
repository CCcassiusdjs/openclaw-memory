# docker debug - Docker CLI Reference

**URL:** https://docs.docker.com/reference/cli/docker/debug/
**Lido em:** 2026-03-11
**Categoria:** Debugging
**Prioridade:** Alta

---

## Resumo

Comando para debug de containers e images, alternativa ao `docker exec` para containers slim.

---

## O que é

Docker Debug permite obter shell em qualquer container ou image, mesmo sem shell instalado.

### Benefícios:
- Debug de slim/minimal containers
- Não modifica a imagem
- Toolbox própria com ferramentas Linux
- Suporte a bash, fish, zsh

---

## Uso Básico

```bash
# Debug de container
docker debug my-container

# Debug de imagem (sem container)
docker debug nginx

# Debug de container parado
docker debug stopped-container
```

---

## Opções

| Flag | Default | Descrição |
|------|---------|-----------|
| `--shell` | auto | Shell: bash, fish, zsh, auto |
| `-c, --command` | | Executar comando diretamente |
| `--host` | | Conectar a Docker remoto |

---

## Toolbox

### Ferramentas Pre-instaladas:
- vim
- nano
- htop
- curl

### Comandos Custom:

```bash
# Instalar pacote Nix
install nmap

# Desinstalar
uninstall nmap

# Ver entradaoint
entrypoint --print

# Rodar entradaoint
entrypoint --run

# Ver builtins
builtins
```

### Nix Packages:
Ferramentas de: https://search.nixos.org/packages

---

## Exemplos

### Container sem Shell

```bash
# Container slim (hello-world não tem shell)
docker run --name my-app hello-world

# Debug funciona mesmo assim
docker debug my-app
docker> ls
dev  etc  hello  nix  proc  sys
```

### Debug de Imagem Direta

```bash
# Não precisa criar container
docker debug nginx
docker> ls /usr/share/nginx/html
```

### Modificar Container Running

```bash
# Editar arquivo em container running
docker run -d --name web-app -p 8080:80 nginx
docker debug web-app
docker> vim /usr/share/nginx/html/index.html
# Mudanças são visíveis no container
```

### Instalar Ferramentas

```bash
docker debug nginx
docker> install nmap
docker> nmap --version
```

### Comando Direto (Scripting)

```bash
# Executar sem shell interativo
docker debug --command "cat /usr/share/nginx/html/index.html" nginx
```

### Debug Remoto

```bash
# Via SSH
docker debug --host ssh://root@example.org my-container

# Via socket local
docker debug --host unix:///some/path/docker.sock my-container
```

---

## Entrypoint Tool

```bash
# Ver entradaoint
docker> entrypoint --print
/hello

# Ver detalhes do entradaoint
docker> entrypoint
From CMD in Dockerfile:
 ['nginx', '-g', 'daemon off;']

From ENTRYPOINT in Dockerfile:
 ['/docker-entrypoint.sh']

By default, any container from this image will be started with:
/docker-entrypoint.sh nginx -g daemon off;

Lint results:
 PASS: '/docker-entrypoint.sh' found
 PASS: no mixing of shell and exec form
 PASS: no double use of shell form
```

---

## Comportamento

| Tipo | Mudanças |
|------|----------|
| **Imagem** | Descartadas ao sair |
| **Container parado** | Descartadas ao sair |
| **Container running** | Visíveis no container |
| **Qualquer** | `/nix` não é visível ao container |

---

## Comparação: debug vs exec

| Aspecto | docker exec | docker debug |
|---------|-------------|--------------|
| **Requer shell** | Sim | Não |
| **Modifica imagem** | Não | Não |
| **Ferramentas** | Do container | Toolbox próprio |
| **Slim containers** | ❌ | ✅ |
| **Imagens** | ❌ | ✅ |
| **Stopped containers** | ❌ | ✅ |

---

## Key Takeaways

1. **Funciona sem shell:** Ideal para slim containers
2. **Toolbox próprio:** vim, nano, htop, curl + install de Nix
3. **Não modifica:** Imagem/container permanecem intactos
4. **entrypoint tool:** Entende CMD/ENTRYPOINT
5. **Remoto:** Suporta SSH e sockets