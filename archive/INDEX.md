# Archive — pre-pivot documents (v1, edge-inference design)

These are the **original** StoneScan design documents from before the
**cloud-inference pivot** (June 2026). They describe the superseded architecture:
a smart handheld **edge device** running on-device inference with **photometric
stereo** capture, **Jetson** compute, and **signed-OTA** model bundles.

They are kept here for historical reference and provenance only. **Do not build
from these.** The current, authoritative documents live in their normal
locations at the repo root and under `stone-defect-project-document/`.

## Current vs. archived

| Topic | Current (authoritative) | Archived (this folder) |
|---|---|---|
| Architecture | thin **stereo + LiDAR** device → mobile app → **cloud (AKS)** inference | smart edge device, on-device inference |
| Capture | RGB-D (stereo + LiDAR) | photometric stereo (LED ring) |
| Models | served in-cluster (container images) | signed-OTA bundles to devices |
| Business | subscription (device bundled with service) | hardware + later subscription |

## Contents (as committed before the pivot)

- `README.md`, `SPEC.md`, `stone-scanner-project-plan.md`
- `diagram/system-overview.mmd`, `diagram/data-flow.mmd`
- `stone-defect-project-document/01..05` (PRD, architecture, security, frontend, tickets)
