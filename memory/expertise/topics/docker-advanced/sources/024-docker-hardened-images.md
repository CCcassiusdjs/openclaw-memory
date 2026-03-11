# Docker Hardened Images

**Fonte:** https://www.docker.com/blog/introducing-docker-hardened-images/
**Data:** 2026-03-11
**Status:** Lido

---

## Resumo

Docker Hardened Images (DHI) são imagens de container purpose-built para ambientes de produção modernos, com segurança por design.

## Conceitos-Chave

### 1. Redução de Superfície de Ataque
- Até **95% menores** que imagens tradicionais
- Filosofia distroless: removem shells, package managers, ferramentas de debug
- Apenas dependências de runtime essenciais

### 2. Características Principais
- **Curadas e mantidas pelo Docker**
- **Near-zero CVEs conhecidos**
- Suportam distros populares (Alpine, Debian)
- Integração com ferramentas de segurança existentes

### 3. SLA de Patching
- Critical e High CVEs: **patched within 7 days**
- Rebuilds automáticos com testes extensivos
- SLSA Build Level 3–compliant build system

### 4. Migração Simples
```dockerfile
# Antes
FROM node:20

# Depois (Hardened)
FROM docker/hardened-node:20
```

### 5. Parceiros de Integração
- Microsoft, NGINX, Sonatype, GitLab, Wiz, Grype, Neo4j, JFrog, Sysdig, Cloudsmith

## Casos de Uso

- Ambientes de produção com requisitos de segurança elevados
- Compliance com regulamentações de supply chain
- Redução de overhead de patching manual

## Benefícios Medidos

Em testes internos com hardened Node image:
- Vulnerabilidades: **zero**
- Redução de pacotes: **>98%**
- Menor attack surface
- Operação simplificada

## Conclusão

Docker Hardened Images são a evolução natural para produção - não apenas imagens slim, mas imagens construídas do zero com segurança, eficiência e usabilidade real em mente.