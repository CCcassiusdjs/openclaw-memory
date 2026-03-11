# Docker Container Exec - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/container/exec/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Uso

```bash
docker container exec [OPTIONS] CONTAINER COMMAND [ARG...]
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

---

## Descrição

Executa um comando em um container em execução. O comando roda enquanto o processo principal (PID 1) está rodando.

---

## Opções

| Opção | Default | Descrição |
|-------|---------|-----------|
| `-d`, `--detach` | - | Rodar em background |
| `--detach-keys` | - | Sequência de teclas para detach |
| `-e`, `--env` | - | Variáveis de ambiente (API 1.25+) |
| `--env-file` | - | Arquivo com variáveis de ambiente |
| `-i`, `--interactive` | - | Manter STDIN aberto |
| `--privileged` | - | Privilégios estendidos |
| `-t`, `--tty` | - | Alocar pseudo-TTY |
| `-u`, `--user` | - | Usuário ou UID |
| `-w`, `--workdir` | - | Diretório de trabalho (API 1.35+) |

---

## Requisitos

1. Container deve estar **rodando** (não pode estar pausado)
2. O processo principal (PID 1) deve estar ativo
3. O comando deve ser um **executável**

### O que Funciona
```bash
docker exec -it my_container sh -c "echo a && echo b"
```

### O que NÃO Funciona
```bash
docker exec -it my_container "echo a && echo b"
```

---

## Exemplos

### Executar em Background
```bash
docker exec -d mycontainer touch /tmp/execWorks
```

### Shell Interativo
```bash
docker exec -it mycontainer sh
```

### Com Variáveis de Ambiente
```bash
docker exec -e VAR_A=1 -e VAR_B=2 mycontainer env
# PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
# HOSTNAME=f64a4851eb71
# VAR_A=1
# VAR_B=2
# HOME=/root
```

### Diretório de Trabalho
```bash
# Default: diretório do container
docker exec -it mycontainer pwd
# /

# Customizado
docker exec -it -w /root mycontainer pwd
# /root
```

### Usuário Específico
```bash
docker exec -u root mycontainer whoami
# root
```

### Privilégios Estendidos
```bash
docker exec --privileged mycontainer command
# CUIDADO: dá acesso total ao host
```

---

## Container Pausado

Se o container estiver pausado, `docker exec` falha:

```bash
docker pause mycontainer
docker exec mycontainer sh
# Error response from daemon: Container mycontainer is paused, unpause the container before exec
```

---

## Diferenças vs docker run

| Aspecto | docker exec | docker run |
|---------|-------------|------------|
| Container | Existente | Novo |
| Processo principal | Não afeta | É o processo principal |
| Variáveis de ambiente | Adicionais à existentes | Definem o ambiente |
| Working directory | Default do container | Pode ser definido no run |

---

## Conceitos Aprendidos

1. **PID 1** - Processo principal deve estar rodando
2. **Container pausado** - Não aceita exec
3. **-it** - Interativo com TTY
4. **--env** - Variáveis apenas para o comando
5. **--workdir** - Diretório específico para execução

---

## Aplicações Práticas

1. **Debugging** - Entrar no container para investigar
2. **One-off commands** - Executar comandos únicos
3. **Hot reload** - Recarregar configurações
4. **File operations** - Criar/modificar arquivos
5. **Health checks** - Verificar estado interno

---

## Referências Cruzadas

- Ver: `043-docker-inspect.md`
- Ver: `001-docker-run-reference.md`
- Relacionado: Container lifecycle, debugging