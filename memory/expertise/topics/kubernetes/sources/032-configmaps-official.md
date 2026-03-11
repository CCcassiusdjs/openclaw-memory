# Kubernetes ConfigMaps (Official Docs)

**Fonte:** https://kubernetes.io/docs/concepts/configuration/configmap/
**Tipo:** Official Documentation
**Prioridade:** Alta
**Data:** 2026-03-11

## Resumo Executivo

ConfigMaps armazenam dados não-confidenciais em key-value pairs, permitindo separar configuração de código de aplicação.

---

## O que é ConfigMap?

### Definição
- API object para armazenar configuração
- Key-value pairs (strings ou binary data)
- Decouple environment-specific config de container images
- Máximo 1 MiB de dados

### Vantagens
- Portabilidade de container images
- Configuração por ambiente
- Hot reload (em volumes)
- Imutável com `immutable: true`

---

## Cuidado

⚠️ **ConfigMaps NÃO fornecem secrecy ou encryption.**
- Use Secrets para dados confidenciais
- Use ferramentas terceiras para dados privados

---

## Criando ConfigMaps

### Diretamente
```bash
kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2
```

### De arquivo
```bash
kubectl create configmap my-config --from-file=path/to/file.properties
```

### De diretório
```bash
kubectl create configmap my-config --from-file=path/to/directory
```

### YAML
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
```

---

## Consumindo ConfigMaps

### 1. Environment Variables
```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: demo
    image: alpine
    env:
    - name: PLAYER_INITIAL_LIVES
      valueFrom:
        configMapKeyRef:
          name: game-demo
          key: player_initial_lives
```

### 2. Environment Variables (All Keys)
```yaml
spec:
  containers:
  - name: demo
    image: alpine
    envFrom:
    - configMapRef:
        name: game-demo
```

### 3. Command Line Arguments
```yaml
spec:
  containers:
  - name: demo
    image: alpine
    command: ["./start", "$(PLAYER_LIVES)"]
    env:
    - name: PLAYER_LIVES
      valueFrom:
        configMapKeyRef:
          name: game-demo
          key: player_initial_lives
```

### 4. Volume Mount (as Files)
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: config
      mountPath: "/etc/config"
      readOnly: true
  volumes:
  - name: config
    configMap:
      name: myconfigmap
      items:
      - key: "game.properties"
        path: "game.properties"
```

---

## Immutable ConfigMaps

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  key: value
immutable: true
```

### Benefícios
- Protege contra updates acidentais
- Melhora performance do kube-apiserver
- Reduz watches em clusters grandes

### Limitação
- Não pode ser alterado após criado
- Deletar e recriar para atualizar

---

## Atualizações Automáticas

### Volumes
- ConfigMaps montados são atualizados automaticamente
- Kubelet periodicamente sincroniza
- Delay até atualização (kubelet sync period + cache propagation)

### Environment Variables
- **NÃO são atualizados automaticamente**
- Requer restart do Pod

### SubPath
- SubPath mounts **não recebem** updates automáticos

---

## Tamanho Limit

- **Máximo:** 1 MiB por ConfigMap
- Para configs maiores, usar volume ou database externo

---

## Exemplos Práticos

### Application Config
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_ENV: "production"
  DATABASE_HOST: "postgres.default.svc.cluster.local"
  DATABASE_PORT: "5432"
  LOG_LEVEL: "info"
---
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        envFrom:
        - configMapRef:
            name: app-config
```

### Config File Mount
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-config
data:
  nginx.conf: |
    server {
      listen 80;
      server_name example.com;
      location / {
        proxy_pass http://backend;
      }
    }
---
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: nginx
    image: nginx
    volumeMounts:
    - name: config
      mountPath: /etc/nginx/nginx.conf
      subPath: nginx.conf
  volumes:
  - name: config
    configMap:
      name: nginx-config
```

---

## Conceitos-Chave

1. **Key-Value Pairs**: Dados de configuração
2. **Environment Variables**: Injetar como env vars
3. **Volume Mount**: Montar como arquivos
4. **Immutable**: ConfigMaps que não mudam
5. **1 MiB Limit**: Tamanho máximo

---

## ConfigMap vs Secret

| Aspecto | ConfigMap | Secret |
|---------|-----------|--------|
| **Dados** | Não-confidenciais | Confidenciais |
| **Encoding** | Plain text | Base64 |
| **Tamanho** | 1 MiB | 1 MiB |
| **Uso** | Configs, env vars | Passwords, tokens |
| **Encryption** | Não (sem config) | Sim (com config) |

---

## Próximos Passos de Estudo

- [ ] ConfigMaps com Helm/Kustomize
- [ ] Config drift detection
- [ ] GitOps com ConfigMaps
- [ ] ConfigMap rotation strategies

---

## Referências

- Kubernetes Docs: https://kubernetes.io/docs/concepts/configuration/configmap/
- Configure Pod: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
- Twelve-Factor App: https://12factor.net/