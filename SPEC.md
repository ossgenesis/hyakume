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

Cloud-inference design: `device (stereo + LiDAR) → mobile app → cloud (AKS) → result to mobile/web`. Four parts: **capture unit** (thin device, RGB-D capture only), **mobile app** (relay + operator UI), **cloud backend on Kubernetes** (inference + grading + management + reports), and **MLOps pipeline** (train → deploy model image to the cluster). The device runs no inference.

See [stone-defect-project-document/02-technical-architecture-stonescan.md](stone-defect-project-document/02-technical-architecture-stonescan.md) and [diagram/system-overview.mmd](diagram/system-overview.mmd).

## 5. Component Map

| Directory | What it is | Language / Framework |
|---|---|---|
| `edge/` | Capture-unit firmware: stereo + LiDAR RGB-D capture only | Python |
| `backend/` | Cloud API + services: org, user, device, scan, profile, report; hosts inference + grading | Go (services), Python (model serving) |
| `dashboard/` | Web SPA: search, scan detail, reports, management | React / TypeScript |
| `mlops/` | Training, eval, active-learning loop (RGB-D models) | Python (Anomalib, Ultralytics, DVC, MLflow) |
| `deploy/` | Infrastructure-as-code: Terraform (AKS + GPU pools), k8s manifests, Docker | YAML / HCL |
| `diagram/` | Architecture diagrams (Mermaid) | — |
| `stone-defect-project-document/` | Design documents (PRD, architecture, security, frontend spec, tickets) | — |

## 6. Release Stages

| Stage | Scope |
|---|---|
| **R0 — Bench POC** | Stereo + LiDAR capture (SS-A1), cloud RGB-D anomaly detection (SS-B1), result on mobile/web (SS-C8). Prove detection against expert. |
| **R1 — Pilot** | Full capture device + mobile app; capture quality gate, slab coverage, cloud defect segmentation, fissure/crack discriminator, cloud grading, records, reports, org/user/device management, grading profiles, consented data capture. |
| **R2 — Scale** | Buyer-shared report links, active-learning feedback loop, in-cluster LLM features, SLAs. |

## 7. Gates

- **G1:** Blind-test detection ≥ expert on agreed classes in controlled lighting.
- **G2:** Median per-slab workflow < 60 s; stable accuracy in real ambient light.
- **G3:** Field accuracy ≥ expert; ≥ 3 paying/renewing pilots; early buyer-side demand.

## 8. Key Technical Decisions

| Decision | Rationale |
|---|---|
| Anomaly-detection-first | Defects are rare/varied; train mostly on "good" stone — reduces labeled-data needs at R0 |
| Stereo + LiDAR (RGB-D) | Real 3D surface relief separates filled fissures from structural cracks; commodity sensor, no LED rig |
| Cloud inference (thin device) | Device stays cheap/replaceable; models iterate centrally with no OTA; GPUs unconstrained by an edge budget |
| Subscription model | Device bundled with service; moat is the RGB-D dataset + dashboard/inference, not the hardware |
| AKS + GPU node pools | Free control plane runs 24/7; GPU pools scale to zero when idle; all infra via Terraform |
| DVC + MLflow | Reproducible data and model lineage for a data-flywheel product |
| Go backend | Efficient ingestion under high device concurrency; Python sidecar serves the models |

> **Note:** requires connectivity at inspection time — the original offline-first guarantee is intentionally traded away for the thin-device / cloud-inference model.

## 9. Related Docs

| Doc | Path |
|---|---|
| PRD | [stone-defect-project-document/01-PRD-stonescan.md](stone-defect-project-document/01-PRD-stonescan.md) |
| Technical Architecture | [stone-defect-project-document/02-technical-architecture-stonescan.md](stone-defect-project-document/02-technical-architecture-stonescan.md) |
| Security & Access | [stone-defect-project-document/03-security-and-access-stonescan.md](stone-defect-project-document/03-security-and-access-stonescan.md) |
| Frontend Spec | [stone-defect-project-document/04-frontend-spec-stonescan.md](stone-defect-project-document/04-frontend-spec-stonescan.md) |
| Feature Tickets | [stone-defect-project-document/05-feature-tickets-stonescan.md](stone-defect-project-document/05-feature-tickets-stonescan.md) |
