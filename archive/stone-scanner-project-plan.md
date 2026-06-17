# Project Plan — Handheld Stone Surface-Defect Scanner (POC → Validated Pilots)

*Building a portable, AI-powered device that inspects natural-stone slabs (granite, marble, slate, quartzite) for surface grains, cracks, fissures and impurities — and laying the reusable "engine" foundation for later visual-inspection verticals.*

> Assumptions: small founding team (1–4 people), bootstrap-to-pilot, ~6-month horizon. Budget and effort figures are illustrative planning ranges, not commitments or financial advice. The plan is gated — advance only when each gate's criteria are met.

---

## 1. Objective & definition of done

**North-star for this plan:** reach an evidence-backed go/no-go decision to scale or raise. "Done" means all four are true:

1. A **handheld prototype** that detects surface defects at or above an expert inspector on 3–4 stone types, in real (not just lab) lighting.
2. **3–5 paid pilots** showing the workflow fits and customers will pay.
3. A **proprietary labeled stone dataset** plus a first written grading rubric (your moat seed).
4. The **engine documented for reuse** — capture-rig spec, data/ML pipeline, deploy path — so vertical #2 is cheaper to enter.

**Hard scope guardrails (resist drift):** surface defects only; handheld only; stone only. No internal/ultrasonic, no LiDAR, no second vertical until after the go/no-go gate.

---

## 2. Workstreams

Seven parallel tracks run across the phases; each phase pulls different amounts from each.

| # | Workstream | Owns |
|---|---|---|
| W1 | Customer & market validation | Interviews, defect taxonomy (with customers), pilot recruitment, pricing tests, buyer-side pull |
| W2 | Data | Capture protocol, sample sourcing, collection, annotation, dataset versioning |
| W3 | ML / computer vision | Anomaly-detection baseline, supervised segmentation, fissure-vs-crack disambiguation, eval harness |
| W4 | Hardware & optics | Lighting/shroud, photometric-stereo rig, camera selection, handheld housing, edge compute, battery, screen |
| W5 | Software & app | Capture app, on-device inference, pass/fail + heatmap UI, per-slab report/record, cloud sync/archive |
| W6 | MLOps & infra | Training pipeline, experiment tracking, model registry, edge export/quantization, drift monitoring |
| W7 | Business & ops | Positioning/IP basics, pilot agreements, BOM/costing, fundraising-readiness |

---

## 3. Phases & gates

### Phase 0 — Discovery & setup *(≈ weeks 1–3)*
- **W1:** 15–25 structured interviews with factories/traders (and a few buyers); quantify annual reject/dispute losses in money. Lock 3+ design partners.
- **W1/W2:** define an initial defect taxonomy with 2–3 domain experts; this is a *commercial* decision (what counts as a reject) as much as a technical one.
- **W2:** acquire physical stone samples — good and defective — across 3–4 types.
- **W6:** stand up repos, dev environment, MLOps skeleton (DVC + MLflow), download open datasets (MCS, Marble Surface Anomaly Detection, Roboflow granite/marble, STI).
- **Gate G0 — proceed if:** pain is quantified and real, and ≥3 design partners have verbally committed to a pilot.

### Phase 1 — Bench POC *(≈ weeks 3–8)*
- **W4:** build a bench rig — single machine-vision camera + a **light hood** that blocks ambient light; add a switchable LED ring for **photometric stereo** (multi-angle capture).
- **W2:** capture protocol v1; collect and annotate the first in-house dataset in CVAT/Label Studio.
- **W3:** train an **anomaly-detection baseline** (Anomalib — PatchCore for accuracy, EfficientAd for edge speed) on *good* stone; add supervised segmentation (YOLO-seg / U-Net / SAM 2) for named defects using open + own data.
- **W3:** build a reproducible **eval harness**; run a blind test — scanner vs. expert vs. ground truth on 100+ patches/slabs.
- **Gate G1 — proceed if:** detection meets or beats the expert on agreed defect classes under controlled lighting.

### Phase 2 — Handheld prototype *(≈ weeks 8–16)*
- **W4:** integrate camera + LED ring + Jetson Orin Nano (or a phone) + battery + power management + screen into a 3D-printed handheld housing.
- **W6/W5:** quantize and export the model (ONNX → OpenVINO/TensorRT); run **on-device inference**.
- **W5:** pass/fail + defect **heatmap** UI; generate a per-slab, timestamped **record** (image + grade); cloud sync/archive.
- **W4:** field-harden — shroud/contact discipline for lighting, ergonomics, and the scan workflow (decide patch-by-patch vs. sweep-and-stitch).
- **W1:** internal field test in a real yard / loading bay.
- **Gate G2 — proceed if:** sub-minute per-slab workflow, stable accuracy in real ambient light, device robust enough to hand to a stranger.

