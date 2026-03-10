# Docker Compose Networks

**Fonte:** https://docs.docker.com/reference/compose-file/networks/
**Tipo:** Documentação Oficial
**Lido em:** 2026-03-10
**Status:** completed

---

## Conceitos-Chave

### 1. Network Default
- Compose cria uma rede default para todos os serviços
- Containers são discoverable pelo nome do serviço
- DNS automático funciona dentro da rede

### 2. Rede Customizada

```yaml
services:
  frontend:
    image: example/webapp
    networks:
      - front-tier
      - back-tier

networks:
  front-tier:
  back-tier:
```

### 3. Atributos de Networks

| Atributo | Descrição |
|----------|-----------|
| `attachable` | Permite containers standalone conectarem |
| `driver` | Driver de rede (bridge, overlay, etc.) |
| `driver_opts` | Opções específicas do driver |
| `enable_ipv4` | Habilita IPv4 |
| `enable_ipv6` | Habilita IPv6 |
| `external` | Rede gerenciada externamente |
| `ipam` | Configuração IPAM customizada |
| `internal` | Rede isolada (sem acesso externo) |
| `labels` | Metadados |
| `name` | Nome customizado |

---

## Exemplos

### Rede com Driver Customizado
```yaml
networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
  backend:
    driver: custom-driver
```

### Rede Overlay Attachable
```yaml
networks:
  mynet1:
    driver: overlay
    attachable: true
```

### Rede Externa
```yaml
services:
  proxy:
    image: example/proxy
    networks:
      - outside
      - default

networks:
  outside:
    external: true
```

### Rede IPv6
```yaml
networks:
  ip6net:
    enable_ipv4: false
    enable_ipv6: true
```

### IPAM Customizado
```yaml
networks:
  mynet1:
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          ip_range: 172.28.5.0/24
          gateway: 172.28.5.254
          aux_addresses:
            host1: 172.28.1.5
            host2: 172.28.1.6
```

### Rede Interna (Isolada)
```yaml
networks:
  internal_net:
    internal: true
```

---

## Boas Práticas

1. **Separar redes por função** - frontend, backend, database
2. **Usar internal para backend** - Isola do mundo externo
3. **Nomear redes** - Facilita identificação
4. **Usar redes externas** - Para compartilhar entre projetos
5. **Configurar IPAM** - Para ambientes específicos

## Próximos Passos
- [ ] Estudar overlay networking
- [ ] Praticar com múltiplas redes
- [ ] Configurar rede isolada