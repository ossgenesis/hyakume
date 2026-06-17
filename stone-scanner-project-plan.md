# Project Plan — Stone Surface-Defect Scanner (POC → Validated Pilots)

*Building an AI-powered inspection product for natural-stone slabs (granite, marble, slate, quartzite) — surface grains, cracks, fissures and impurities. A thin **stereo + LiDAR** capture device streams **RGB-D** through a **mobile app** to **cloud inference**; sold as a subscription. Laying the reusable "engine" foundation for later visual-inspection verticals.*

> Assumptions: small founding team (1–4 people), bootstrap-to-pilot, ~6-month horizon. Budget and effort figures are illustrative planning ranges, not commitments or financial advice. The plan is gated — advance only when each gate's criteria are met.

---

## 1. Objective & definition of done

**North-star for this plan:** reach an evidence-backed go/no-go decision to scale or raise. "Done" means all four are true:

1. A **capture device + mobile app + cloud inference** that detects surface defects at or above an expert inspector on 3–4 stone types, in real (not just lab) lighting.
2. **3–5 paid pilots** showing the workflow fits and customers will pay the subscription.
3. A **proprietary labeled RGB-D stone dataset** plus a first written grading rubric (your moat seed).
4. The **engine documented for reuse** — capture spec, data/ML pipeline, cloud deploy path — so vertical #2 is cheaper to enter.

**Hard scope guardrails (resist drift):** surface defects only; stone only; **cloud inference only** (no on-device ML); no internal/subsurface (ultrasonic/X-ray) sensing; no second vertical until after the go/no-go gate. (The LiDAR here measures **surface** relief — it is not subsurface sensing.)

---

## 2. Workstreams

Seven parallel tracks run across the phases; each phase pulls different amounts from each.

| # | Workstream | Owns |
|---|---|---|
| W1 | Customer & market validation | Interviews, defect taxonomy (with customers), pilot recruitment, subscription pricing tests, buyer-side pull |
| W2 | Data | Capture protocol, sample sourcing, collection, annotation, RGB-D dataset versioning |
| W3 | ML / computer vision | RGB-D anomaly-detection baseline, supervised segmentation, fissure-vs-crack disambiguation (LiDAR relief), eval harness |
| W4 | Hardware & sensors | Stereo + LiDAR rig, camera/LiDAR selection, extrinsic calibration, handheld housing, capture board, battery |
| W5 | Software & app | Mobile app (capture relay + UI), cloud inference/grading services, pass/fail + heatmap UI, per-slab report/record, cloud archive |
| W6 | MLOps & infra | Training pipeline, experiment tracking, model registry, cloud serving on AKS (Terraform), drift monitoring |
| W7 | Business & ops | Positioning/IP basics, subscription pilot agreements, BOM/costing, fundraising-readiness |

---

## 3. Phases & gates

### Phase 0 — Discovery & setup *(≈ weeks 1–3)*
- **W1:** 15–25 structured interviews with factories/traders (and a few buyers); quantify annual reject/dispute losses in money. Lock 3+ design partners.
- **W1/W2:** define an initial defect taxonomy with 2–3 domain experts; this is a *commercial* decision (what counts as a reject) as much as a technical one.
- **W2:** acquire physical stone samples — good and defective — across 3–4 types.
- **W6:** stand up repos, dev environment, MLOps skeleton (DVC + MLflow), and a **cloud skeleton (AKS + GPU pool via Terraform)**; download open datasets (MCS, Marble Surface Anomaly Detection, Roboflow granite/marble, STI).
- **Gate G0 — proceed if:** pain is quantified and real, and ≥3 design partners have verbally committed to a pilot.

### Phase 1 — Bench POC *(≈ weeks 3–8)*
- **W4:** build a bench rig — **stereo camera + LiDAR** with a rigid mount; calibrate; capture registered **RGB-D** patches.
- **W2:** capture protocol v1; collect and annotate the first in-house RGB-D dataset in CVAT/Label Studio.
- **W3:** train an **RGB-D anomaly-detection baseline** (Anomalib — PatchCore/EfficientAd) on *good* stone; add supervised segmentation (YOLO-seg / U-Net / SAM 2) for named defects using open + own data; serve it in the cloud.
- **W3:** build a reproducible **eval harness**; run a blind test — scanner vs. expert vs. ground truth on 100+ patches/slabs.
- **Gate G1 — proceed if:** detection meets or beats the expert on agreed defect classes under controlled lighting.

### Phase 2 — Capture device + mobile + cloud *(≈ weeks 8–16)*
- **W4:** integrate stereo camera + LiDAR + capture board + battery into a 3D-printed handheld housing (the phone is the screen — no on-device compute).
- **W6/W5:** stand up the **cloud inference + grading services** on the GPU pool (warm node + scale-to-zero); wire the mobile app → cloud round-trip.
- **W5:** mobile app with pass/fail + defect **heatmap** UI; generate a per-slab, timestamped **record** (RGB-D + grade) stored in the cloud.
- **W4:** field-harden — sensor calibration/registration discipline, ergonomics, and the scan workflow (decide patch-by-patch vs. sweep-and-stitch).
- **W1:** internal field test in a real yard / loading bay (with live connectivity).
- **Gate G2 — proceed if:** sub-minute per-slab workflow, stable accuracy in real ambient light, device robust enough to hand to a stranger.

