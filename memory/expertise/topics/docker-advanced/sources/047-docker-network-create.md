# Docker Network Create - CLI Reference

**Fonte:** https://docs.docker.com/reference/cli/docker/network/create/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Uso

```bash
docker network create [OPTIONS] NETWORK
```

---

## Opções

| Opção | Default | Descrição |
|-------|---------|-----------|
| `--attachable` | - | Permitir attach manual (API 1.25+) |
| `--aux-address` | - | Endereços IPv4/IPv6 auxiliares |
| `--config-from` | - | Copiar configuração de outra rede (API 1.30+) |
| `--config-only` | - | Criar rede apenas de configuração (API 1.30+) |
| `-d`, `--driver` | `bridge` | Driver de rede (bridge, overlay, etc.) |
| `--gateway` | - | Gateway IPv4/IPv6 |
| `--ingress` | - | Criar rede routing-mesh (Swarm) |
| `--internal` | - | Restringir acesso externo |
| `--ip-range` | - | Alocar IPs de sub-range |
| `--ipam-driver` | - | Driver de IPAM |
| `--ipam-opt` | - | Opções do IPAM driver |
| `--ipv4` | `true` | Habilitar IPv4 |
| `--ipv6` | - | Habilitar IPv6 |
| `--label` | - | Metadados |
| `-o`, `--opt` | - | Opções do driver |
| `--scope` | - | Escopo da rede (local, swarm) |
| `--subnet` | - | Sub-rede em formato CIDR |

---

## Drivers de Rede

### Bridge (Default)
```bash
docker network create -d bridge my-bridge-network
```
- Rede isolada em um único host
- Containers se comunicam por nome
- Default para containers

### Overlay (Swarm)
```bash
docker network create --scope=swarm --attachable -d overlay my-multihost-network
```
- Rede multi-host
- Requer Swarm mode
- `--attachable` permite containers manuais

---

## Sub-redes e Gateways

### Bridge (Subnet Única)
```bash
docker network create \
  --driver=bridge \
  --subnet=192.168.0.0/16 \
  br0
```

### Com Gateway e IP Range
```bash
docker network create \
  --driver=bridge \
  --subnet=172.28.0.0/16 \
  --ip-range=172.28.5.0/24 \
  --gateway=172.28.5.254 \
  br0
```

### Overlay (Múltiplas Subnets)
```bash
docker network create -d overlay \
  --subnet=192.168.10.0/25 \
  --subnet=192.168.20.0/25 \
  --gateway=192.168.10.100 \
  --gateway=192.168.20.100 \
  my-multihost-network
```

---

## Opções do Bridge Driver

| Opção | Daemon Option | Descrição |
|-------|---------------|-----------|
| `com.docker.network.bridge.name` | - | Nome do Linux bridge |
| `com.docker.network.bridge.enable_ip_masquerade` | `--ip-masq` | IP masquerading |
| `com.docker.network.bridge.enable_icc` | `--icc` | Inter-container connectivity |
| `com.docker.network.bridge.host_binding_ipv4` | `--ip` | IP default para port binding |
| `com.docker.network.driver.mtu` | `--mtu` | MTU da rede |
| `com.docker.network.container_iface_prefix` | - | Prefixo das interfaces |

### Exemplo com Opções
```bash
docker network create \
  -o "com.docker.network.bridge.host_binding_ipv4"="172.19.0.1" \
  simple-network
```

---

## Internal Mode (--internal)

Containers em uma rede internal podem se comunicar entre si, mas **não com outras redes ou internet**.

### Comportamento
- Sem rota default
- Firewall drop para outras redes
- Pode comunicar com gateway IP (host services)
- Host pode comunicar com qualquer container IP

### Overlay Internal
```bash
docker network create -d overlay --internal my-internal-network
```
- Por default, overlay conecta bridge para external connectivity
- `--internal` remove essa bridge

---

## Ingress Mode (--ingress)

Cria rede para routing-mesh no Swarm cluster.

```bash
docker network create -d overlay \
  --subnet=10.11.0.0/16 \
  --ingress \
  --opt com.docker.network.driver.mtu=9216 \
  --opt encrypted=true \
  my-ingress-network
```

### Restrições
- Apenas uma rede ingress
- Não pode usar `--attachable`
- Removível apenas se sem serviços dependentes

---

## Swarm Networks com Local Scope Drivers

```bash
docker network create -d bridge \
  --scope swarm \
  --attachable \
  swarm-network
```

### Config-Only Networks (Macvlan)
```bash
# Node 1
docker network create --config-only \
  --subnet 192.168.100.0/24 \
  --gateway 192.168.100.115 \
  mv-config

# Node 2
docker network create --config-only \
  --subnet 192.168.200.0/24 \
  --gateway 192.168.200.202 \
  mv-config

# Create swarm network (any node)
docker network create -d macvlan \
  --scope swarm \
  --config-from mv-config \
  --attachable \
  swarm-network
```

---

## Limitações de Overlay

- **Use /24 blocks** (256 IPs max) para VIP endpoint-mode
- Para mais IPs, use:
  - DNSRR endpoint mode + external load balancer
  - Múltiplas redes overlay menores

---

## Conceitos Aprendidos

1. **Bridge vs Overlay** - Local vs multi-host
2. **Internal mode** - Isolamento total do externo
3. **Ingress network** - Routing mesh para Swarm
4. **Config-only networks** - Configuração node-specific para drivers locais
5. **Attachable** - Permite containers manuais em overlay

---

## Aplicações Práticas

1. **Isolamento** - Redes internas para serviços sensíveis
2. **Multi-host** - Overlay para Swarm/Kubernetes
3. **DMZ** - Rede bridge para serviços expostos
4. **Testing** - Redes isoladas para testes
5. **Routing mesh** - Ingress para load balancing

---

## Referências Cruzadas

- Ver: `046-docker-network-commands.md`
- Ver: `001-docker-networking-overview.md`
- Ver: `026-docker-compose-networks.md`
- Relacionado: Swarm networking, macvlan, IPAM