# Kubernetes Backup and Restore with Velero

**Fonte:** OneUptime Blog - https://oneuptime.com/blog/post/2026-01-06-kubernetes-backup-restore-velero/view
**Data:** Janeiro 2026
**Tópico:** Velero, Backup, Disaster Recovery, Scheduled Backups, Restore
**Status:** Lido

---

## Resumo Executivo

Guia completo de backup e restore de Kubernetes com Velero, incluindo instalação, backup scheduling, restore procedures, disaster recovery e migração cross-cluster.

---

## O que Velero Backup

### Recursos
- Kubernetes resources (Deployments, Services, ConfigMaps, etc.)
- Persistent Volume data (via snapshots ou file-level backup)
- Custom Resource Definitions (CRDs)
- Cluster-scoped resources (opcional)

---

## Instalação do Velero CLI

### macOS
```bash
brew install velero
```

### Linux
```bash
curl -L https://github.com/vmware-tanzu/velero/releases/download/v1.15.0/velero-v1.15.0-linux-amd64.tar.gz | tar xz
sudo mv velero-v1.15.0-linux-amd64/velero /usr/local/bin/
```

---

## Setup por Provider

### AWS S3 + EBS
```bash
# Criar S3 bucket
aws s3 mb s3://velero-backups-mycompany --region us-west-2

# Criar IAM policy
cat > velero-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeVolumes",
        "ec2:DescribeSnapshots",
        "ec2:CreateTags",
        "ec2:CreateVolume",
        "ec2:CreateSnapshot",
        "ec2:DeleteSnapshot"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:PutObject",
        "s3:AbortMultipartUpload",
        "s3:ListMultipartUploadParts"
      ],
      "Resource": "arn:aws:s3:::velero-backups-mycompany/*"
    },
    {
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::velero-backups-mycompany"
    }
  ]
}
EOF

# Criar credentials
cat > credentials-velero <<EOF
[default]
aws_access_key_id=<AWS_ACCESS_KEY>
aws_secret_access_key=<AWS_SECRET_KEY>
EOF

# Instalar Velero
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.11.0 \
  --bucket velero-backups-mycompany \
  --backup-location-config region=us-west-2 \
  --snapshot-location-config region=us-west-2 \
  --secret-file ./credentials-velero
```

### GCP GCS + Persistent Disk
```bash
# Criar GCS bucket
gsutil mb gs://velero-backups-mycompany

# Criar service account
gcloud iam service-accounts create velero --display-name "Velero service account"

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:velero@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/compute.storageAdmin

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:velero@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/storage.objectAdmin

# Criar key
gcloud iam service-accounts keys create credentials-velero \
  --iam-account velero@$PROJECT_ID.iam.gserviceaccount.com

# Instalar
velero install \
  --provider gcp \
  --plugins velero/velero-plugin-for-gcp:v1.11.0 \
  --bucket velero-backups-mycompany \
  --secret-file ./credentials-velero
```

### Azure Blob Storage
```bash
# Criar storage account
az storage account create \
  --name velerobackups \
  --resource-group myResourceGroup \
  --sku Standard_GRS

# Criar container
az storage container create \
  --name velero \
  --account-name velerobackups

# Obter key
AZURE_STORAGE_KEY=$(az storage account keys list \
  --account-name velerobackups \
  --query "[0].value" -o tsv)

# Criar credentials
cat > credentials-velero <<EOF
AZURE_STORAGE_ACCOUNT_ACCESS_KEY=$AZURE_STORAGE_KEY
AZURE_CLOUD_NAME=AzurePublicCloud
EOF

# Instalar
velero install \
  --provider azure \
  --plugins velero/velero-plugin-for-microsoft-azure:v1.11.0 \
  --bucket velero \
  --backup-location-config storageAccount=velerobackups \
  --secret-file ./credentials-velero
```

---

## Criando Backups

### On-Demand Backup
```bash
# Backup completo do cluster
velero backup create full-cluster-backup

# Backup de namespace específico
velero backup create production-backup --include-namespaces production

# Backup de múltiplos namespaces
velero backup create apps-backup --include-namespaces production,staging

# Backup por label
velero backup create critical-apps --selector app=critical

# Backup excluindo recursos
velero backup create partial-backup \
  --include-namespaces production \
  --exclude-resources secrets,configmaps

# Backup com TTL
velero backup create daily-backup --ttl 168h  # 7 dias
```

### Verificar Status
```bash
# Listar backups
velero backup get

# Detalhes do backup
velero backup describe production-backup

# Logs do backup
velero backup logs production-backup
```

---

## Scheduled Backups

### Criar Schedules
```bash
# Backup diário às 2 AM
velero schedule create daily-production \
  --schedule="0 2 * * *" \
  --include-namespaces production \
  --ttl 168h

# Backup horário
velero schedule create hourly-backup \
  --schedule="0 * * * *" \
  --include-namespaces production \
  --ttl 24h

# Backup semanal
velero schedule create weekly-full \
  --schedule="0 0 * * 0" \
  --ttl 720h  # 30 dias
```