### Phase 3 — Paid pilots & validation *(≈ weeks 16–26)*
- **W1/W7:** deploy to 3–5 design partners under **paid** subscription pilots; offer an inspection-as-a-service option to earn revenue and harvest training data simultaneously.
- **W3/W6:** iterate the model via active learning on pilot data; redeploy improved model images to the cluster; tune per-customer thresholds (especially fissure vs. structural crack).
- **W1:** measure dispute/reject rate vs. each customer's baseline; test subscription pricing (device-bundled subscription vs. rental vs. per-scan); run the **buyer-side pull** experiment (get 1–2 importers to value the report).
- **W3–W6:** document the **engine** (capture spec, labeling pipeline, training recipe, cloud deploy steps) for vertical reuse.
- **Gate G3 (GO / NO-GO) — scale or raise if:** field accuracy ≥ expert, ≥3 paying and renewing pilots, and early buyer-side demand for the scan report.

---

## 4. Team & roles

| Role | Focus | If solo/tiny team |
|---|---|---|
| ML / CV engineer | W3, W6 | Core hire; hardest to outsource |
| Hardware / embedded + sensors | W4 | Contract or partner for housing/electronics; stereo + LiDAR calibration know-how is a crown jewel — keep in-house |
| Full-stack / mobile + cloud | W5 | Mobile app + cloud services; can be part-time until Phase 2 |
| Founder / BD | W1, W7 | You — customer dev is non-delegable early |
| Domain expert (stone grader) | advisory across W1–W3 | Paid advisor; defines "reject" and validates the model |

Minimum-viable solo path: run phases more sequentially, contract the hardware build, and lean on open datasets + anomaly detection to limit how much labeling you need before G1.

---

## 5. Tech stack

- **CV / ML:** Python, PyTorch, Anomalib, Ultralytics YOLO, SAM 2, OpenCV; RGB-D (open3d for depth/point clouds).
- **Annotation:** CVAT or Label Studio.
- **MLOps:** DVC (data/model versioning), MLflow or Weights & Biases (experiments), a simple model registry.
- **Cloud serving:** ONNX Runtime-GPU / Triton behind a FastAPI/gRPC service on **AKS** GPU node pools (NVIDIA A10); **Terraform** IaC; reserved GPU capacity optional.
- **Device:** stereo camera + LiDAR capture board streaming RGB-D to the phone (no on-device inference).
- **App / cloud:** mobile app (e.g. Flutter) + Go backend (services) + cloud object archive; optional in-cluster lightweight LLM for report summaries.
- **Datasets to seed from:** Marble Crack Segmentation (MCS), Marble Surface Anomaly Detection, Roboflow granite/marble/slate sets, STI stone-texture set, plus MVTec AD for pipeline benchmarking.

---

## 6. Prototype bill of materials (rough, single unit)

| Item | Notes |
|---|---|
| Stereo camera (or dual cameras) | Global shutter; 5–12 MP; provides RGB + stereo depth |
| LiDAR module | Solid-state / ToF depth sensor for surface relief; registered to the camera |
| Capture board | Lightweight embedded board: drives sensors, registers RGB-D, streams to phone (no GPU inference) |
| Battery + power management | Sized for a working session (capture-only draws less than edge compute) |
| Housing + fasteners | 3D-printed enclosure, trigger button (the phone is the screen) |

Order-of-magnitude: low-to-mid hundreds of USD for one prototype unit, falling with volume. Ongoing **cloud GPU** cost (AKS A10, scale-to-zero) is the recurring infra line. The dominant cost in this whole plan is **people-time**, not parts.

---

## 7. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Fissure vs. structural crack confusion (marble) | LiDAR surface-relief features; per-customer tunable thresholds; expert-in-the-loop through pilots |
| Field connectivity gaps (cloud inference) | Mobile capture queue + retry; warm GPU for low latency; reserved GPU capacity option |
| Ambient lighting in real yards | RGB-D capture is less light-dependent than flat imaging; validate explicitly in Phase 2 field test |
| Sensor calibration drift (stereo + LiDAR) | On-device registration checks; capture quality gate; pre-session calibration routine |
| Scarce labeled defect data | Anomaly-detection-first (train on "good"); harvest data via inspection-as-a-service in Phase 3 |
| Customers see manual inspection as "good enough" | Sell the documentation / dispute-evidence value, not just detection accuracy |
| Generalization across many stone types | Start narrow (3–4 types); expand only after G1/G3 |
| Scope creep (internal defects, 3D, vertical #2) | Hard guardrails in §1; gates block premature spend |

---

## 8. Budget framing (illustrative buckets)

Not a forecast — buckets to fill with real quotes. Keep each as a range and revisit at every gate.
- Prototype hardware (a few units across iterations)
- Compute & cloud (training + **GPU inference serving** + archive)
- Data & annotation (labeling time/tools, possibly outsourced labeling)
- Physical stone samples
- Software tools / licenses
- Customer-development travel
- People (the largest and most variable line)

---

## 9. Decision-gate summary (the spine of the plan)

| Gate | When | Must be true to proceed |
|---|---|---|
| G0 | end Phase 0 | Pain quantified + ≥3 design partners committed |
| G1 | end Phase 1 | Detection ≥ expert on agreed classes (controlled lighting) |
| G2 | end Phase 2 | Sub-minute workflow + robust in real lighting |
| G3 | end Phase 3 | Field accuracy ≥ expert + ≥3 paying/renewing pilots + buyer pull → **scale/raise** |

If a gate fails, the move is to fix or pivot *within that phase* — not to spend forward on faith.

---

## 10. Immediate next two weeks

1. Draft the interview script and line up the first 10 customer conversations (W1).
2. Source physical stone samples — good and defective — across 3–4 types (W2).
3. Stand up the repo, DVC + MLflow skeleton, and the AKS + GPU pool skeleton via Terraform; pull the open datasets (W6).
4. Get a stereo camera + LiDAR on the bench, calibrate, and capture a first batch of registered RGB-D images (W4/W2).
5. Run an Anomalib PatchCore baseline on the open marble/granite data to feel the pipeline end-to-end before your own data lands (W3).
