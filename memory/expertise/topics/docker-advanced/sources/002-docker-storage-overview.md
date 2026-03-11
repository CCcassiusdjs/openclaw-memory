# Docker Storage Overview

**Fonte:** Docker Docs  
**URL:** https://docs.docker.com/engine/storage/  
**Tipo:** Documentação Oficial  
**Status:** completed

---

## 📋 Resumo Executivo

Docker storage cobre dois conceitos: persistência de dados de containers (volumes, bind mounts, tmpfs) e backends de armazenamento do daemon (containerd image store, storage drivers).

---

## 🔑 Conceitos-Chave

### Container Layer Basics

- **Writable container layer** - Arquivos ficam em camada writeable sobre read-only image layers
- **Non-persistent** - Dados perdidos quando container destruído
- **Isolated** - Camada única por container, difícil extrair dados

---

## 📦 Storage Mount Options

### Volume Mounts

- **Gerenciados pelo Docker daemon**
- **Persistentes** - Retêm dados após container removido
- **Stored on host** - Local gerenciado pelo daemon
- **High performance** - Raw file performance

**Use case:** Dados críticos, longo prazo, performance

### Bind Mounts

- **Direct link** - Host path → container path
- **Not isolated** - Host e container acessam mesmo arquivo
- **Any location** - Pode montar de qualquer lugar do host

**Use case:** Development, shared config files

### tmpfs Mounts

- **In-memory** - Armazena em RAM, não em disco
- **Ephemeral** - Perdido quando container para
- **No persistence** - Não persiste no host nem no container

**Use case:** Sensitive data, caching, temporary files

### Named Pipes

- **Communication** - Host ↔ container IPC
- **Windows** - Comum para Docker Engine API

---

## 📊 Comparação

| Tipo | Persistência | Performance | Uso |
|------|--------------|-------------|-----|
| **Volume** | ✅ | Alta | Dados de produção |
| **Bind Mount** | ✅ | Média | Development |
| **tmpfs** | ❌ | Muito Alta | Temporário, sensível |

---

## 📝 Próximos Passos

1. Volumes: `/engine/volumes/`
2. Bind mounts: `/engine/bind-mounts/`
3. tmpfs mounts: `/engine/tmpfs/`
4. Storage drivers: `/engine/storage/drivers/`

---

## 💡 Insights Principais

1. **Volumes são preferidos para dados** - Gerenciados pelo Docker, isolados
2. **Bind mounts para development** - Edição em tempo real
3. **tmpfs para dados sensíveis** - Nunca toca disco
4. **Container layer is temporary** - Não confie para persistência
5. **Storage drivers são diferentes** - About image layers, not data

---

**Tempo de leitura:** ~10 minutos  
**Relevância:** ⭐⭐⭐⭐⭐ (Fundamental para Docker)