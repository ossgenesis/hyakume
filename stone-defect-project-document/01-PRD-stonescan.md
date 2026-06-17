# Product Requirements Document — StoneScan

| | |
|---|---|
| **Product** | StoneScan (working codename) — stone surface-defect inspection: a thin stereo + LiDAR capture device + mobile app + cloud inference, sold as a subscription |
| **Status** | Draft v0.2 (cloud-inference pivot) |
| **Owner** | Founder / Product |
| **Related docs** | Technical Architecture, Security & Access, Frontend Spec, Feature Tickets |

---

## 1. Overview & problem

Small and mid-size stone factories, processors and traders inspect slab surfaces **manually** before shipment. This is subjective, inconsistent, slow, and produces no objective record — leading to rejected shipments, buyer disputes, and repeated per-consignment third-party inspection costs. Existing automated inspection is large, fixed, inline machine vision built for big production lines and cannot serve a trader's warehouse or a buyer's receiving dock.

StoneScan is a **handheld, surface-only** system: an operator sweeps a thin **stereo + LiDAR capture unit** across a slab; the capture (RGB + depth) streams through a **mobile app** to the **cloud**, which returns a pass/fail grade, a defect heatmap, and a timestamped per-slab record that both buyer and seller can trust.

## 2. Strategic context

StoneScan is the **wedge** for a broader "vertical AI for visual inspection" company. The moat is **not the hardware** — it is the proprietary stone-defect **RGB-D dataset** and an accepted **grading standard**, delivered as a **subscription** (the device is bundled with the service and is a commodity: cheap, replaceable, upgradeable). Every product decision should favour accumulating clean labeled data and producing a defensible, shareable grade. The capture/cloud-inference stack is designed as a reusable **engine** for later surface-QC verticals (tiles, glass, wood, metal, precast concrete).

## 3. Goals & non-goals

**Goals**
- Detect surface grains, cracks, fissures, pits, stains and impurities on granite, marble, slate and quartzite.
- Match or beat an expert inspector's accuracy on agreed defect classes.
- Sub-minute inspection workflow per slab in real yard/warehouse lighting.
- Produce a tamper-evident per-slab record and exportable report.
- Continuously grow a proprietary labeled **RGB-D** dataset from consented field use.
- Iterate models centrally (cloud) so every device improves without hardware changes.

**Non-goals (this product cycle)**
- Internal/subsurface defects (no ultrasonic or X-ray; the LiDAR here measures **surface** relief only).
- Dimensional metrology / flatness as a primary feature.
- Any second vertical before the go/no-go gate (G3).
- A fully autonomous fixed/inline line system.
- On-device inference / offline operation (inference is cloud-side by design).

## 4. Personas

| Persona | Context | Primary need |
|---|---|---|
| **QC Operator** (Maya) | Works the grading/loading bay; dusty, bright/variable light; limited tech comfort | Scan fast, one hand, clear pass/fail |
| **Factory/Trader Owner** (Rahul) | Runs an export-oriented SME; feels reject/dispute costs | Reduce rejects, prove quality, manage devices/users, pay per subscription |
| **Buyer / Importer** (external) | Receives slabs abroad; wants independent verification | Trusted, tamper-evident scan report per slab |
| **Inspection-firm Operator** (partner) | Scans on behalf of clients (inspection-as-a-service) | Reliable device + certified reports across many sites |

## 5. Use cases / user stories

- As a **QC Operator**, I sweep the device over a slab and within a second or two see pass/fail with a defect heatmap returned from the cloud, so I can sort slabs without expert judgment.
- As a **QC Operator**, if the network drops mid-session, captures queue on my phone and upload automatically when the connection returns.
- As an **Owner**, I configure what counts as a reject for a given customer (grading profile), so grading matches each buyer's tolerance.
- As an **Owner**, I export a per-slab report to send with a shipment as quality evidence.
- As a **Buyer**, I open a shared scan report and verify it is authentic and unaltered.
- As an **Inspection-firm Operator**, I manage many devices and produce consistent certified reports across sites.
- As the **company**, consented scans flow back as labeled training data to improve the cloud models for everyone.

## 6. Functional requirements

Priority: **P0** = required for the release it's tagged to; **P1** = important; **P2** = later. Release: R0 bench POC, R1 pilot, R2 scale.

### 6.1 Capture (device + mobile app)
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-C1 | Capture a registered **RGB-D** frame of a slab patch (stereo RGB + LiDAR depth), with stereo rectification and LiDAR→RGB registration | P0 | R0 |
| FR-C2 | Live viewfinder with one-tap trigger; capture in < 2 s per patch | P0 | R1 |
| FR-C3 | Robust capture in variable ambient light (LiDAR depth + stereo reduce lighting dependence) | P0 | R1 |
| FR-C4 | Guide the operator to cover a full slab (patch sequence or sweep) and track coverage | P1 | R1 |
| FR-C5 | Reject blurred/under-exposed/poorly-registered captures with retake prompt | P1 | R1 |
| FR-C6 | Device pairs with the mobile app (BLE / USB / Wi-Fi) and streams captures to it | P0 | R1 |

