# Product Requirements Document — StoneScan

| | |
|---|---|
| **Product** | StoneScan (working codename) — handheld surface-defect scanner for natural stone |
| **Status** | Draft v0.1 |
| **Owner** | Founder / Product |
| **Related docs** | Technical Architecture, Security & Access, Frontend Spec, Feature Tickets |

---

## 1. Overview & problem

Small and mid-size stone factories, processors and traders inspect slab surfaces **manually** before shipment. This is subjective, inconsistent, slow, and produces no objective record — leading to rejected shipments, buyer disputes, and repeated per-consignment third-party inspection costs. Existing automated inspection is large, fixed, inline machine vision built for big production lines and cannot serve a trader's warehouse or a buyer's receiving dock.

StoneScan is a **handheld, surface-only** device that turns slab inspection into a fast, repeatable, documented measurement: an operator sweeps it across a slab and gets a pass/fail grade, a defect heatmap, and a timestamped per-slab record that both buyer and seller can trust.

## 2. Strategic context

StoneScan is the **wedge** for a broader "vertical AI for visual inspection" company. The moat is not the hardware — it is the proprietary stone-defect **dataset** and an accepted **grading standard**. Every product decision should favour accumulating clean labeled data and producing a defensible, shareable grade. The capture/ML/deploy stack is designed as a reusable **engine** for later surface-QC verticals (tiles, glass, wood, metal, precast concrete).

## 3. Goals & non-goals

**Goals**
- Detect surface grains, cracks, fissures, pits, stains and impurities on granite, marble, slate and quartzite.
- Match or beat an expert inspector's accuracy on agreed defect classes.
- Sub-minute inspection workflow per slab; works offline in real yard/warehouse lighting.
- Produce a tamper-evident per-slab record and exportable report.
- Continuously grow a proprietary labeled dataset from consented field use.

**Non-goals (this product cycle)**
- Internal/subsurface defects (no ultrasonic, X-ray, or LiDAR).
- Dimensional metrology / flatness as a primary feature.
- Any second vertical before the go/no-go gate (G3).
- A fully autonomous fixed/inline line system.

## 4. Personas

| Persona | Context | Primary need |
|---|---|---|
| **QC Operator** (Maya) | Works the grading/loading bay; dusty, bright/variable light; limited tech comfort | Scan fast, one hand, clear pass/fail |
| **Factory/Trader Owner** (Rahul) | Runs an export-oriented SME; feels reject/dispute costs | Reduce rejects, prove quality, manage devices/users |
| **Buyer / Importer** (external) | Receives slabs abroad; wants independent verification | Trusted, tamper-evident scan report per slab |
| **Inspection-firm Operator** (partner) | Scans on behalf of clients (inspection-as-a-service) | Reliable device + certified reports across many sites |

## 5. Use cases / user stories

- As a **QC Operator**, I sweep the device over a slab and immediately see pass/fail with a defect heatmap, so I can sort slabs without expert judgment.
- As a **QC Operator**, I work in a warehouse with no internet and trust that all scans sync later.
- As an **Owner**, I configure what counts as a reject for a given customer (grading profile), so grading matches each buyer's tolerance.
- As an **Owner**, I export a per-slab report to send with a shipment as quality evidence.
- As a **Buyer**, I open a shared scan report and verify it is authentic and unaltered.
- As an **Inspection-firm Operator**, I manage many devices and produce consistent certified reports across sites.
- As the **company**, consented scans flow back as labeled training data to improve models.

## 6. Functional requirements

Priority: **P0** = required for the release it's tagged to; **P1** = important; **P2** = later. Release: R0 bench POC, R1 pilot, R2 scale.

### 6.1 Capture
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-C1 | Capture multi-angle images of a slab patch via photometric-stereo LED sequence, synchronized with the camera | P0 | R0 |
| FR-C2 | Live viewfinder with one-tap trigger; capture in < 2 s per patch | P0 | R1 |
| FR-C3 | Shrouded/contact capture that suppresses ambient light variability | P0 | R1 |
| FR-C4 | Guide the operator to cover a full slab (patch sequence or sweep) and track coverage | P1 | R1 |
| FR-C5 | Reject blurred/under-exposed captures with retake prompt | P1 | R1 |

