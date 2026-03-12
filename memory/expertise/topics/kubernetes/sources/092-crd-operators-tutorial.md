# Building Kubernetes Custom Resources and Operators

**Fonte:** OneUptime Blog - https://oneuptime.com/blog/post/2026-02-20-kubernetes-custom-resources-operators/view
**Data:** Fevereiro 2026
**Tópico:** CRDs, Custom Resources, Operators, kopf, Controller Development
**Status:** Lido

---

## Resumo Executivo

Tutorial completo de criação de Custom Resource Definitions e Operators, incluindo CRD YAML, controller Python com kopf, e deployment com RBAC.

---

## Conceitos

### CRD vs CR
- **CRD (Custom Resource Definition)**: Define schema do novo recurso
- **CR (Custom Resource)**: Instância do CRD (como row matching schema)

### Operator
- Controller que watch CRs e reconcilia estado

---

## Arquitetura

```
CRD → Extends Kubernetes API
     → Users create Custom Resources
     → Operator watches for changes
     → Operator reconciles desired state
     → Creates/Updates Kubernetes objects
     → Application running as desired
```

---

## CRD: WebApp

### webapp-crd.yaml
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: webapps.apps.example.com
spec:
  group: apps.example.com
  names:
    kind: WebApp
    listKind: WebAppList
    plural: webapps
    singular: webapp
    shortNames:
    - wa
  scope: Namespaced
  versions:
  - name: v1alpha1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            required:
            - image
            - replicas
            properties:
              image:
                type: string
                description: "Container image to deploy"
              replicas:
                type: integer
                minimum: 1
                maximum: 20
                description: "Number of pod replicas"
              port:
                type: integer
                default: 8080
                description: "Container port"
              resources:
                type: object
                properties:
                  cpu:
                    type: string
                    default: "100m"
                  memory:
                    type: string
                    default: "128Mi"
          status:
            type: object
            properties:
              availableReplicas:
                type: integer
              conditions:
                type: array
                items:
                  type: object
                  properties:
                    type:
                      type: string
                    status:
                      type: string
                    lastTransitionTime:
                      type: string
                    message:
                      type: string
    additionalPrinterColumns:
    - name: Image
      type: string
      jsonPath: .spec.image
    - name: Replicas
      type: integer
      jsonPath: .spec.replicas
    - name: Available
      type: integer
      jsonPath: .status.availableReplicas
    - name: Age
      type: date
      jsonPath: .metadata.creationTimestamp
    subresources:
      status: {}
```

---

## Custom Resource: WebApp Instance

### my-webapp.yaml
```yaml
apiVersion: apps.example.com/v1alpha1
kind: WebApp
metadata:
  name: my-frontend
  namespace: default
spec:
  image: nginx:1.25
  replicas: 3
  port: 80
  resources:
    cpu: "200m"
    memory: "256Mi"
```

### Comandos
```bash
# Registrar CRD
kubectl apply -f webapp-crd.yaml

# Verificar CRD
kubectl get crd webapps.apps.example.com

# Criar instância
kubectl apply -f my-webapp.yaml

# Listar WebApps
kubectl get webapps
kubectl get wa
```

---

## Controller Python (kopf)

### operator.py
```python
import kopf
import kubernetes
from kubernetes import client

@kopf.on.create("apps.example.com", "v1alpha1", "webapps")
def create_webapp(spec, name, namespace, logger, **kwargs):
    """Create Deployment and Service for WebApp."""
    image = spec["image"]
    replicas = spec["replicas"]
    port = spec.get("port", 8080)
    resources = spec.get("resources", {})

    deployment = build_deployment(name, namespace, image, replicas, port, resources)
    service = build_service(name, namespace, port)

    apps_api = client.AppsV1Api()
    apps_api.create_namespaced_deployment(
        namespace=namespace,
        body=deployment,
    )
    logger.info(f"Deployment {name} created")

    core_api = client.CoreV1Api()
    core_api.create_namespaced_service(
        namespace=namespace,
        body=service,
    )
    logger.info(f"Service {name} created")

@kopf.on.update("apps.example.com", "v1alpha1", "webapps")
def update_webapp(spec, name, namespace, logger, **kwargs):
    """Update Deployment when WebApp changes."""
    image = spec["image"]
    replicas = spec["replicas"]
    port = spec.get("port", 8080)
    resources = spec.get("resources", {})

    deployment = build_deployment(name, namespace, image, replicas, port, resources)

    apps_api = client.AppsV1Api()
    apps_api.patch_namespaced_deployment(
        name=name,
        namespace=namespace,
        body=deployment,
    )
    logger.info(f"Deployment {name} updated")