### 6.2 Detection & grading (cloud)
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-D1 | Cloud anomaly detection flags surface regions deviating from "good" stone (RGB-D input) | P0 | R0 |
| FR-D2 | Cloud segments and classifies named defects: crack, fissure, pit, stain, chip, color/impurity | P0 | R1 |
| FR-D3 | Disambiguate harmless mineral-filled fissures from structural cracks using **LiDAR depth / surface-relief** cues | P0 | R1 |
| FR-D4 | Output a per-slab grade (pass/fail + grade tier) from a configurable grading profile | P0 | R1 |
| FR-D5 | Per-defect confidence and location returned with each result | P1 | R1 |
| FR-D6 | Stone-type selection or auto-detection to route to the right model/profile | P1 | R1 |

### 6.3 Results, records & reporting
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-R1 | Show pass/fail, defect heatmap overlay, and defect list in the mobile app (and web) | P0 | R0 |
| FR-R2 | Create a per-slab record: RGB-D captures, heatmap, defects, grade, timestamp, device, operator, profile version, model version | P0 | R1 |
| FR-R3 | Generate an exportable report (PDF) suitable to accompany a shipment | P1 | R1 |
| FR-R4 | Records are tamper-evident (integrity hash; see Security doc) | P1 | R1 |
| FR-R5 | Share a read-only report link/file with an external buyer | P2 | R2 |

### 6.4 Sync, management & learning
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-S1 | Mobile app uploads captures/records to the cloud over TLS; queue + retry if the connection drops | P0 | R1 |
| FR-S2 | Web dashboard: search/browse slabs and scans, view details, export | P0 | R1 |
| FR-S3 | Org/user management with roles (see Security doc RBAC) | P0 | R1 |
| FR-S4 | Device enrollment and management | P1 | R1 |
| FR-S5 | Configure grading profiles per org/customer | P0 | R1 |
| FR-S6 | Update cloud inference models centrally (cluster deploy) — no per-device updates | P1 | R1 |
| FR-S7 | Consented capture of field data into the training pipeline; per-org opt-in | P0 | R1 |
| FR-S8 | Operator correction/feedback on a result (active-learning label) | P1 | R2 |
| FR-S9 | Subscription/account management: device bundled with plan, renewal, entitlement | P1 | R1 |

## 7. Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-1 Accuracy | Detection quality on agreed classes | ≥ expert inspector; track precision/recall, image & pixel AUROC |
| NFR-2 Latency | Cloud inference per patch (warm GPU) | < 500 ms; end-to-end per patch incl. upload < 2 s |
| NFR-3 Throughput | End-to-end workflow per slab | < 60 s |
| NFR-4 Connectivity | Network required at inspection; graceful queue + retry on drop | No capture lost on transient drop |
| NFR-5 Battery | Continuous capture session (capture-only device) | ≥ 6 hours |
| NFR-6 Robustness | Operation in variable ambient light, dusty environment | Stable accuracy via RGB-D capture |
| NFR-7 Reliability | Cloud availability | 99.5% (R2) |
| NFR-8 Scalability | Slabs/scans stored & queryable; GPU inference autoscaling | Millions of records; scale-to-zero GPU off-hours |
| NFR-9 Security/Privacy | Per Security & Access Document | — |
| NFR-10 Usability | Taps to complete a scan | ≤ 2 |
| NFR-11 Localization | Operator (mobile) UI languages | English + 1 pilot-market language at R1 |

## 8. Success metrics (tied to project gates)

- **G1:** blind-test detection ≥ expert on agreed classes in controlled lighting.
- **G2:** median per-slab workflow < 60 s; stable accuracy in real ambient light.
- **G3:** field accuracy ≥ expert; ≥ 3 paying/renewing pilots; early buyer-side demand for the report.
- Ongoing: labeled RGB-D images accumulated per week; dispute/reject rate reduction vs. customer baseline.

## 9. Release scope

- **R0 (Bench POC):** FR-C1, FR-D1, FR-R1 on a tethered bench rig + cloud inference. Prove detection.
- **R1 (Pilot):** capture device + mobile app, full capture/detect/grade/record/report/sync/management, grading profiles, consented data capture, subscription/account management.
- **R2 (Scale):** buyer-shared reports, active-learning feedback loop, in-cluster LLM features, hardening and SLAs.

## 10. Dependencies & assumptions

- Access to physical stone samples (good + defective) across 3–4 types.
- Domain expert to define defect taxonomy and validate grading.
- Cloud GPU capacity (AKS A10 node pools; reserved capacity optional) for inference and training.
- Reliable-enough connectivity at inspection sites (the cloud-inference trade-off).
- Anomaly-detection-first approach reduces labeled-defect data needs early.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Fissure vs. structural crack confusion | LiDAR surface-relief features + tunable per-profile thresholds + expert-in-loop |
| Field connectivity gaps | Capture queue + retry on the phone; warm GPU to keep latency low; reserved GPU capacity option |
| Field lighting variability | RGB-D capture is less light-dependent; validate at G2 |
| Insufficient labeled data | Anomaly-first; harvest via consented capture and inspection-as-a-service |
| Generalization across stone types | Start with 3–4 types; expand post-gate |
| Sensor calibration drift (stereo + LiDAR) | On-device registration checks; capture quality gate (FR-C5) |
| Scope creep into internal/3D | Enforce non-goals |

## 12. Out of scope / future

Internal-defect sensing, dimensional metrology, second verticals, marketplace features, dedicated/custom device variants (only on future demand). Revisit only after G3.
