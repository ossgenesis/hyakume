# Frontend Spec Document — StoneScan

| | |
|---|---|
| **Status** | Draft v0.1 |
| **Surfaces** | (A) On-device operator UI, (B) Web dashboard |
| **Related docs** | PRD, Technical Architecture, Security & Access, Feature Tickets |

---

## 1. Design principles

- **Glanceable & one-handed** — the operator works in a noisy, dusty, bright bay; the core result (pass/fail) must read at arm's length in ≤ 1 second.
- **Minimal taps** — a scan completes in ≤ 2 taps (NFR-10).
- **Offline-honest** — the UI always shows sync state; nothing implies data is lost when offline.
- **High contrast & large targets** — usable with gloves, in sunlight, by non-technical users.
- **Trust-forward** — results show confidence and a clear, explainable defect overlay, not a black box.
- **Localized** — operator UI in English + pilot-market language at R1 (NFR-11).

---

## 2. Surface A — On-device operator UI

Runs on the handheld touchscreen. Target framework: a lightweight kiosk UI (e.g. Flutter or a web/Qt shell) on the edge device; full offline operation.

### 2.1 Screens

**A1. Sign-in / device ready**
- Operator sign-in (or device-bound session); shows device + org, current model bundle version, sync state, battery.
- States: signed-out, ready, update-available.

**A2. New session / slab setup**
- Select stone type (or auto-detect), optional slab/lot label, grading profile (defaults to org/customer profile).
- Primary action: **Start scanning**.

**A3. Live capture (viewfinder)**
- Camera viewfinder with framing guide; large **trigger** button.
- Coverage indicator (which parts of the slab are scanned) (FR-C4).
- Inline quality warnings: "too dark / move closer / hold steady" with retake (FR-C5).
- States: live, capturing (photometric sequence in progress), quality-warning.

**A4. Patch result**
- Pass/fail badge (color + icon + text, never color alone — accessibility).
- **Defect heatmap** overlay on the captured patch; toggle overlay on/off.
- Defect list: type, confidence, location; tap a defect to highlight on the image.
- Actions: **Accept**, **Retake**, **Flag as wrong** (operator correction → active-learning label, FR-S8).

**A5. Slab summary**
- Aggregated grade for the slab, count by defect type, coverage.
- Actions: **Finish slab**, **Add report note**, **Generate report**.
- Save writes the local record (FR-R2).

**A6. Sync & queue**
- Pending uploads, last sync time, retry; clear messaging when offline.

**A7. Settings**
- Active grading profile (read/select), calibration/light-check routine, language, device info, update now.

### 2.2 Component states (all screens)
Every data view defines: **loading**, **empty**, **error**, **offline**. Capture and result views additionally define **low-confidence** (prompt to rescan or flag).

### 2.3 Key on-device flow
`A1 → A2 → A3 (capture patches) → A4 (per patch) → A5 (finish) → record saved → A6 syncs`

---

## 3. Surface B — Web dashboard

React SPA. Authenticated per Security doc; views are RBAC-gated.

### 3.1 Screens

**B1. Sign-in** — email/SSO; MFA for Owner/Admin.

**B2. Overview** — KPIs: scans this period, pass rate, defect-type breakdown, reject/dispute trend, devices online. Operator sees site-scoped data; Admin/Owner see org-wide.

**B3. Slabs & scans (browse/search)** — filter by date, stone type, grade, device, operator, lot; list with thumbnails + grade. (FR-S2)

**B4. Scan/slab detail** — images + heatmap viewer, defect list with confidence, grade, model/profile version, timestamp, device/operator. Actions: **Export report (PDF)**, **Share with buyer** (R2), view **integrity hash** status.

**B5. Reports / dispute records** — list of generated reports; verify integrity; manage shares.

**B6. Grading profiles** — create/edit per stone type and per customer: thresholds, which defect types fail, grade tiers; versioned. (FR-S5)

**B7. Devices** — enroll, view status/bundle version, revoke; staged update rollout view. (FR-S4)

**B8. Users & roles** — invite, assign roles, MFA status, remove. (FR-S3)

**B9. Org settings** — org profile, **data-opt-in toggle** (FR-S7), retention policy, billing (Owner).

**B10. Model & updates (admin/internal)** — current bundle, available versions, rollout status. (FR-S6)

### 3.2 Component states
List/detail/admin views each define loading, empty, error, and permission-denied states. Destructive actions (revoke device, delete record, remove user) require confirmation.

### 3.3 Key dashboard flows
- **Review & export:** B3 → B4 → Export report → share.
- **Configure grading:** B6 → create profile → assign to customer/device.
- **Onboard a site:** B8 invite users → B7 enroll devices → B6 assign profiles.

---

## 4. Cross-cutting

### 4.1 Accessibility
- Never rely on color alone; pair with icon + text.
- Minimum tap target ~48px; on-device font sizes large by default.
- Screen-reader labels on dashboard; keyboard navigation.

### 4.2 Localization
- All strings externalized; English + one pilot-market language at R1; right-to-left readiness considered for later markets.

### 4.3 Responsive (dashboard)
- Works on desktop and tablet; field managers may review on tablet.

### 4.4 Visual system
- Clean, flat, high-contrast; consistent design tokens across both surfaces; pass = clear positive treatment, fail = clear negative treatment, both with text labels. Defect overlay uses a consistent color-by-type legend.

### 4.5 Performance
- On-device UI must remain responsive during the inference (< 300 ms target, NFR-2) with a clear in-progress state.
- Dashboard lists paginate / virtualize for large histories (NFR-8).

---

## 5. Open questions
- Capture model: discrete patches vs. continuous sweep-and-stitch (affects A3/A4 design) — resolve in R1 field testing.
- Is the on-device UI web-based (shared components with dashboard) or native — decide based on edge framework choice.
- Buyer-facing report view: hosted page vs. signed PDF only (R2).
