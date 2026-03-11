# Kubernetes Sidecar and Ambassador Patterns

**Fonte:** https://oneuptime.com/blog/post/2026-01-19-kubernetes-sidecar-ambassador-patterns/view
**Tipo:** Architecture Patterns
**Prioridade:** Média
**Data:** 2026-03-11

## Resumo Executivo

Padrões de containers que estendem funcionalidade de aplicações sem modificar o container principal.

---

## Patterns Overview

| Pattern | Propósito | Exemplos |
|---------|-----------|----------|
| **Sidecar** | Estender funcionalidade | Logging, sync, proxy |
| **Ambassador** | Proxy de conexões | Service mesh, load balancing |
| **Adapter** | Padronizar output | Metrics export, log formatting |
| **Init Container** | Setup antes do app | Migrations, config download |

---

## Sidecar Pattern

### Logging Sidecar
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-with-logging
spec:
  volumes:
  - name: log-volume
    emptyDir: {}
  
  containers:
  - name: app
    image: myapp:latest
    volumeMounts:
    - name: log-volume
      mountPath: /var/log/app
  
  - name: log-shipper
    image: fluent/fluent-bit:latest
    volumeMounts:
    - name: log-volume
      mountPath: /var/log/app
      readOnly: true
    env:
    - name: FLUENT_ELASTICSEARCH_HOST
      value: "elasticsearch.logging"
```

**Uso:** Fluent Bit, Fluentd, Vector para shipping de logs.

### Git-Sync Sidecar
```yaml
containers:
- name: nginx
  image: nginx:alpine
  volumeMounts:
  - name: content
    mountPath: /usr/share/nginx/html

- name: git-sync
  image: k8s.gcr.io/git-sync/git-sync:v3.6.0
  volumeMounts:
  - name: content
    mountPath: /data
  env:
  - name: GIT_SYNC_REPO
    value: "https://github.com/example/content.git"
  - name: GIT_SYNC_BRANCH
    value: "main"
  - name: GIT_SYNC_PERIOD
    value: "30s"
```

**Uso:** Sincronizar conteúdo de repositórios Git.

### TLS/SSL Termination Sidecar
```yaml
containers:
- name: app
  image: myapp:latest
  ports:
  - containerPort: 8080  # HTTP only

- name: ssl-proxy
  image: nginx:alpine
  ports:
  - containerPort: 443
  volumeMounts:
  - name: ssl-certs
    mountPath: /etc/ssl/certs
    readOnly: true
```

**Uso:** NGINX, Envoy para TLS termination.

---

## Ambassador Pattern

### Database Connection Ambassador (PgBouncer)
```yaml
containers:
- name: app
  image: myapp:latest
  env:
  - name: DATABASE_HOST
    value: "localhost"  # Connect to ambassador
  - name: DATABASE_PORT
    value: "5432"

- name: pgbouncer
  image: edoburu/pgbouncer:latest
  ports:
  - containerPort: 5432
  env:
  - name: POOL_MODE
    value: "transaction"
  - name: DEFAULT_POOL_SIZE
    value: "20"
```

**Benefícios:**
- Connection pooling
- Connection limiting
- Reduced database load

### Cloud SQL Proxy Ambassador
```yaml
containers:
- name: app
  image: myapp:latest
  env:
  - name: DB_HOST
    value: "localhost"
  - name: DB_PORT
    value: "5432"

- name: cloudsql-proxy
  image: gcr.io/cloudsql-docker/gce-proxy:latest
  command:
  - /cloud_sql_proxy
  - -instances=project:region:instance=tcp:5432
  - -credential_file=/secrets/cloudsql/credentials.json
  ports:
  - containerPort: 5432
```

**Benefícios:**
- IAM-based auth
- TLS automatic
- No public IPs

### Service Mesh Ambassador (Envoy)
```yaml
containers:
- name: app
  image: myapp:latest
  env:
  - name: UPSTREAM_URL
    value: "http://localhost:8080"

- name: envoy
  image: envoyproxy/envoy:v1.27-latest
  ports:
  - containerPort: 8080
  volumeMounts:
  - name: envoy-config
    mountPath: /etc/envoy
  args:
  - -c
  - /etc/envoy/envoy.yaml