@kopf.on.delete("apps.example.com", "v1alpha1", "webapps")
def delete_webapp(name, namespace, logger, **kwargs):
    """Cleanup Deployment and Service."""
    apps_api = client.AppsV1Api()
    core_api = client.CoreV1Api()

    try:
        apps_api.delete_namespaced_deployment(name=name, namespace=namespace)
        logger.info(f"Deployment {name} deleted")
    except client.exceptions.ApiException as e:
        if e.status != 404:
            raise

    try:
        core_api.delete_namespaced_service(name=name, namespace=namespace)
        logger.info(f"Service {name} deleted")
    except client.exceptions.ApiException as e:
        if e.status != 404:
            raise

def build_deployment(name, namespace, image, replicas, port, resources):
    """Build Deployment object."""
    return client.V1Deployment(
        metadata=client.V1ObjectMeta(name=name, namespace=namespace),
        spec=client.V1DeploymentSpec(
            replicas=replicas,
            selector=client.V1LabelSelector(
                match_labels={"app": name, "managed-by": "webapp-operator"},
            ),
            template=client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(
                    labels={"app": name, "managed-by": "webapp-operator"},
                ),
                spec=client.V1PodSpec(
                    containers=[
                        client.V1Container(
                            name="app",
                            image=image,
                            ports=[client.V1ContainerPort(container_port=port)],
                            resources=client.V1ResourceRequirements(
                                requests={
                                    "cpu": resources.get("cpu", "100m"),
                                    "memory": resources.get("memory", "128Mi"),
                                },
                            ),
                        )
                    ],
                ),
            ),
        ),
    )

def build_service(name, namespace, port):
    """Build Service object."""
    return client.V1Service(
        metadata=client.V1ObjectMeta(name=name, namespace=namespace),
        spec=client.V1ServiceSpec(
            selector={"app": name, "managed-by": "webapp-operator"},
            ports=[
                client.V1ServicePort(
                    port=port,
                    target_port=port,
                    protocol="TCP",
                )
            ],
            type="ClusterIP",
        ),
    )
```

---

## Deployment do Operator

### operator-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-operator
  namespace: operators
spec:
  replicas: 1
  selector:
    matchLabels:
      app: webapp-operator
  template:
    spec:
      serviceAccountName: webapp-operator
      containers:
      - name: operator
        image: myregistry/webapp-operator:v1.0.0
        command: ["kopf", "run", "operator.py", "--verbose"]
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: webapp-operator
  namespace: operators
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: webapp-operator
rules:
- apiGroups: ["apps.example.com"]
  resources: ["webapps", "webapps/status"]
  verbs: ["get", "list", "watch", "patch", "update"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["events"]
  verbs: ["create"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: webapp-operator
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: webapp-operator
subjects:
- kind: ServiceAccount
  name: webapp-operator
  namespace: operators
```

---

## Reconciliation Loop

```
Watch for CR Events → Event Type?
  → Create: Create child resources
  → Update: Update child resources
  → Delete: Delete child resources
→ Update CR status
→ Wait for next event
```

---

## Testing

```bash
# Aplicar CRD
kubectl apply -f webapp-crd.yaml

# Deploy operator
kubectl apply -f operator-deployment.yaml

# Criar WebApp
kubectl apply -f my-webapp.yaml

# Verificar Deployment e Service criados
kubectl get deployments -l managed-by=webapp-operator
kubectl get services -l managed-by=webapp-operator

# Scale atualizando CR
kubectl patch webapp my-frontend --type merge -p '{"spec":{"replicas":5}}'

# Verificar logs
kubectl logs -n operators deployment/webapp-operator
```

---

## Best Practices

1. **Owner References**: Cleanup automático de recursos filhos
2. **Idempotência**: Mesmo resultado sempre
3. **Status Subresource**: Usuários verificam estado
4. **Finalizers**: Cleanup antes de deletar CR
5. **Validation**: Schema rejeita inputs inválidos
6. **Logging**: Logs claros para debugging

---

## Insights para Kubernetes

1. **CRD define schema**: Validação automática na API
2. **kopf simplifica**: Framework Python para controllers
3. **RBAC é obrigatório**: Operator precisa de permissões
4. **Reconciliation é core**: Loop de sincronização estado
5. **Best practices são críticas**: Idempotência, owner references

---

## Palavras-Chave
`crd` `custom-resources` `operators` `kopf` `python` `controller` `kubernetes`