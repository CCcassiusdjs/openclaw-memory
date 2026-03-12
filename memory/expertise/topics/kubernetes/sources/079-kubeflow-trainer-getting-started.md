# Getting Started with Kubeflow Trainer - PyTorch

**Fonte:** https://www.kubeflow.org/docs/components/trainer/getting-started/
**Tipo:** Tutorial
**Data:** 2026-03-12

---

## Resumo

Tutorial prático de Kubeflow Trainer com PyTorch distributed training. Mostra como definir função de treinamento, criar TrainJob e monitorar execução.

---

## Prerequisites

- Kubernetes cluster com Kubeflow Trainer control plane
- Kubeflow Python SDK instalado

### Install Kubeflow SDK
```bash
# Stable version
pip install -U kubeflow

# Latest from source
pip install git+https://github.com/kubeflow/sdk.git@main
```

---

## PyTorch Training Function

### Complete Example
```python
def train_pytorch():
    import os
    import torch
    from torch import nn
    import torch.nn.functional as F
    from torchvision import datasets, transforms
    import torch.distributed as dist
    from torch.utils.data import DataLoader, DistributedSampler

    # [1] Configure device and backend
    device, backend = ("cuda", "nccl") if torch.cuda.is_available() else ("cpu", "gloo")
    dist.init_process_group(backend=backend)

    local_rank = int(os.getenv("LOCAL_RANK", 0))
    print(
        "Distributed Training with WORLD_SIZE: {}, RANK: {}, LOCAL_RANK: {}.".format(
            dist.get_world_size(),
            dist.get_rank(),
            local_rank,
        )
    )

    # [2] Define CNN Model
    class Net(nn.Module):
        def __init__(self):
            super(Net, self).__init__()
            self.conv1 = nn.Conv2d(1, 20, 5, 1)
            self.conv2 = nn.Conv2d(20, 50, 5, 1)
            self.fc1 = nn.Linear(4 * 4 * 50, 500)
            self.fc2 = nn.Linear(500, 10)

        def forward(self, x):
            x = F.relu(self.conv1(x))
            x = F.max_pool2d(x, 2, 2)
            x = F.relu(self.conv2(x))
            x = F.max_pool2d(x, 2, 2)
            x = x.view(-1, 4 * 4 * 50)
            x = F.relu(self.fc1(x))
            x = self.fc2(x)
            return F.log_softmax(x, dim=1)

    # [3] Attach model to device
    device = torch.device(f"{device}:{local_rank}")
    model = nn.parallel.DistributedDataParallel(Net().to(device))
    model.train()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)

    # [4] Download dataset on rank 0
    if local_rank == 0:
        dataset = datasets.FashionMNIST(
            "./data",
            train=True,
            download=True,
            transform=transforms.Compose([transforms.ToTensor()]),
        )
    dist.barrier()
    
    dataset = datasets.FashionMNIST(
        "./data",
        train=True,
        download=False,
        transform=transforms.Compose([transforms.ToTensor()]),
    )
    train_loader = DataLoader(
        dataset,
        batch_size=100,
        sampler=DistributedSampler(dataset),
    )

    # [5] Training loop
    for epoch in range(3):
        for batch_idx, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            loss = F.nll_loss(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            if batch_idx % 10 == 0 and dist.get_rank() == 0:
                print(
                    "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                        epoch,
                        batch_idx * len(inputs),
                        len(train_loader.dataset),
                        100.0 * batch_idx / len(train_loader),
                        loss.item(),
                    )
                )

    dist.barrier()
    if dist.get_rank() == 0:
        print("Training is finished")
    dist.destroy_process_group()
```

---

## Listing Available Runtimes

```python
from kubeflow.trainer import TrainerClient, CustomTrainer

for r in TrainerClient().list_runtimes():
    print(f"Runtime: {r.name}")
```

Output:
```
Runtime: torch-distributed
```

---

## Creating a TrainJob

```python
job_id = TrainerClient().train(
    trainer=CustomTrainer(
        func=train_pytorch,
        num_nodes=4,
        resources_per_node={
            "cpu": 3,
            "memory": "16Gi",
            "gpu": 1,  # Comment if no GPUs
        },
    )
)
```

---

## Checking Job Status

### View Steps
```python
for s in TrainerClient().get_job(name=job_id).steps:
    print(f"Step: {s.name}, Status: {s.status}, Devices: {s.device} x {s.device_count}")
```

Output:
```
Step: node-0, Status: Succeeded, Devices: gpu x 1
Step: node-1, Status: Succeeded, Devices: gpu x 1
Step: node-2, Status: Succeeded, Devices: gpu x 1
Step: node-3, Status: Succeeded, Devices: gpu x 1
```

### View Logs
```python
for logline in TrainerClient().get_job_logs(job_id, follow=True):
    print(logline)
```

---

## Key Concepts

### Automatic Environment Setup
Kubeflow Trainer configura automaticamente:
- Distributed backend (NCCL/Gloo)
- Process group initialization
- LOCAL_RANK, WORLD_SIZE, RANK

### DistributedSampler
```python
train_loader = DataLoader(
    dataset,
    batch_size=100,
    sampler=DistributedSampler(dataset),  # Automatic data distribution
)
```

### Rank 0 Operations
```python
if local_rank == 0:
    # Download dataset only on rank 0
    dataset = datasets.FashionMNIST(...)
    
dist.barrier()  # Wait for download to complete
```

---

## Architecture Flow

```
┌─────────────────────────────────────────────────────┐
│           Python SDK (TrainerClient)               │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│          Kubeflow Trainer Control Plane             │
│  ┌───────────────────────────────────────────────┐│
│  │         TrainJob (4 nodes, 1 GPU each)         ││
│  └───────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│              Kubernetes Cluster                    │
│  ┌─────────────────────────────────────────────┐  │
│  │         torch-distributed Runtime            │  │
│  └─────────────────────────────────────────────┘  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐│
│  │ node-0  │  │ node-1  │  │ node-2  │  │ node-3 ││
│  │ rank=0  │  │ rank=1  │  │ rank=2  │  │ rank=3 ││
│  │ 15k imgs│  │ 15k imgs│  │ 15k imgs│  │ 15k im ││
│  └─────────┘  └─────────┘  └─────────┘  └────────┘│
└─────────────────────────────────────────────────────┘
```

---

## Distributed Data Parallel (DDP)

Kubeflow Trainer configura automaticamente DDP:
- `torch.distributed.init_process_group(backend)`
- `nn.parallel.DistributedDataParallel(model)`
- Sincronização de gradientes entre nodes

---

## Conceitos-Chave Extraídos

| Conceito | Descrição |
|----------|-----------|
| CustomTrainer | Define training function e recursos |
| TrainerClient | API client para TrainJobs |
| num_nodes | Número de nodes distribuídos |
| resources_per_node | CPU, memory, GPU por node |
| LOCAL_RANK | Rank local do processo no node |
| WORLD_SIZE | Total de processos distribuídos |
| DistributedSampler | Divide dados entre workers |

---

## Referências

- PyTorch DDP Tutorial: https://pytorch.org/tutorials/intermediate/ddp_tutorial.html
- Kubeflow PyTorch Guide: https://www.kubeflow.org/docs/components/trainer/user-guides/pytorch/