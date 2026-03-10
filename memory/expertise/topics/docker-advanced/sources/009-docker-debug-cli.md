# Docker Debug CLI

**Fonte:** https://docs.docker.com/reference/cli/docker/debug/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## O que é Docker Debug

Ferramenta CLI para debuggar containers e imagens sem modificar a imagem.

**Vantagens:**
- Funciona em imagens slim (sem shell)
- Não modifica a imagem
- Traz toolbox com ferramentas comuns
- Instala ferramentas adicionais via Nix

---

## Uso Básico

### Debuggar Container
```bash
# Container rodando
docker debug my-container

# Container parado
docker debug my-stopped-container

# Imagem (sem container)
docker debug nginx:latest
```

### Debuggar Imagem Remota
```bash
# Faz pull automático
docker debug hello-world
```

---

## Shell Options

```bash
# Shell específico
docker debug --shell bash my-container
docker debug --shell fish my-container
docker debug --shell zsh my-container

# Auto-detect (default)
docker debug --shell auto my-container
```

---

## Toolbox (Ferramentas Incluídas)

**Pre-instaladas:**
- `vim`, `nano` - Editores
- `htop` - Monitor de processos
- `curl`, `wget` - HTTP clients
- `grep`, `sed`, `awk` - Text processing
- `find`, `ls`, `cat` - File operations

---

## Instalar Ferramentas Adicionais

```bash
# Entrar no debug
docker debug nginx

# Instalar ferramenta (via Nix)
docker > install nmap
docker > install jq
docker > install tcpdump

# Ferramentas disponíveis: https://search.nixos.org/packages

# Desinstalar
docker > uninstall nmap

# Ver builtin tools
docker > builtins
```

**Nota:** Ferramentas instaladas ficam no toolbox, não na imagem!

---

## Comandos Úteis

### Entrypoint Investigation
```bash
docker debug nginx

# Ver entrypoint
docker > entrypoint --print
/docker-entrypoint.sh

# Lintar entrypoint
docker > entrypoint --lint
 PASS: '/docker-entrypoint.sh' found
 PASS: no mixing of shell and exec form

# Rodar entrypoint (teste)
docker > entrypoint --run
```

### Scripting (Non-Interactive)
```bash
# Executar comando sem shell interativo
docker debug --command "cat /etc/nginx/nginx.conf" nginx

# Útil para scripts e CI
docker debug --command "ls -la /app" my-image
```

### Remote Debugging
```bash
# Via SSH
docker debug --host ssh://root@example.org my-container

# Via socket alternativo
docker debug --host unix:///some/path/docker.sock my-container
```

---

## Diferença: docker debug vs docker exec

| Aspecto | docker exec | docker debug |
|---------|-------------|--------------|
| Requer shell na imagem | Sim | Não |
| Modifica a imagem | Não | Não |
| Ferramentas disponíveis | Apenas as da imagem | Toolbox + Nix |
| Funciona em slim images | Limitado | Sim |
| Funciona em container parado | Não | Sim |
| Funciona em imagem | Não | Sim |

---

## Casos de Uso

### 1. Debuggar imagem slim
```bash
# Imagem sem shell
docker debug gcr.io/distroless/static-debian12

# Ver arquivos
docker > ls /
docker > cat /etc/passwd
```

### 2. Modificar arquivo em container rodando
```bash
docker debug nginx
docker > vim /usr/share/nginx/html/index.html
# Mudanças são visíveis no container!
```

### 3. Debuggar entrypoint
```bash
docker debug my-app
docker > entrypoint --print
docker > entrypoint --lint
docker > entrypoint --run
```

### 4. Instalar ferramentas de diagnóstico
```bash
docker debug suspicious-container
docker > install nmap
docker > install tcpdump
docker > nmap localhost
docker > tcpdump -i eth0
```

---

## Boas Práticas

1. **Usar docker debug** ao invés de adicionar ferramentas na imagem
2. **Não modificar imagens** para debug - use o toolbox
3. **Criar alias** para comandos comuns
4. **Documentar entrypoints** para troubleshooting
5. **Usar --command** para scripts de diagnóstico

## Próximos Passos
- [ ] Praticar com diferentes tipos de imagens
- [ ] Explorar Nix packages disponíveis
- [ ] Criar scripts de diagnóstico