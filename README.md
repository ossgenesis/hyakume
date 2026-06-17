# StoneScan

Surface-defect inspection for natural stone. A thin handheld capture unit sweeps a slab; the cloud produces a pass/fail grade, a defect heatmap, and a tamper-evident per-slab record viewed on mobile/web.

Sold as a **subscription**: the customer gets a capture device bundled with service. The moat is the **proprietary RGB-D dataset and the dashboard/inference service**, not the hardware — the device is a commodity, easy to replace or upgrade.

See [SPEC.md](SPEC.md) for the full design spec and component map.

## Architecture (cloud-inference)

```
device (stereo camera + LiDAR)  →  mobile app  →  cloud (AKS / Kubernetes)  →  result to mobile/web
        capture only                 relay + UI        inference + grading
```

All ML runs in the cloud. The device captures synchronized RGB + LiDAR depth and streams it to a paired mobile app, which relays it to a GPU-backed Kubernetes cluster for inference and grading. No on-device inference, no signed-OTA model bundles.

## Repository layout

```
edge/          capture unit firmware (Python) — stereo + LiDAR capture only
backend/       cloud backend  (Go)            — API, org/user/device/scan/report services
dashboard/     web dashboard  (React)         — browse, manage, export
mlops/         ML pipeline    (Python)        — train, eval, active learning (RGB-D models)
deploy/        infrastructure                 — Terraform (AKS), k8s manifests, Docker
diagram/       architecture diagrams          — Mermaid .mmd files
stone-defect-project-document/   design docs  — PRD, arch, security, frontend spec, tickets
```

## Quick start

```bash
# cloud backend
cd backend && go run ./cmd/server

# web dashboard
cd dashboard && npm install && npm run dev

# local stack
docker-compose up

# provision cloud infra (AKS + GPU pools)
cd deploy/terraform && terraform init && terraform apply
```

## Releases

| Stage | Goal |
|---|---|
| R0 — Bench POC | Stereo + LiDAR capture → cloud RGB-D anomaly detection → result on mobile/web |
| R1 — Pilot | Full capture device + mobile app; cloud grading, reports, management, grading profiles |
| R2 — Scale | Buyer-shared reports, active-learning loop, in-cluster LLM features, SLAs |

## Archive

Pre-pivot (edge-inference) design documents are kept under [archive/](archive/INDEX.md) for historical reference only. The authoritative docs are the current ones at the repo root and in `stone-defect-project-document/`.