### Gerenciar Schedules
```bash
# Listar
velero schedule get

# Detalhes
velero schedule describe daily-production

# Pausar
velero schedule pause daily-production

# Resumir
velero schedule unpause daily-production

# Deletar
velero schedule delete daily-production
```

---

## Restore

### Full Restore
```bash
# Restaurar tudo
velero restore create --from-backup production-backup

# Restaurar namespace específico
velero restore create --from-backup full-backup \
  --include-namespaces production

# Restaurar em namespace diferente
velero restore create --from-backup production-backup \
  --namespace-mappings production:production-restored
```

### Selective Restore
```bash
# Apenas deployments e services
velero restore create --from-backup production-backup \
  --include-resources deployments,services

# Excluir PVCs
velero restore create --from-backup production-backup \
  --exclude-resources persistentvolumeclaims

# Por label selector
velero restore create --from-backup production-backup \
  --selector app=frontend
```

### Verificar Restore
```bash
# Listar restores
velero restore get

# Detalhes
velero restore describe production-restore

# Logs
velero restore logs production-restore
```

---

## Volume Backups

### CSI Snapshots (Recomendado)
- Velero v1.14+ tem CSI plugin bundled
- Usa VolumeSnapshotClass nativo do Kubernetes

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: velero-snapshot-class
  labels:
    velero.io/csi-volumesnapshot-class: "true"
driver: ebs.csi.aws.com
deletionPolicy: Retain
```

### Restic/Kopia File-Level Backup
```bash
# Com Restic
velero install \
  --use-node-agent \
  --default-volumes-to-fs-backup

# Com Kopia (mais rápido)
velero install \
  --use-node-agent \
  --uploader-type=kopia \
  --default-volumes-to-fs-backup
```

### Annotation para Pods
```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    backup.velero.io/backup-volumes: data,logs
spec:
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: my-pvc
```

---

## Backup Hooks

### Pre-Backup Hook
```yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    pre.hook.backup.velero.io/container: myapp
    pre.hook.backup.velero.io/command: '["/bin/sh", "-c", "pg_dump -U postgres mydb > /backup/dump.sql"]'
    pre.hook.backup.velero.io/timeout: 120s
```

### Post-Backup Hook
```yaml
metadata:
  annotations:
    post.hook.backup.velero.io/container: myapp
    post.hook.backup.velero.io/command: '["/bin/sh", "-c", "rm /backup/dump.sql"]'
```

---

## Disaster Recovery Procedure

### Step 1: Prepare New Cluster
```bash
# Instalar Velero no cluster de DR
velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.11.0 \
  --bucket velero-backups-mycompany \
  --backup-location-config region=us-west-2 \
  --secret-file ./credentials-velero
```

### Step 2: Verify Backup Accessibility
```bash
# Verificar backup location
velero backup-location get

# Listar backups disponíveis
velero backup get
```

### Step 3: Restore Critical Namespaces
```bash
# Restaurar infra primeiro
velero restore create dr-infra \
  --from-backup latest-backup \
  --include-namespaces cert-manager,ingress-nginx

# Aguardar
velero restore wait dr-infra

# Restaurar aplicações
velero restore create dr-apps \
  --from-backup latest-backup \
  --include-namespaces production

# Aguardar
velero restore wait dr-apps
```

### Step 4: Verify Restoration
```bash
# Listar recursos
kubectl get all -n production

# Verificar PVCs
kubectl get pvc -n production

# Confirmar pods
kubectl get pods -n production

# Testar health
curl https://app.example.com/healthz
```

---

## Cross-Cluster Migration

```bash
# Source cluster: criar backup
velero backup create migration-backup --include-namespaces production

# Destination cluster: instalar Velero
velero install \
  --provider aws \
  --bucket velero-backups-mycompany \
  ...

# Destination cluster: restaurar
velero restore create migration-restore --from-backup migration-backup
```

---

## Monitoring

### Prometheus Metrics
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: velero
  namespace: velero
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: velero
  endpoints:
  - port: monitoring
```

### Alerts
- Backup failures
- Missed scheduled backups
- Restore failures
- Storage location issues

---

## Insights para Kubernetes

1. **Velero é essencial para DR**: Backup completo de recursos e volumes
2. **CSI Snapshots recomendados**: Integração nativa com storage providers
3. **Scheduled backups obrigatórios**: Automação para consistência
4. **Hooks para consistência**: Pre/post hooks para databases
5. **Cross-cluster migration**: Mesmo bucket para migração

---

## Palavras-Chave
`velero` `backup` `disaster-recovery` `restore` `scheduled-backups` `csi-snapshots` `kubernetes`