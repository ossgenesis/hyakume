# StoneScan

Handheld surface-defect scanner for natural stone. Sweeps a slab, produces a pass/fail grade, a defect heatmap, and a tamper-evident per-slab record.

See [SPEC.md](SPEC.md) for the full design spec and component map.

## Repository layout

```
edge/          on-device app  (Python) — capture, inference, grading, sync, UI
backend/       cloud backend  (Go)     — API, org/user/device/scan/report services
dashboard/     web dashboard  (React)  — browse, manage, export
mlops/         ML pipeline    (Python) — train, eval, export, active learning
deploy/        infrastructure          — k8s, Docker, Terraform
diagram/       architecture diagrams   — Mermaid .mmd files
hyakume/       design documents        — PRD, arch, security, frontend spec, tickets
```

## Quick start

```bash
# cloud backend
cd backend && go run ./cmd/server

# web dashboard
cd dashboard && npm install && npm run dev

# local stack
docker-compose up
```

## Releases

| Stage | Goal |
|---|---|
| R0 — Bench POC | Photometric-stereo capture + anomaly detection + on-device result |
| R1 — Pilot | Full handheld device; sync, reports, management, grading profiles |
| R2 — Scale | OTA updates, buyer reports, active-learning loop, SLAs |