### 6.2 Detection & grading
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-D1 | Anomaly detection flags surface regions deviating from "good" stone | P0 | R0 |
| FR-D2 | Segment and classify named defects: crack, fissure, pit, stain, chip, color/impurity | P0 | R1 |
| FR-D3 | Disambiguate harmless mineral-filled fissures from structural cracks using surface-normal cues | P0 | R1 |
| FR-D4 | Output a per-slab grade (pass/fail + grade tier) from a configurable grading profile | P0 | R1 |
| FR-D5 | Per-defect confidence and location returned with each result | P1 | R1 |
| FR-D6 | Stone-type selection or auto-detection to load the right model/profile | P1 | R1 |

### 6.3 Results, records & reporting
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-R1 | Show pass/fail, defect heatmap overlay, and defect list on-device | P0 | R0 |
| FR-R2 | Create a per-slab record: images, heatmap, defects, grade, timestamp, device, operator, profile version, model version | P0 | R1 |
| FR-R3 | Generate an exportable report (PDF) suitable to accompany a shipment | P1 | R1 |
| FR-R4 | Records are tamper-evident (integrity hash; see Security doc) | P1 | R1 |
| FR-R5 | Share a read-only report link/file with an external buyer | P2 | R2 |

### 6.4 Sync, management & learning
| ID | Requirement | Pri | Rel |
|---|---|---|---|
| FR-S1 | Offline-first local storage; automatic sync to cloud when connected | P0 | R1 |
| FR-S2 | Web dashboard: search/browse slabs and scans, view details, export | P0 | R1 |
| FR-S3 | Org/user management with roles (see Security doc RBAC) | P0 | R1 |
| FR-S4 | Device enrollment and management | P1 | R1 |
| FR-S5 | Configure grading profiles per org/customer | P0 | R1 |
| FR-S6 | Over-the-air signed model/profile updates to devices | P1 | R2 |
| FR-S7 | Consented capture of field data into the training pipeline; per-org opt-in | P0 | R1 |
| FR-S8 | Operator correction/feedback on a result (active-learning label) | P1 | R2 |

## 7. Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-1 Accuracy | Detection quality on agreed classes | ≥ expert inspector; track precision/recall, image & pixel AUROC |
| NFR-2 Latency | On-device inference per patch | < 300 ms |
| NFR-3 Throughput | End-to-end workflow per slab | < 60 s |
| NFR-4 Offline | Full capture→result→record without connectivity | 100% of core flow |
| NFR-5 Battery | Continuous inspection session | ≥ 4 hours |
| NFR-6 Robustness | Operation in variable ambient light, dusty environment | Stable accuracy with shroud |
| NFR-7 Reliability | Cloud availability | 99.5% (R2) |
| NFR-8 Scalability | Slabs/scans stored & queryable | Millions of records |
| NFR-9 Security/Privacy | Per Security & Access Document | — |
| NFR-10 Usability | Taps to complete a scan | ≤ 2 |
| NFR-11 Localization | Operator UI languages | English + 1 pilot-market language at R1 |

## 8. Success metrics (tied to project gates)

- **G1:** blind-test detection ≥ expert on agreed classes in controlled lighting.
- **G2:** median per-slab workflow < 60 s; stable accuracy in real ambient light.
- **G3:** field accuracy ≥ expert; ≥ 3 paying/renewing pilots; early buyer-side demand for the report.
- Ongoing: labeled images accumulated per week; dispute/reject rate reduction vs. customer baseline.

## 9. Release scope

- **R0 (Bench POC):** FR-C1, FR-D1, FR-R1 on a tethered bench rig. Prove detection.
- **R1 (Pilot):** handheld device, full capture/detect/grade/record/report/sync/management, grading profiles, consented data capture.
- **R2 (Scale):** OTA updates, buyer-shared reports, active-learning feedback loop, hardening and SLAs.

## 10. Dependencies & assumptions

- Access to physical stone samples (good + defective) across 3–4 types.
- Domain expert to define defect taxonomy and validate grading.
- Edge compute (Jetson Orin Nano class) or capable phone available.
- Anomaly-detection-first approach reduces labeled-defect data needs early.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Fissure vs. structural crack confusion | Photometric stereo + tunable per-profile thresholds + expert-in-loop |
| Field lighting variability | Shroud/contact discipline; validate at G2 |
| Insufficient labeled data | Anomaly-first; harvest via consented capture and inspection-as-a-service |
| Generalization across stone types | Start with 3–4 types; expand post-gate |
| Scope creep into internal/3D | Enforce non-goals |

## 12. Out of scope / future

Internal-defect sensing, dimensional metrology, second verticals, marketplace features, mobile consumer app. Revisit only after G3.
