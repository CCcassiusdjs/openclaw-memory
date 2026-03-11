# Extend your Compose File - Docker Docs

**URL:** https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/
**Lido em:** 2026-03-11
**Categoria:** Compose Advanced
**Prioridade:** Média

---

## Resumo

Documentação sobre o atributo `extends` para compartilhar configurações entre serviços Compose.

---

## O que é extends

Permite compartilhar configurações comuns entre serviços:
- Diferentes arquivos Compose
- Diferentes projetos
- Mesmo arquivo

### Benefícios:
- DRY (Don't Repeat Yourself)
- Configuração centralizada
- Override de atributos específicos

---

## Sintaxe Básica

### De outro arquivo:

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
```

### Do mesmo arquivo:

```yaml
services:
  web:
    build: ./alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### Combinando arquivo + local:

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
    environment:
      - DEBUG=1
    cpu_shares: 5

  important_web:
    extends: web
    cpu_shares: 10
```

---

## Exemplo Completo

### common.yaml:

```yaml
services:
  app:
    build: .
    environment:
      CONFIG_FILE_PATH: /code/config
      API_KEY: xxxyyy
    cpu_shares: 5
```

### compose.yaml:

```yaml
services:
  webapp:
    extends:
      file: common.yaml
      service: app
    command: /code/run_web_app
    ports:
      - 8080:8080
    depends_on:
      - queue
      - db

  queue_worker:
    extends:
      file: common.yaml
      service: app
    command: /code/run_worker
    depends_on:
      - queue
```

---

## Relative Paths

### Importante:
- Paths são relativos ao **base Compose file**
- Extends files não precisam ser Compose files válidos
- Podem conter apenas fragments

### Exemplo:

**Base: compose.yaml:**
```yaml
services:
  webapp:
    image: example
    extends:
      file: ../commons/compose.yaml
      service: base
```

**commons/compose.yaml:**
```yaml
services:
  base:
    env_file: ./container.env
```

**Result (docker compose config):**
```yaml
services:
  webapp:
    image: example
    env_file: 
      - ../commons/container.env
```

---

## Diferença: extends vs include

| Aspecto | extends | include |
|---------|---------|---------|
| **Propósito** | Reutilizar configuração | Incluir serviços inteiros |
| **Serviço original** | Não incluído automaticamente | Incluído automaticamente |
| **Validação** | Pode ser fragment | Deve ser Compose válido |

---

## Incluir Serviço Estendido

Para incluir o serviço original:

```yaml
services:
  web:
    build: ./alpine
    command: echo
    extends:
      file: common-services.yml
      service: webapp
  webapp:
    extends:
      file: common-services.yml
      service: webapp
```

Ou usar `include`.

---

## Key Takeaways

1. **extends:** Reutiliza configuração de outro serviço
2. **file + service:** Aponta para arquivo e serviço específico
3. **Relative paths:** São relativos ao base file
4. **Override:** Atributos locais sobrepõem extends
5. **DRY:** Evita repetição de configuração