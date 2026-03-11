# OpenTelemetry Support - Build Debugging

**Fonte:** https://docs.docker.com/build/debug/opentelemetry/
**Prioridade:** Média
**Lido em:** 2026-03-11

---

## Visão Geral

Buildx e BuildKit suportam OpenTelemetry para tracing de builds. Útil para debugging e análise de performance.

---

## Setup com Jaeger

### 1. Criar Container Jaeger
```bash
docker run -d --name jaeger \
  -p "6831:6831/udp" \
  -p "16686:16686" \
  --restart unless-stopped \
  jaegertracing/all-in-one
```

### 2. Criar Builder com OpenTelemetry
```bash
docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "network=host" \
  --driver-opt "env.JAEGER_TRACE=localhost:6831"
```

### 3. Inicializar Builder
```bash
docker buildx inspect --bootstrap
```

### 4. Acessar Traces
```
http://127.0.0.1:16686/
```

---

## Como Funciona

1. **Buildx/BuildKit** envia traces para Jaeger via UDP
2. **Jaeger** coleta e armazena traces
3. **UI Web** permite visualizar e analisar

---

## Use Cases

1. **Debug de builds lentos** - Identificar stages lentas
2. **Análise de cache** - Ver cache hits/misses
3. **Paralelismo** - Verificar execução paralela
4. **CI/CD** - Rastrear builds em pipelines

---

## Conceitos Aprendidos

1. **OpenTelemetry** - Standard de observabilidade
2. **Jaeger** - Backend para traces
3. **driver-opt** - Configurar opções do builder
4. **network=host** - Permitir comunicação com localhost
5. **env.JAEGER_TRACE** - Variável para configurar endpoint

---

## Aplicações Práticas

1. **Performance tuning** - Identificar gargalos
2. **Debug de builds** - Ver onde falhou
3. **CI/CD observability** - Rastrear builds em pipelines
4. **Análise de paralelismo** - Verificar eficiência

---

## Referências Cruzadas

- Ver: `034-buildkit-overview.md`
- Ver: `007-docker-build-cache.md`
- Relacionado: BuildKit, Buildx, Jaeger