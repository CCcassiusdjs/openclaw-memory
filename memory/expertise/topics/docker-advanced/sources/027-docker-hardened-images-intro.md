# Docker Hardened Images - Introdução

**Fonte:** https://www.docker.com/blog/introducing-docker-hardened-images/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## O que são Docker Hardened Images (DHI)

Imagens de container seguras por padrão, construídas especificamente para ambientes de produção modernos.

### Características Principais

1. **Attack Surface Reduzido**
   - Até 95% menor que imagens tradicionais
   - Filosofia distroless: sem shells, package managers, ferramentas de debug
   - Apenas dependências de runtime essenciais

2. **CVEs Próximo de Zero**
   - Mantidas continuamente pelo Docker
   - Patch automático de vulnerabilidades
   - SLA: Critical e High patched em 7 dias

3. **Compatibilidade**
   - Suporta Alpine e Debian
   - Migração simples: trocar uma linha no Dockerfile
   - Integração com ferramentas existentes

4. **Supply Chain Security**
   - SLSA Build Level 3 compliant
   - Attestations de integridade
   - SBOM support

---

## Problemas que Resolve

### 1. Integridade
- "Como sabemos que cada componente é o que diz ser?"
- Imagens assinadas e verificadas

### 2. Attack Surface
- Imagens gerais (Ubuntu, Alpine) acumulam pacotes desnecessários
- DHI elimina componentes não essenciais
- 98%+ menos pacotes em alguns casos

### 3. Operational Overhead
- Menos CVEs para remediar
- Patching automático
- Reduz carga de security teams

---

## Migração

### Exemplo Simples
```dockerfile
# Antes
FROM node:18

# Depois (Hardened)
FROM docker/hardened-node:18
```

### Customizações Suportadas
- Certificados
- Pacotes adicionais
- Scripts
- Configurações

---

## Parcerias de Integração

- Microsoft, NGINX, Sonatype, GitLab
- Wiz, Grype, Neo4j, JFrog
- Sysdig, Cloudsmith
- Integração com scanners, registries, CI/CD

---

## Validação Interna

Docker testou internamente com imagem Node hardened:
- **Vulnerabilidades:** Zero (de muitas)
- **Pacotes:** Redução de 98%+
- **Attack Surface:** Dramaticamente menor

---

## Conceitos Aprendidos

1. **Hardened ≠ Minimal** - Não é apenas reduzir tamanho, é segurança desde o design
2. **Distroless philosophy** - Remover shells, package managers, debug tools
3. **SLA de patching** - 7 dias para Critical/High
4. **SLSA Build Level 3** - Supply chain security framework
5. **Migration path** - Trocar uma linha no Dockerfile

---

## Comparação

| Aspecto | Imagem Tradicional | Hardened Image |
|---------|-------------------|----------------|
| Tamanho | Completa | Até 95% menor |
| CVEs | Variáveis | Próximo de zero |
| Pacotes | Todos | Apenas essenciais |
| Shell | Sim | Não (distroless) |
| Package Manager | Sim | Não |
| Patching | Manual | Automático |
| Attestations | Opcional | Built-in |

---

## Aplicações Práticas

1. **Produção** - Imagens de runtime otimizadas
2. **Compliance** - SLSA Level 3 para auditoria
3. **Supply Chain Security** - Attestations e SBOM
4. **Microserviços** - Base segura para serviços
5. **CI/CD** - Menos vulnerabilidades para remediar

---

## Referências Cruzadas

- Ver: `003-docker-security-overview.md`
- Ver: `004-owasp-docker-security-cheat-sheet.md`
- Ver: `025-docker-image-security-best-practices.md`
- Relacionado: Distroless images, minimal containers