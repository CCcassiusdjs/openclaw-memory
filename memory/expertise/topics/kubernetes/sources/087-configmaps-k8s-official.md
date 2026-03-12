# ConfigMaps - Kubernetes Official Documentation

**Fonte:** Kubernetes.io - https://kubernetes.io/docs/concepts/configuration/configmap/
**Data:** Janeiro 2026
**Tópico:** ConfigMaps, Configuration Management, Environment Variables, Volumes
**Status:** Lido

---

## Resumo Executivo

Documentação oficial de ConfigMaps, cobrindo criação, consumo (env vars, volumes, comandos), imutabilidade e diferenças em relação a Secrets.

---

## O que são ConfigMaps

### Definição
- Objeto API para armazenar dados não-confidenciais
- Pares chave-valor
- Permite separar configuração do código da aplicação
- Portabilidade entre ambientes

### Atenção
- **ConfigMaps não oferecem segredos ou criptografia**
- Dados confidenciais devem usar Secrets
- Limite: **1 MiB** por ConfigMap

---

## Motivação

### Separação de Configuração
- Desenvolvimento: `DATABASE_HOST=localhost`
- Produção: `DATABASE_HOST=prod-db-service`
- Mesma imagem, configuração diferente

### 12-Factor App
- Config em environment variables
- Imagem portável
- Separação de código e configuração

---

## Objeto ConfigMap

### Estrutura
- Campos: `data` e `binaryData`
- `data`: strings UTF-8
- `binaryData`: dados binários (base64-encoded)
- Nome: DNS subdomain name válido
- Chaves: alphanumeric, `-`, `_`, `.`

### Exemplo Básico
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: game-demo
data:
  # property-like keys
  player_initial_lives: "3"
  ui_properties_file_name: "user-interface.properties"
  
  # file-like keys
  game.properties: |
    enemy.types=aliens,monsters
    player.maximum-lives=5
  user-interface.properties: |
    color.good=purple
    color.bad=yellow
    allow.textmode=true
```

---

## Consumindo ConfigMaps

### Quatro Métodos

1. **Command line args** dentro do container
2. **Environment variables** para o container
3. **Volume mount** como arquivo read-only
4. **Kubernetes API** no código do Pod

### Método 1: Environment Variables
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-env-pod
spec:
  containers:
  - name: demo
    image: alpine
    command: ["sleep", "3600"]
    env:
    - name: PLAYER_INITIAL_LIVES
      valueFrom:
        configMapKeyRef:
          name: game-demo
          key: player_initial_lives
    - name: UI_PROPERTIES_FILE_NAME
      valueFrom:
        configMapKeyRef:
          name: game-demo
          key: ui_properties_file_name
```

### Método 2: All Keys as Env Vars
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: env-configmap
spec:
  containers:
  - name: app
    command: ["/bin/sh", "-c", "printenv"]
    image: busybox:latest
    envFrom:
    - configMapRef:
        name: myconfigmap
```

### Método 3: Volume Mount
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-volume-pod
spec:
  containers:
  - name: demo
    image: alpine
    command: ["sleep", "3600"]
    volumeMounts:
    - name: config
      mountPath: "/config"
      readOnly: true
  volumes:
  - name: config
    configMap:
      name: game-demo
      items:
      - key: "game.properties"
        path: "game.properties"
      - key: "user-interface.properties"
        path: "user-interface.properties"
```

### Método 4: Kubernetes API
- Código dentro do Pod lê ConfigMap diretamente
- Permite subscrição para updates
- Permite acessar ConfigMaps em outros namespaces

---

## Atualizações de ConfigMap

### Volume Mounts
- Atualizações propagam automaticamente
- Kubelet usa cache local
- Delay = sync period + cache propagation

### Environment Variables
- **NÃO atualizam automaticamente**
- Requer restart do Pod

### subPath
- Containers usando subPath NÃO recebem updates

---

## Immutable ConfigMaps

### Feature State
- Kubernetes v1.21+ (stable)

### Benefícios
- Protege contra updates acidentais
- Melhora performance (reduz load no API server)
- Fecha watches para ConfigMaps imutáveis

### Configuração
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: immutable-config
data:
  key1: value1
  key2: value2
immutable: true
```

### Limitações
- Não pode ser revertido
- Não pode mutar data ou binaryData
- Deletar e recriar é a única opção
- Pods existentes mantêm referência ao deletado

---

## Boas Práticas

### Naming
- Nomes DNS subdomain válidos
- Chaves: alphanumeric, `-`, `_`, `.`

### Size Limits
- Máximo 1 MiB por ConfigMap
- Para configurações maiores, usar volumes ou database externo

### Security
- ConfigMaps não oferecem segurança
- Dados sensíveis devem usar Secrets

### Immutability
- Para configs estáveis, usar `immutable: true`
- Performance + segurança

---

## ConfigMaps vs Secrets

| Aspecto | ConfigMap | Secret |
|---------|-----------|--------|
| **Dados** | Não-confidenciais | Confidenciais |
| **Encoding** | Plain text | Base64 |
| **Segurança** | Nenhuma | Encryption at Rest opcional |
| **Limite** | 1 MiB | 1 MiB |
| **Uso** | Config de app | Credenciais, tokens |

---

## Casos de Uso

### Application Config
```yaml
# Config para diferentes ambientes
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database_url: "postgres://prod-db:5432"
  log_level: "info"
  feature_flags: |
    new_ui=true
    dark_mode=false
```

### Feature Flags
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: feature-flags
data:
  NEW_FEATURE: "enabled"
  EXPERIMENTAL: "disabled"
```

### Environment-Specific Config
```yaml
# dev-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DEBUG: "true"
  LOG_LEVEL: "debug"

---
# prod-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DEBUG: "false"
  LOG_LEVEL: "error"
```

---

## Insights para Kubernetes

1. **ConfigMaps para config não-sensível**: Separar código de configuração
2. **Secrets para dados sensíveis**: ConfigMaps não oferecem segurança
3. **Limite de 1 MiB**: Para configs maiores, usar volumes externos
4. **Immutable melhora performance**: Fechar watches reduz load
5. **Updates automáticos só em volumes**: Env vars requerem restart

---

## Palavras-Chave
`configmaps` `configuration` `environment-variables` `volumes` `immutable` `kubernetes` `12-factor-app`