```

**Benefícios:**
- Load balancing
- Circuit breaking
- Retry logic
- Traffic splitting

---

## Adapter Pattern

### Prometheus Metrics Adapter
```yaml
containers:
- name: app
  image: myapp:latest
  ports:
  - containerPort: 8080

- name: nginx-exporter
  image: nginx/nginx-prometheus-exporter:latest
  args:
  - -nginx.scrape-uri=http://localhost:8080/stub_status
  ports:
  - containerPort: 9113
```

**Uso:** Adaptar formato de métricas para Prometheus.

### Log Format Adapter (Vector)
```yaml
containers:
- name: app
  image: myapp:latest
  volumeMounts:
  - name: log-volume
    mountPath: /var/log/app

- name: log-adapter
  image: timberio/vector:latest-alpine
  volumeMounts:
  - name: log-volume
    mountPath: /var/log/app
    readOnly: true
  - name: vector-config
    mountPath: /etc/vector
```

**Uso:** Parse, enrich, forward logs.

---

## Init Containers

### Database Migration
```yaml
initContainers:
- name: wait-for-db
  image: busybox:latest
  command:
  - sh
  - -c
  - |
    until nc -z postgres-service 5432; do
      echo "Waiting for database..."
      sleep 2
    done

- name: migrate
  image: myapp:latest
  command: ["python", "manage.py", "migrate"]
```

**Uso:** Wait for dependencies, run migrations.

### Configuration Download
```yaml
initContainers:
- name: download-config
  image: curlimages/curl:latest
  volumeMounts:
  - name: config-volume
    mountPath: /config
  command:
  - sh
  - -c
  - |
    curl -o /config/app.conf https://config-server/myapp/config
    curl -o /config/secrets.json https://vault:8200/v1/secret/data/myapp

containers:
- name: app
  image: myapp:latest
  volumeMounts:
  - name: config-volume
    mountPath: /app/config
```

---

## Deployment with Sidecars

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  template:
    spec:
      volumes:
      - name: log-volume
        emptyDir: {}
      - name: fluent-bit-config
        configMap:
          name: fluent-bit-config

      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: log-volume
          mountPath: /var/log/app
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

      - name: fluent-bit
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: log-volume
          mountPath: /var/log/app
          readOnly: true
        - name: fluent-bit-config
          mountPath: /fluent-bit/etc/
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
```

---

## Best Practices

### Resource Allocation
```yaml
containers:
- name: main-app
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi"
      cpu: "1000m"

- name: sidecar
  resources:
    requests:
      memory: "64Mi"
      cpu: "50m"
    limits:
      memory: "128Mi"
      cpu: "100m"
```

**Importante:** Sempre definir resources para sidecars.

### Health Checks
```yaml
- name: sidecar
  livenessProbe:
    httpGet:
      path: /health
      port: 8081
    initialDelaySeconds: 10
    periodSeconds: 30
  readinessProbe:
    httpGet:
      path: /ready
      port: 8081
    initialDelaySeconds: 5
    periodSeconds: 10
```

---

## Conceitos-Chave

1. **Sidecar**: Container auxiliar no mesmo Pod
2. **Ambassador**: Proxy de conexões externas
3. **Adapter**: Padronização de output
4. **Init Container**: Setup antes do app principal
5. **Shared Volume**: Comunicação entre containers

---

## Casos de Uso Comuns

| Pattern | Quando Usar |
|---------|-------------|
| Sidecar | Logging, monitoring, TLS |
| Ambassador | Connection pooling, proxies |
| Adapter | Metrics export, format conversion |
| Init Container | Migrations, config download |

---

## Próximos Passos de Estudo

- [ ] Service mesh patterns (Istio, Linkerd)
- [ ] Dapr sidecar pattern
- [ ] Vault agent injector
- [ ] Multi-container debugging

---

## Referências

- Article: https://oneuptime.com/blog/post/2026-01-19-kubernetes-sidecar-ambassador-patterns/view
- Kubernetes Docs: https://kubernetes.io/docs/concepts/workloads/pods/#how-pods-manage-multiple-containers