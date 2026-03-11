# Use Multiple Compose Files - Docker Docs

**URL:** https://docs.docker.com/compose/how-tos/multiple-compose-files/
**Lido em:** 2026-03-11
**Categoria:** Compose Advanced
**Prioridade:** Média

---

## Resumo

Visão geral das opções para trabalhar com múltiplos arquivos Compose.

---

## Por que Múltiplos Compose Files

Permite customizar aplicações para diferentes ambientes:
- Development vs Production
- Different teams
- Large applications com dezenas de containers
- Monorepo com ownership distribuído

---

## Três Abordagens

### 1. Merge (flag -f)

```bash
docker compose -f base.yml -f override.yml up
```

- Mais rápido para usar
- Regras de merge podem ser complexas
- Último arquivo sobrepõe anteriores

### 2. Extend

```yaml
services:
  web:
    extends:
      file: common.yml
      service: webapp
```

- Seleciona partes específicas
- Pode override atributos
- Mais controle granular

### 3. Include

```yaml
include:
  - path: common.yml
```

- Inclui serviços inteiros automaticamente
- Não precisa referenciar explicitamente
- Útil para composição de projetos

---

## Comparação

| Aspecto | Merge (-f) | Extend | Include |
|---------|-----------|--------|---------|
| **Velocidade** | Rápido | Médio | Médio |
| **Controle** | Menor | Granular | Médio |
| **Complexidade** | Regras de merge | Simples | Simples |
| **Uso** | Ambientes | Reuso de config | Composição |

---

## Merge Rules

### Listas:
- Variáveis de ambiente: merge
- Volumes: merge
- Ports: merge
- Networks: merge

### Valores Únicos:
- Image: override
- Command: override
- Entrypoint: override

### Complexidade:
- Regras podem ser confusas
- Difícil prever resultado sem testar
- Use `docker compose config` para verificar

---

## Best Practices

1. **Use merge para:** Ambientes (dev, staging, prod)
2. **Use extends para:** Reuso de configuração entre serviços
3. **Use include para:** Composição de projetos independentes
4. **Sempre verifique:** `docker compose config` para ver resultado final

---

## Key Takeaways

1. **Três abordagens:** merge, extends, include
2. **Merge:** Rápido, mas regras complexas
3. **Extends:** Controle granular de configuração
4. **Include:** Inclui serviços automaticamente
5. **Verifique sempre:** Use `docker compose config`