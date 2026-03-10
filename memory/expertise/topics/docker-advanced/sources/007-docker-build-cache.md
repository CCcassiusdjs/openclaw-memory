# Docker Build Cache

**Fonte:** https://docs.docker.com/build/cache/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. Como Funciona o Cache
Cada instrução no Dockerfile = uma layer na imagem.

```
┌─────────────────────┐
│  RUN make build     │ ← Topo (última layer)
├─────────────────────┤
│  COPY main.c ...    │
├─────────────────────┤
│  RUN apt-get ...    │
├─────────────────────┤
│  FROM ubuntu:latest │ ← Base
└─────────────────────┘
```

### 2. Cache Invalidation
- Se uma layer muda, ela precisa ser re-built
- **Todas as layers subsequentes também precisam ser re-built**
- Mesmo que não produzam nada diferente

```
┌─────────────────────┐
│  RUN make build     │ ← INVALIDATED (depois de COPY)
├─────────────────────┤
│  COPY main.c ...    │ ← INVALIDATED (arquivo mudou)
├─────────────────────┤
│  RUN apt-get ...    │ ← Cache hit (antes de COPY)
├─────────────────────┤
│  FROM ubuntu:latest │ ← Cache hit
└─────────────────────┘
```

### 3. Regra de Ouro
**Ordem importa!** Coloque instruções mais estáveis primeiro:
1. FROM (base image)
2. Instalação de dependências (pouco muda)
3. COPY de arquivos de dependência (package.json, requirements.txt)
4. Instalação de dependências do projeto
5. COPY do código fonte (muda frequentemente)
6. Build/compilação

---

## Otimização do Cache

### Padrão Correto (Node.js)
```dockerfile
FROM node:20-alpine
WORKDIR /app

# Primeiro: copiar apenas package.json (cache hit se dependências não mudarem)
COPY package*.json ./

# Segundo: instalar dependências (cache hit se package.json não mudar)
RUN npm ci

# Terceiro: copiar código (invalida cache daqui para baixo)
COPY . .

# Quarto: build (re-executa se código mudar)
RUN npm run build
```

### Padrão Incorreto
```dockerfile
FROM node:20-alpine
WORKDIR /app

# ERRADO: copiar tudo primeiro invalida cache de npm install
COPY . .
RUN npm ci  # Re-executa toda vez que QUALQUER arquivo muda
RUN npm run build
```

---

## Recursos Relacionados

- **Cache invalidation** - Como evitar invalidação desnecessária
- **Optimize build cache** - Estratégias avançadas
- **Garbage collection** - Limpar cache antigo
- **Cache storage backends** - Cache remoto (CI/CD)

---

## Boas Práticas

1. **Ordem das instruções** - Mais estáveis primeiro
2. **Separar dependências** - COPY package.json antes do código
3. **Usar .dockerignore** - Reduz contexto e mudanças
4. **Multi-stage builds** - Separa build de runtime
5. **BuildKit** - Cache mais eficiente
6. **Cache remoto** - Compartilhar cache entre builds (CI/CD)

## Próximos Passos
- [ ] Estudar cache backends para CI/CD
- [ ] Configurar garbage collection
- [ ] Praticar otimização de Dockerfiles