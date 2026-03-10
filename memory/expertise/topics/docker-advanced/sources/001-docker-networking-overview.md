# Docker Networking Overview

**Fonte:** https://docs.docker.com/engine/network/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. Network Drivers Disponíveis
| Driver | Descrição |
|--------|-----------|
| **bridge** | Driver padrão. Rede bridge para containers no mesmo host. |
| **host** | Remove isolamento de rede - container usa rede do host diretamente. |
| **none** | Isola completamente o container (sem rede). |
| **overlay** | Conecta múltiplos Docker daemons (Swarm). |
| **ipvlan** | Conecta containers a VLANs externas. |
| **macvlan** | Containers aparecem como dispositivos físicos na rede do host. |

### 2. Default Bridge vs User-Defined Networks
- **Default Bridge:** Containers não se comunicam por nome, apenas por IP
- **User-Defined Networks:** DNS automático permite comunicação por nome
- Boa prática: Usar redes user-defined para isolamento

### 3. Múltiplas Redes
- Containers podem ser conectados a múltiplas redes
- Útil para separar frontend (acesso externo) de backend (rede interna)
- Gateway priority controla rota padrão

### 4. Port Publishing
- Ports em bridge networks são acessíveis do host e containers na mesma rede
- `--publish` / `-p` para expor fora do host
- Port mapping para roteamento

### 5. IP Address e Hostname
- IPv4 habilitado por padrão, IPv6 com `--ipv6`
- Containers recebem IP de cada rede conectada
- Subnet allocation: explícita ou automática (default-address-pools)
- Gateway priority: `--network name=gwnet,gw-priority=1`

### 6. DNS Services
- Containers herdam DNS do host por padrão
- User-defined networks usam DNS embedded do Docker
- Flags: `--dns`, `--dns-search`, `--dns-opt`, `--hostname`
- Custom hosts via `/etc/hosts` não são herdados

### 7. Container Networks (Network Namespace Sharing)
- `--network container:<name|id>`: Compartilha stack de rede
- Flags não suportadas: `--hostname`, `--dns`, `--publish`, etc.
- Útil para debug e sidecar patterns

## Comandos Principais

```bash
# Criar rede user-defined
docker network create -d bridge my-net

# Rodar container em rede específica
docker run --network=my-net -it busybox

# Conectar container em múltiplas redes
docker network connect anet2 myctr

# Criar rede IPv6
docker network create --ipv6 --ipv4=false v6net

# Especificar subnet
docker network create --subnet 192.0.2.0/24 mynet
```

## Boas Práticas

1. Usar user-defined networks ao invés de default bridge
2. Separar redes por função (frontend/backend/database)
3. Usar gateway priority quando múltiplas redes precisam de rota específica
4. Configurar DNS explicitamente para ambientes específicos
5. Documentar configurações de rede no docker-compose

## Aplicações Práticas

### Arquitetura Multi-Tier
```
Frontend (bridge com acesso externo)
    ↓
Backend (rede interna --internal)
    ↓
Database (rede isolada)
```

### Sidecar Pattern
```bash
# Main container
docker run -d --name app myapp

# Sidecar compartilhando rede
docker run -d --network container:app monitoring-sidecar
```

---

## Próximos Passos
- [ ] Estudar overlay networking para Swarm
- [ ] Estudar ipvlan e macvlan em detalhes
- [ ] Praticar container network sharing