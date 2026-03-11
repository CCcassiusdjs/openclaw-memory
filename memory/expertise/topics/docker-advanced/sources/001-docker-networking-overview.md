# Docker Networking Overview

**Fonte:** Docker Docs  
**URL:** https://docs.docker.com/engine/network/  
**Tipo:** Documentação Oficial  
**Status:** completed

---

## 📋 Resumo Executivo

Container networking permite containers conectarem e comunicarem entre si e com serviços não-Docker. Containers têm networking habilitado por padrão e podem fazer conexões de saída.

---

## 🔑 Conceitos-Chave

### Network Drivers

| Driver | Descrição |
|--------|-----------|
| **bridge** | Driver padrão. Isola containers na mesma rede. |
| **host** | Remove isolamento de rede entre container e host. |
| **none** | Isola completamente o container. |
| **overlay** | Conecta múltiplos Docker daemons (Swarm). |
| **ipvlan** | Conecta containers a VLANs externas. |
| **macvlan** | Containers aparecem como dispositivos na rede do host. |

### User-Defined Networks

- Containers podem se comunicar por **IP** ou **nome**
- Isolamento entre grupos de containers
- Exemplo: `docker network create -d bridge my-net`

### Multiple Networks

- Containers podem conectar a múltiplas redes
- Útil para arquitetura frontend/backend
- `--internal` para redes sem acesso externo
- `gw-priority` para escolher gateway padrão

---

## 📐 IP Address Management

### IPv4/IPv6 Allocation

- IPv4 habilitado por padrão
- IPv6: `--ipv6`
- Pode desabilitar IPv4: `--ipv4=false`

### Subnet Allocation

**Explicit:**
```bash
docker network create --subnet 192.0.2.0/24 mynet
```

**Automatic:**
- Docker aloca de default address pools
- Configurável em `/etc/docker/daemon.json`
- Default: `172.17.0.0/16`, `172.18.0.0/16`, etc.

### Custom Pools

```json
{
  "default-address-pools": [
    {"base": "172.17.0.0/16", "size": 24}
  ]
}
```

---

## 🔧 DNS Services

| Flag | Descrição |
|------|-----------|
| `--dns` | IP do servidor DNS |
| `--dns-search` | Domínio de busca |
| `--dns-opt` | Opções DNS |
| `--hostname` | Hostname do container |

### DNS Behavior

- Containers herdam DNS do host por padrão
- Custom networks usam Docker embedded DNS server
- Embedded DNS encaminha consultas externas

---

## 🔗 Container Networks

### Network Sharing

```bash
docker run --network container:<name|id> ...
```

- Compartilha stack de rede com outro container
- Útil para debugging
- Flags não suportadas: `--hostname`, `--dns`, `--publish`

---

## 📝 Published Ports

- Ports em bridge networks: acessíveis do host
- `--publish` ou `-p` para expor externamente
- Containers em outras redes: não acessíveis por padrão

---

## 💡 Insights Principais

1. **User-defined networks são recomendadas** - DNS por nome, isolamento
2. **Multiple networks = flexibilidade** - Frontend/backend separation
3. **gw-priority controla gateway** - Importante para routing
4. **IPv6 suportado** - Mas precisa habilitar explicitamente
5. **Container network sharing** - Debugging e sidecars

---

**Tempo de leitura:** ~15 minutos  
**Relevância:** ⭐⭐⭐⭐⭐ (Fundamental para Docker)