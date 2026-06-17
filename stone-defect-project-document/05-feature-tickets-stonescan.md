# Feature Ticket List — StoneScan

| | |
|---|---|
| **Status** | Draft v0.2 (cloud-inference pivot) |
| **Purpose** | Backlog of epics and tickets, traceable to PRD requirements |
| **Legend** | Pri: P0/P1/P2 · Rel: R0 bench POC, R1 pilot, R2 scale · Traces: PRD FR/NFR IDs |
| **Related docs** | PRD, Technical Architecture, Security & Access, Frontend Spec |

> Each ticket should be refined with full acceptance criteria, estimates, and owners before a sprint. IDs are stable references for cross-linking. Architecture: thin **stereo + LiDAR** capture device → **mobile app** → **cloud (AKS) inference/grading**.

---

## EPIC A — Capture (stereo + LiDAR)
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-A1 | RGB-D capture (stereo + LiDAR) | Capture a registered RGB-D patch (stereo RGB + LiDAR depth); stereo rectification + LiDAR→RGB registration | P0 | R0 | FR-C1 |
| SS-A2 | Sensor mount & extrinsic calibration | Rigid stereo + LiDAR mount; calibration routine aligns depth to RGB; validated against drift | P0 | R1 | FR-C1, NFR-6 |
| SS-A3 | Viewfinder + one-tap trigger (mobile) | Live preview in app, capture < 2 s, ≤ 2 taps to scan | P0 | R1 | FR-C2, NFR-3, NFR-10 |
| SS-A4 | Capture quality gate | Detect blur/under-exposure/bad registration; prompt retake | P1 | R1 | FR-C5 |
| SS-A5 | Slab coverage tracking | Guide operator across the slab; show covered/uncovered | P1 | R1 | FR-C4 |
| SS-A6 | Calibration check routine | Pre-session stereo + LiDAR calibration check | P1 | R1 | NFR-6 |

## EPIC B — ML detection & grading (cloud)
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-B1 | Anomaly-detection baseline (RGB-D) | Anomalib PatchCore/EfficientAd on RGB-D flags deviation from "good"; eval on open + own data | P0 | R0 | FR-D1, NFR-1 |
| SS-B2 | Eval harness & blind test | Reproducible metrics (precision/recall, image/pixel AUROC); scanner vs expert vs ground truth | P0 | R0 | NFR-1 |
| SS-B3 | Defect segmentation & classification | Localize+label crack/fissure/pit/stain/chip/impurity | P0 | R1 | FR-D2 |
| SS-B4 | Fissure-vs-crack discriminator | Use **LiDAR depth / surface relief** to separate filled fissures from structural cracks | P0 | R1 | FR-D3 |
| SS-B5 | Grading service | Apply grading-profile thresholds → pass/fail + grade tier (cloud service) | P0 | R1 | FR-D4 |
| SS-B6 | Per-defect confidence & location | Return confidence + bbox/mask per defect | P1 | R1 | FR-D5 |
| SS-B7 | Stone-type routing | Select model/profile by stone type (manual + auto) | P1 | R1 | FR-D6 |
| SS-B8 | Model serving image (GPU) | Package model as a container image; serve via ONNX Runtime-GPU / Triton; meet warm-GPU latency | P0 | R1 | NFR-2 |

## EPIC C — Capture device firmware & mobile app
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-C1 | Capture controller (firmware) | Drives stereo + LiDAR capture; handles registration + retakes | P0 | R0 | FR-C1 |
| SS-C2 | Preprocessing (device/phone) | Stereo rectification + LiDAR→RGB registration before upload | P0 | R1 | FR-C1 |
| SS-C3 | Mobile app: capture + result | Pair device, relay captures to cloud, display result/heatmap | P0 | R1 | FR-C6, FR-R1 |
| SS-C4 | Mobile upload queue | Queue captures on connectivity drop; retry; no data loss | P0 | R1 | FR-S1 |
| SS-C5 | Device firmware update | Signed firmware update + rollback (no model bundles on device) | P1 | R2 | sec §3 |

