# Docker Image Security Best Practices: SBOM, Non-Root, Provenance

**Fonte:** https://bell-sw.com/blog/docker-image-security-best-practices-for-production/
**Data:** 2026-03-11
**Status:** Lido

---

## Resumo

11 práticas comprovadas de segurança para imagens Docker, focando em reduzir superfície de ataque, garantir integridade e fortalecer o supply chain.

## 11 Práticas de Segurança

### 1. Keep Container Images Lean
- Minimizar componentes no caminho de execução direta
- Usar distros minimalistas, distroless, ou scratch
- **Multi-stage builds** para transferir apenas o necessário

**Exemplo Java:**
```dockerfile
FROM bellsoft/liberica-runtime-container:jdk-25-musl AS builder
WORKDIR /app
ADD my-java-app /app/my-java-app
RUN cd my-java-app && ./mvnw package

FROM bellsoft/liberica-runtime-container:jre-25-musl
WORKDIR /app
COPY --from=builder /app/my-java-app/target/*.jar app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**Exemplo Go (distroless):**
```dockerfile
FROM golang:1.24.4 AS builder
WORKDIR /app
COPY go.mod main.go ./
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -o /hello

FROM gcr.io/distroless/static-debian12
WORKDIR /
COPY --from=builder /hello /hello
ENTRYPOINT ["/hello"]
```

### 2. No Package Manager in Production
- Package manager mata imutabilidade
- SBOM, assinatura e provenance perdem valor se pacotes são instalados em runtime
- Attackers podem instalar ferramentas maliciosas
- Optar por slim final base image sem package manager

### 3. Run as Non-root with Minimum Privileges
- Containers root dão acesso a nível de host
- Criar usuário não-privilegiado:
```dockerfile
USER 1234:1234
# OU
RUN groupadd -r myuser && useradd -r -g myuser myuser
USER myuser
```
- Nunca usar `--privileged` desnecessariamente
- Usar capability dropping:
```bash
docker run --cap-drop all --cap-add <required-privilege>
```

### 4. Don't Tweak Containers in Production
- Container deve corresponder à imagem
- Sem patches, tweaks ou fixes em produção
- Rebuild e redeploy para qualquer mudança

**Benefícios:**
- Integridade de runtime (SBOMs/signatures refletem o que roda)
- Rollback mais fácil
- Menos oportunidades de tampering

**Flags úteis:**
```bash
--tmpfs <mount-path>           # Dados temporários fora do container
--security-opt no-new-privileges  # Previne escalação de privilégios
--read-only                    # Filesystem somente leitura
```

### 5. Deterministic Container Images
- **Same input → exact same bytes**
- Detecta tampering e mudanças de dependência
- Elimina TOCTOU vulnerability

**Como:**
- Pin tudo: toolchain, build system, OS version
- **Pin base image by digest, not tag:**
```dockerfile
#base image version: bellsoft/liberica-runtime-container:jre-25_37-slim-musl
bellsoft/liberica-runtime-container:sha256:5646cf896dafe95def30420defa8077fc8ee71ef5578e2c018c2572aae0541e2
```

### 6. Implement SBOM and Provenance

**SBOM (Software Bill of Materials):**
- Lista de componentes, bibliotecas, módulos
- Nome, versão, licença, identificadores únicos
- Previne vulnerabilidades ocultas
- Acelera remediação de CVEs

**Gerar SBOM:**
```bash
syft $IMG --output cyclonedx-json=oci-sbom-syft.json
```

**Provenance:**
- Prova de onde a imagem veio
- Metadata: builder identity, source repo commit, build steps
- Framework: SLSA (Supply-chain Levels for Software Artifacts)

**Attestation:**
```bash
cosign attest --predicate oci-sbom-syft.json --type cyclonedx $IMG
```

**Workflow:**
1. Gerar SBOM + provenance para cada imagem
2. Armazenar como attestations tied to image digest
3. Assinar imagens
4. No deploy, verificar assinatura e provenance

**Decisões:**
- Accept: imagem verificada
- Quarantine: assinatura não verificada, SBOM stale, vulnerabilidades médias
- Reject: unsigned, wrong identity, missing attestation, critical vulnerabilities

### 7. No DIY for Base Images
- Base images random introduzem riscos:
  - CVE blind spots
  - Sem provenance/trust
  - Sem vendor-backed SLA
  - Sem compliance com requisitos legais

**Usar imagens de vendors confiáveis, verificar:**
```bash
cosign verify \
  --certificate-identity "$EXPECTED_IDENTITY" \
  --certificate-oidc-issuer "$EXPECTED_ISSUER" \
  <chosen-image>@sha256:<PINNED_DIGEST>
```

### 8. Use LTS Versions + Update Regularly

**LTS Benefits:**
- Suporte por anos
- Patches de segurança backported
- Menos vulnerabilidades que non-LTS

**Ciclos de Suporte:**
- Node.js LTS: 2.5 anos
- Java LTS: depende do vendor
- Ubuntu LTS: 5 anos
- Alpine: ~2 anos
- Alpaquita LTS: 4 anos

**Monitorar updates:**
- Dependabot, Renovate
- Rebuild, rescan, resign após updates

### 9. No Secrets in Containers
- Container image = distribution artifact
- Tudo pode ser cached, copied, extracted
- **Secrets na imagem = security risk grave**
- Usar soluções dedicadas (Vault, secrets managers)

### 10. Use Security Scanners
- Escanear imagens regularmente
- Integrar no CI/CD
- Ferramentas: Trivy, Grype, Snyk, Docker Scout

### 11. Implement Host Hardening
- Container security não basta
- Host também deve ser endurecido
- Kernel hardening, network policies, runtime security

## Conceitos-Chave

| Conceito | Descrição |
|----------|-----------|
| **SBOM** | Software Bill of Materials - inventário de componentes |
| **Provenance** | Prova de origem do artifact |
| **Attestation** | Statement criptograficamente assinado sobre propriedades |
| **SLSA** | Supply-chain Levels for Software Artifacts |
| **TOCTOU** | Time-of-Check to Time-of-Use vulnerability |
| **Distroless** | Imagens sem shell, package manager, ferramentas de debug |

## Conclusão

Segurança de imagens Docker é uma combinação de:
1. Imagens minimalistas e deterministicas
2. Runtime seguro (non-root, capabilities limitadas)
3. Supply chain verificável (SBOM, provenance, signatures)
4. Processos de update e monitoramento

---
*Fonte parcialmente truncada - conteúdo principal capturado*