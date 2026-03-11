# Docker Compose Networks - Documentação Oficial

**Fonte:** https://docs.docker.com/reference/compose-file/networks/
**Prioridade:** Alta
**Lido em:** 2026-03-11

---

## Conceitos-Chave

### 1. Rede Padrão
- Compose cria automaticamente uma rede `default` quando nenhuma é especificada
- Serviços sem declaração explícita de redes são conectados à rede default
- A rede default pode ser customizada com declaração explícita

### 2. Sintaxe de Networks
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

### 3. Isolamento de Serviços
- Serviços em redes diferentes não podem se comunicar diretamente
- Útil para separar frontend de backend de banco de dados

### 4. Atributos Importantes

#### `attachable`
```yaml
networks:
  mynet1:
    driver: overlay
    attachable: true  # containers standalone podem se conectar
```

#### `driver`
- Especifica driver de rede (bridge, overlay, macvlan, etc.)
- Retorna erro se driver não disponível na plataforma

#### `driver_opts`
```yaml
networks:
  frontend:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
```

#### `enable_ipv4` / `enable_ipv6`
- Controla atribuição de endereços IPv4/IPv6

#### `external`
- Rede gerenciada externamente ao Compose
- Compose não tenta criar, apenas conecta
- Útil para redes pré-existentes

#### `ipam` (IP Address Management)
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
```

#### `internal`
- Cria rede isolada externamente (sem acesso à internet)

#### `labels`
- Metadados para a rede (reverse-DNS recomendado)

#### `name`
- Nome customizado para a rede (não scoped pelo projeto)

---

## Padrões Recomendados

### Separação de Camadas
```yaml
services:
  proxy:
    networks:
      - frontend
  app:
    networks:
      - frontend
      - backend
  db:
    networks:
      - backend

networks:
  frontend:
  backend:
```
- proxy não pode acessar db diretamente
- app é o único ponto de comunicação entre camadas

### Rede Externa para Gateway
```yaml
services:
  proxy:
    networks:
      - outside
      - default

networks:
  outside:
    external: true
```

### IPv6-Only Network
```yaml
networks:
  ip6net:
    enable_ipv4: false
    enable_ipv6: true
```

---

## Conceitos Aprendidos

1. **Rede default implícita** - Compose cria automaticamente
2. **Isolamento por redes** - Serviços só comunicam se compartilham rede
3. **IPAM customizado** - Controle fino de sub-redes e endereços
4. **Redes externas** - Integração com infraestrutura existente
5. **Redes attachable** - Containers standalone podem conectar (overlay)
6. **Redes internal** - Isolamento total do mundo externo

---

## Aplicações Práticas

1. **Microserviços** - Isolar serviços por domínio
2. **Ambientes multi-tenant** - Redes separadas por cliente
3. **Segurança** - Backend sem acesso externo direto
4. **Integração** - Conectar a redes pré-existentes
5. **Debugging** - Containers standalone na rede do app

---

## Referências Cruzadas

- Ver: `001-docker-networking-overview.md`
- Ver: `019-docker-compose-networks.md`
- Relacionado: Docker Network Drivers (bridge, overlay, macvlan)