## EPIC D — Records & reporting
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-D1 | Mobile result view | Pass/fail + heatmap overlay + defect list (in app) | P0 | R0 | FR-R1 |
| SS-D2 | Per-slab record (cloud) | Persist RGB-D captures, heatmap, defects, grade, versions, timestamp, operator, device | P0 | R1 | FR-R2 |
| SS-D3 | PDF report export | Generate shipment-ready report | P1 | R1 | FR-R3 |
| SS-D4 | Record integrity hash | Tamper-evident hash over record contents; verifiable | P1 | R1 | FR-R4 (sec §5) |
| SS-D5 | Buyer-shared report | Scoped, expiring read-only share link | P2 | R2 | FR-R5 |

## EPIC E — Connectivity & upload
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-E1 | Upload queue + retry | Queue records on drop; upload on reconnect; no data loss | P0 | R1 | FR-S1 |
| SS-E2 | Upload status UI | Pending/last-sync/retry; connection-honest messaging | P0 | R1 | FR-S1 |
| SS-E3 | Firmware OTA (signed) | Device pulls + verifies signed firmware updates | P2 | R2 | sec §3 |

## EPIC F — Cloud backend, inference & data model
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-F1 | Core data model & migrations | Entities per Architecture §5 (RGB-D refs) | P0 | R1 | — |
| SS-F2 | Ingestion API | Authenticated capture/record upload; tenant-scoped | P0 | R1 | FR-S1, sec §6 |
| SS-F3 | Object storage integration | Store RGB-D captures/heatmaps/PDFs encrypted at rest | P0 | R1 | sec §4 |
| SS-F4 | Report service | Render PDF + compute integrity hash | P1 | R1 | FR-R3/R4 |
| SS-F5 | Model registry + cluster deploy | Versioned model images; deploy to GPU node pool (no signing/OTA) | P1 | R1 | FR-S6 |
| SS-F6 | Search/index for scans | Filterable queries at scale | P0 | R1 | FR-S2, NFR-8 |
| SS-F7 | GPU inference service | Serve anomaly+seg+discriminator pipeline behind the API on the GPU pool; warm node + scale-to-zero | P0 | R1 | FR-D1–D3, NFR-2/8 |
| SS-F8 | Cloud infra (AKS via Terraform) | AKS + CPU/GPU node pools (warm + spot), object storage, Postgres, registry — all via Terraform | P0 | R1 | NFR-7/8 |

## EPIC G — Web dashboard
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-G1 | Auth + RBAC gating | Sign-in, MFA for admin, role-gated views | P0 | R1 | sec §2 |
| SS-G2 | Overview/KPIs | Pass rate, defect breakdown, dispute trend, devices online | P1 | R1 | FR-S2 |
| SS-G3 | Slabs & scans browse/search | Filter + thumbnails + grade | P0 | R1 | FR-S2 |
| SS-G4 | Scan/slab detail | RGB-D + heatmap viewer, defects, export | P0 | R1 | FR-R1/R3 |
| SS-G5 | Grading-profile editor | Create/edit/version profiles per stone/customer | P0 | R1 | FR-S5 |
| SS-G6 | Device management | Enroll/status/revoke, firmware rollout view | P1 | R1 | FR-S4 |
| SS-G7 | User & role management | Invite, assign roles, remove | P0 | R1 | FR-S3 |
| SS-G8 | Org settings + data-opt-in | Profile, retention, data-opt-in toggle, subscription/billing | P0 | R1 | FR-S7/S9, sec §4 |

## EPIC H — Identity, access & security
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-H1 | User auth + MFA | Email/SSO; MFA enforced for Owner/Admin | P0 | R1 | sec §2.3 |
| SS-H2 | Device identity & enrollment | Unique credential; pairs with app; relayed auth; revocation | P0 | R1 | sec §3 |
| SS-H3 | Tenant isolation enforcement | All access scoped by org_id; tests prove no cross-tenant leakage | P0 | R1 | sec §6 |
| SS-H4 | Encryption in transit & at rest | TLS everywhere; encrypted storage + transient device buffer | P0 | R1 | sec §4 |
| SS-H5 | Audit logging | Security-relevant events logged, tamper-evident | P1 | R1 | sec §7 |
| SS-H6 | Firmware signing infrastructure | Sign + verify device firmware artifacts | P1 | R2 | sec §3 |
| SS-H7 | Data deletion / retention controls | Honor per-org/per-record deletion + retention policy | P1 | R2 | sec §4.3 |

