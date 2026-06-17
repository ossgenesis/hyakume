# StoneScan POC infrastructure (AKS)

Terraform for the POC cloud-inference stack on Azure. AKS control plane is free,
so it runs 24/7; GPU node pools are elastic and scale to zero when idle.

## What this creates

| Resource | Purpose |
|---|---|
| Resource group | Container for everything |
| AKS cluster (free control plane) | Orchestration, runs 24/7 |
| `system` pool (CPU, D4s_v5) | Always-on: API, dashboard backend, ingestion |
| `gpuwarm` pool (A10) | Production inference — warm during hours, scale-to-zero off-hours |
| `gpuspot` pool (A10 spot) | Experiments, batch retraining, in-cluster LLM — always scales to zero |
| Capacity reservation *(optional)* | Pre-booked GPU so the warm pool is guaranteed a node |
| Container registry (ACR) | Model server images |
| Storage account + containers | RGB+LiDAR captures, heatmaps, report PDFs |
| Postgres flexible server | Metadata DB (org/user/device/scan/slab/defect) |

## Prerequisites

- `terraform >= 1.6`, `az` CLI logged in (`az login`)
- A GPU **quota** for the `NVadsA10_v5` family in your region — request it under
  Subscription → Usage + quotas *before* applying, approval can take a day.

## Usage

```bash
cd deploy/terraform
cp terraform.tfvars.example terraform.tfvars   # fill in subscription_id etc.
export TF_VAR_postgres_admin_password='a-strong-password'

terraform init
terraform plan
terraform apply

# point kubectl at the cluster
$(terraform output -raw get_credentials_command)
```

## After apply: install the NVIDIA GPU operator

AKS GPU nodes need the NVIDIA device plugin/drivers before pods can request
`nvidia.com/gpu`. Install once with Helm:

```bash
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia && helm repo update
helm install --wait gpu-operator nvidia/gpu-operator \
  -n gpu-operator --create-namespace
```

Schedule GPU pods onto the pools by matching the taint/labels, e.g.:

```yaml
tolerations:
  - key: "nvidia.com/gpu"
    operator: "Exists"
    effect: "NoSchedule"
nodeSelector:
  workload: inference   # or "experiment" for the spot pool
resources:
  limits:
    nvidia.com/gpu: 1
```

## Cost levers

- **Scale to zero:** set `gpu_warm_min_count = 0` to pay nothing for GPU off-hours.
  Trade-off: 3–10 min cold start on the next scan. Set `= 1` during business
  hours to keep inference warm.
- **Fractional GPU:** switch `gpu_vm_size` to `Standard_NV6ads_A10_v5` (1/6 A10)
  for a very cheap always-warm vision node. Too small for the LLM — keep the LLM
  on the spot pool.
- **Spot pool** is interruptible; only use it for work that tolerates eviction.

## Reserved capacity (the kept option)

If Azure GPU availability gets tight, guarantee the warm pool a node:

```hcl
enable_capacity_reservation = true
capacity_reservation_count  = 1
```

You then pay for the reserved GPU whether or not it's in use — the price of
guaranteed availability. Leave `false` for normal POC cost savings.

## Notes / boundaries

- This is **single-cloud by design** for the POC. A managed AKS control plane
  cannot own GPU nodes in GCP/AWS — cross-cloud bursting (Liqo, multi-cluster)
  is a production concern, handled separately.
- Postgres is set to public network access for POC convenience. Lock it behind
  VNet integration / private endpoint before production.
- State is local by default. Uncomment the `backend "azurerm"` block in
  `versions.tf` for team use.
```
