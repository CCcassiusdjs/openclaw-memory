# Docker Engine Security

**Fonte:** Docker Docs  
**URL:** https://docs.docker.com/engine/security/  
**Tipo:** Documentação Oficial  
**Status:** completed

---

## 📋 Resumo Executivo

Quatro áreas principais de segurança em Docker:
1. Segurança intrínseca do kernel (namespaces, cgroups)
2. Superfície de ataque do Docker daemon
3. Configuração de containers
4. Hardening features do kernel

---

## 🔑 Conceitos-Chave

### Kernel Namespaces

- Containers isolados por namespaces
- Processos em um container não veem outros containers
- Network stack próprio por container
- Código maduro desde kernel 2.6.26 (2008)

### Control Groups (cgroups)

- Resource accounting e limiting
- Garantem share justo de CPU, memória, disk I/O
- Previnem DoS por exaustão de recursos
- Código desde kernel 2.6.24 (2006)

### Docker Daemon Attack Surface

- Daemon roda como root por padrão (Rootless mode disponível)
- Apenas usuários confiáveis devem controlar o daemon
- REST API usa Unix socket (não TCP)
- TLS obrigatório se expor API
- Imagens são extraídas em chroot subprocess
- Checksums criptográficos para imagens

---

## 🛡️ Linux Kernel Capabilities

### Capabilities System

- Transforma binário root/non-root em fine-grained access control
- Containers rodam com set restrito de capabilities
- "root" em container tem menos privilégios que root real

### Capabilities Dropped by Default

Docker remove todas exceto as necessárias (allowlist approach):
- `net_bind_service` - Bind port < 1024
- Outras capabilities mantidas conforme necessário

### Operations Denied by Default

- Mount operations
- Raw sockets (previne spoofing)
- Criar device nodes
- Mudar owner de arquivos
- Alterar atributos
- Module loading

---

## 🔒 Docker Content Trust

- Configurar daemon para rodar apenas imagens assinadas
- Trustpinning em `daemon.json`
- Apenas repositórios com chave root especificada

---

## 🛠️ Outros Recursos de Segurança

### Kernel Hardening

- GRSEC e PAX - Safety checks compile-time e run-time
- AppArmor - Templates de segurança para Docker
- SELinux - Policies para Docker (Red Hat)

### User Namespaces

- root no container mapeado para non-root no host
- Mitiga risco de container breakout
- Disponível mas não habilitado por padrão

---

## 💡 Insights Principais

1. **Containers são seguros por default** - Mas adicionar camadas melhora
2. **Capabilities são allowlist** - Apenas necessárias são mantidas
3. **Daemon attack surface** - Cuidado com API exposure
4. **User Namespaces importantes** - Mapeia root para non-root
5. **Hardening opcional** - AppArmor, SELinux, GRSEC

---

**Tempo de leitura:** ~20 minutos  
**Relevância:** ⭐⭐⭐⭐⭐ (Fundamental para segurança Docker)