## EPIC I — MLOps & data flywheel
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-I1 | Dataset versioning (DVC) | Versioned RGB-D datasets over object storage | P0 | R0 | — |
| SS-I2 | Annotation pipeline | CVAT/Label Studio workflow; export to training format | P0 | R0 | FR-D2 |
| SS-I3 | Training + experiment tracking | Anomalib/YOLO RGB-D training logged to MLflow; deploy model image to cluster | P0 | R1 | NFR-1 |
| SS-I4 | Consented data ingestion | Opt-in field scans flow into training store | P0 | R1 | FR-S7 |
| SS-I5 | Operator-correction → label | "Flag as wrong" feeds active-learning queue | P1 | R2 | FR-S8 |
| SS-I6 | Drift monitoring | Alert on input-distribution / accuracy-proxy drift | P1 | R2 | NFR-1 |
| SS-I7 | Engine documentation | Capture spec, pipeline, deploy steps documented for vertical reuse | P1 | R1 | strategy |
| SS-I8 | In-cluster LLM (optional) | Lightweight LLM on spot GPU pool for report summaries / operator Q&A | P2 | R2 | strategy |

## EPIC J — Hardware integration & device
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-J1 | Bench rig assembly | Stereo camera + LiDAR on a bench for R0 | P0 | R0 | FR-C1 |
| SS-J2 | Capture board integration | Embedded capture board streams RGB-D to the phone (no on-device inference) | P0 | R1 | FR-C6 |
| SS-J3 | Handheld housing | Enclosure, trigger, battery; pairs with phone (phone is the screen) | P0 | R1 | NFR-5 |
| SS-J4 | Power management | ≥ 6 h continuous capture session | P1 | R1 | NFR-5 |
| SS-J5 | Field-hardening | Robust in dusty/bright bay; ergonomics validated | P1 | R1 | NFR-6 |

## EPIC K — Validation & ops (non-engineering)
| ID | Title | Description / acceptance | Pri | Rel | Traces |
|---|---|---|---|---|---|
| SS-K1 | Customer interviews | 15–25 interviews; reject/dispute losses quantified | P0 | R0 | gate G0 |
| SS-K2 | Defect taxonomy w/ expert | Agreed class list + reject definitions | P0 | R0 | FR-D2/D4 |
| SS-K3 | Sample sourcing | Good + defective samples across 3–4 stone types | P0 | R0 | NFR-1 |
| SS-K4 | Paid pilot agreements | 3–5 design partners under paid pilots | P0 | R1 | gate G3 |
| SS-K5 | Buyer-pull experiment | 1–2 importers value the scan report | P1 | R1 | gate G3 |
| SS-K6 | Pricing / subscription experiment | Validate device-bundled subscription pricing (vs rental / per-scan) | P1 | R1 | gate G3, FR-S9 |

---

## Suggested ordering by gate
- **To G1 (R0):** SS-K1/K2/K3, SS-I1/I2, SS-A1, SS-C1, SS-B1/B2, SS-D1, SS-J1, SS-F8 (infra bootstrap).
- **To G2 (R1 core):** SS-A2/A3, SS-B3/B4/B5/B8, SS-C2/C3/C4, SS-F2/F7, SS-J2/J3/J5, SS-D2, SS-E1/E2.
- **To G3 (R1 validation):** SS-F1/F3/F4/F5/F6, SS-G1/G3/G4/G5/G7/G8, SS-H1–H5, SS-I3/I4, SS-D3/D4, SS-K4/K5/K6.
- **R2 scale:** SS-C5, SS-D5, SS-E3, SS-H6/H7, SS-G2/G6, SS-I5/I6/I8.