### Phase 3 — Paid pilots & validation *(≈ weeks 16–26)*
- **W1/W7:** deploy to 3–5 design partners under **paid** pilot agreements; offer an inspection-as-a-service option to earn revenue and harvest training data simultaneously.
- **W3/W6:** iterate the model via active learning on pilot data; tune per-customer thresholds (especially fissure vs. structural crack).
- **W1:** measure dispute/reject rate vs. each customer's baseline; test pricing (hardware+subscription vs. rental vs. per-scan); run the **buyer-side pull** experiment (get 1–2 importers to value the report).
- **W3–W6:** document the **engine** (capture-rig spec, labeling pipeline, training recipe, deploy steps) for vertical reuse.
- **Gate G3 (GO / NO-GO) — scale or raise if:** field accuracy ≥ expert, ≥3 paying and renewing pilots, and early buyer-side demand for the scan report.

---

## 4. Team & roles

| Role | Focus | If solo/tiny team |
|---|---|---|
| ML / CV engineer | W3, W6 | Core hire; hardest to outsource |
| Hardware / embedded + optics | W4 | Contract or partner for housing/electronics; lighting know-how is the crown jewel — keep in-house |
| Full-stack / app dev | W5 | Can be part-time until Phase 2 |
| Founder / BD | W1, W7 | You — customer dev is non-delegable early |
| Domain expert (stone grader) | advisory across W1–W3 | Paid advisor; defines "reject" and validates the model |

Minimum-viable solo path: run phases more sequentially, contract the hardware build, and lean on open datasets + anomaly detection to limit how much labeling you need before G1.

---

## 5. Tech stack

- **CV / ML:** Python, PyTorch, Anomalib, Ultralytics YOLO, SAM 2, OpenCV.
- **Annotation:** CVAT or Label Studio.
- **MLOps:** DVC (data/model versioning), MLflow or Weights & Biases (experiments), a simple model registry.
- **Edge / deploy:** ONNX → OpenVINO / TensorRT; Jetson Orin Nano (or on-device mobile inference).
- **App / cloud:** lightweight mobile/embedded UI; FastAPI/BentoML for any cloud reporting + the per-slab archive.
- **Datasets to seed from:** Marble Crack Segmentation (MCS), Marble Surface Anomaly Detection, Roboflow granite/marble/slate sets, STI stone-texture set, plus MVTec AD for pipeline benchmarking.

---

## 6. Prototype bill of materials (rough, single unit)

| Item | Notes |
|---|---|
| Machine-vision camera | Global shutter; 5–12 MP; or a recent phone camera for the earliest POC |
| LED ring + driver | Multi-angle, switchable, for photometric stereo |
| Light hood / shroud | 3D-printed; blocks ambient light — the highest-leverage part |
| Edge compute | Jetson Orin Nano dev kit (or phone) |
| Battery + power management | Sized for a working session |
| Screen / touch display | Pass/fail + heatmap readout |
| Housing + fasteners | 3D-printed enclosure, trigger button |

Order-of-magnitude: low-to-mid hundreds of USD for one prototype unit, falling with volume. The dominant cost in this whole plan is **people-time**, not parts.

---

## 7. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Fissure vs. structural crack confusion (marble) | Photometric stereo for surface relief; per-customer tunable thresholds; expert-in-the-loop through pilots |
| Ambient lighting in real yards | Shrouded/contact capture head; validate explicitly in Phase 2 field test |
| Scarce labeled defect data | Anomaly-detection-first (train on "good"); harvest data via inspection-as-a-service in Phase 3 |
| Customers see manual inspection as "good enough" | Sell the documentation / dispute-evidence value, not just detection accuracy |
| Generalization across many stone types | Start narrow (3–4 types); expand only after G1/G3 |
| Scope creep (internal defects, 3D, vertical #2) | Hard guardrails in §1; gates block premature spend |
| Willingness-to-pay uncertainty | Paid pilots and rental lower the barrier and are a stronger signal than free trials |

---

## 8. Budget framing (illustrative buckets)

Not a forecast — buckets to fill with real quotes. Keep each as a range and revisit at every gate.
- Prototype hardware (a few units across iterations)
- Compute & cloud (training + archive)
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
3. Stand up the repo, DVC + MLflow skeleton, and pull the open datasets (W6).
4. Get a basic light hood + one camera on the bench and capture a first batch of images under multiple light angles (W4/W2).
5. Run an Anomalib PatchCore baseline on the open marble/granite data to feel the pipeline end-to-end before your own data lands (W3).
