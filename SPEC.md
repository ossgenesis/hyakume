# StoneScan — Spec & Plan

| | |
|---|---|
| **Version** | 0.1 (draft) |
| **Owner** | Founder / Product |
| **Status** | Pre-R0 (Bench POC) |

## 1. Problem

Small and mid-size stone factories and traders inspect slab surfaces manually — subjective, inconsistent, and undocumented. StoneScan is a handheld surface-defect scanner that turns inspection into a fast, repeatable, tamper-evident measurement.

Full product requirements: [stone-defect-project-document/01-PRD-stonescan.md](stone-defect-project-document/01-PRD-stonescan.md)

## 2. Goals

- Detect grains, cracks, fissures, pits, stains, and impurities on granite, marble, slate, and quartzite.
- Match or beat an expert inspector's accuracy on agreed defect classes (G1).
- Sub-minute per-slab workflow; full offline operation in real yard/warehouse lighting (G2).
- Produce tamper-evident per-slab records and exportable reports.
- Accumulate a proprietary labeled dataset as a moat.

## 3. Non-Goals (this cycle)

- Internal / subsurface defects.
- Dimensional metrology.
- Any second vertical before gate G3.
- Fixed inline line system.

## 4. Architecture Overview

Four layers: **edge device** (capture + inference + grading + offline record), **cloud backend** (sync + management + reports), **web dashboard** (browse, manage, export), and **MLOps pipeline** (train → registry → OTA).

See [stone-defect-project-document/02-technical-architecture-stonescan.md](stone-defect-project-document/02-technical-architecture-stonescan.md) and [diagram/system-overview.mmd](diagram/system-overview.mmd).

## 5. Component Map

| Directory | What it is | Language / Framework |
|---|---|---|
| `edge/` | On-device app: capture, preprocess, inference, grading, sync | Python |
| `backend/` | Cloud API + services: org, user, device, scan, profile, report, registry | Go |
| `dashboard/` | Web SPA: search, scan detail, reports, management | React / TypeScript |
| `mlops/` | Training, eval, ONNX export, active-learning loop | Python (Anomalib, Ultralytics, DVC, MLflow) |
| `deploy/` | Infrastructure-as-code: k8s manifests, Docker, Terraform | YAML / HCL |
| `diagram/` | Architecture diagrams (Mermaid) | — |
| `hyakume/` | Design documents (PRD, architecture, security, frontend spec, tickets) | — |

## 6. Release Stages

| Stage | Scope |
|---|---|
| **R0 — Bench POC** | Photometric-stereo capture (SS-A1), anomaly detection (SS-B1), on-device result display (SS-C8). Prove detection against expert. |
| **R1 — Pilot** | Full handheld device; capture quality gate, slab coverage, defect segmentation, fissure/crack discriminator, grading engine, local records, offline sync, reports, org/user/device management, grading profiles, consented data capture. |
| **R2 — Scale** | OTA signed model updates, buyer-shared report links, active-learning feedback loop, SLAs. |

## 7. Gates

- **G1:** Blind-test detection ≥ expert on agreed classes in controlled lighting.
- **G2:** Median per-slab workflow < 60 s; stable accuracy in real ambient light.
- **G3:** Field accuracy ≥ expert; ≥ 3 paying/renewing pilots; early buyer-side demand.

## 8. Key Technical Decisions

| Decision | Rationale |
|---|---|
| Anomaly-detection-first | Defects are rare/varied; train mostly on "good" stone — reduces labeled-data needs at R0 |
| Photometric stereo | Surface relief separates filled fissures from structural cracks cheaply |
| Offline-first edge inference | Yards/warehouses lack reliable connectivity; also protects latency and privacy |
| Signed model bundles + OTA | Proprietary models are the moat; must update safely in the field |
| ONNX → TensorRT / OpenVINO | Single training target, optimized per edge hardware at deploy time |
| DVC + MLflow | Reproducible data and model lineage for a data-flywheel product |
| Go backend | Matches ossb toolchain; efficient sync ingestion under high device concurrency |

## 9. Related Docs

| Doc | Path |
|---|---|
| PRD | [stone-defect-project-document/01-PRD-stonescan.md](stone-defect-project-document/01-PRD-stonescan.md) |
| Technical Architecture | [stone-defect-project-document/02-technical-architecture-stonescan.md](stone-defect-project-document/02-technical-architecture-stonescan.md) |
| Security & Access | [stone-defect-project-document/03-security-and-access-stonescan.md](stone-defect-project-document/03-security-and-access-stonescan.md) |
| Frontend Spec | [stone-defect-project-document/04-frontend-spec-stonescan.md](stone-defect-project-document/04-frontend-spec-stonescan.md) |
| Feature Tickets | [stone-defect-project-document/05-feature-tickets-stonescan.md](stone-defect-project-document/05-feature-tickets-stonescan.md) |
