# Security & Access Document — StoneScan

| | |
|---|---|
| **Status** | Draft v0.1 |
| **Scope** | Identity & access, device security, data protection, record integrity, compliance |
| **Related docs** | PRD, Technical Architecture, Frontend Spec, Feature Tickets |

---

## 1. Principles

- **Least privilege** — users and devices get only what their role requires.
- **Tenant isolation** — one organization can never see another's data.
- **Protect the moat** — the proprietary models and dataset are the company's core asset; treat model artifacts and training data as crown-jewel assets.
- **Trustworthy records** — scan records are evidence in buyer/seller disputes, so **integrity and authenticity** are first-class requirements.
- **Privacy by default** — capture and retain the minimum; field-data reuse is **opt-in**.

## 2. Identity & access management

### 2.1 Roles
| Role | Description |
|---|---|
| **Org Owner** | Full control of an organization: billing, users, devices, profiles, data-opt-in |
| **Admin** | Manage users, devices, grading profiles, view all scans |
| **QC Operator** | Operate a device, run scans, view own/site scans; no admin settings |
| **Auditor / Viewer** | Read-only access to scans and reports |
| **External Buyer** | Scoped read-only access to specifically shared reports only (R2) |
| **Device** (machine identity) | Authenticated as itself; pairs with the mobile app and submits captures (firmware updates only — no model bundles) |

### 2.2 RBAC matrix
| Capability | Owner | Admin | Operator | Auditor | Buyer |
|---|:--:|:--:|:--:|:--:|:--:|
| Run a scan (device) | ✓ | ✓ | ✓ | — | — |
| View org scans/reports | ✓ | ✓ | site only | ✓ | shared only |
| Export report | ✓ | ✓ | ✓ | ✓ | shared only |
| Configure grading profile | ✓ | ✓ | — | — | — |
| Manage users/roles | ✓ | ✓ | — | — | — |
| Enroll/revoke devices | ✓ | ✓ | — | — | — |
| Toggle data-opt-in | ✓ | — | — | — | — |
| Billing | ✓ | — | — | — | — |

### 2.3 Authentication
- **Users:** email/password or SSO; **MFA required** for Owner/Admin.
- **Devices:** enrolled with a unique credential at provisioning; pair with the mobile app, which relays captures to the API under the operator's session + the device identity; revocable.
- **API:** short-lived bearer tokens for sessions; scoped, rotatable keys for device/service auth.
- **External buyers:** access via signed, expiring, scoped share links (R2).

## 3. Device security

- **Provisioning/enrollment:** each device receives a unique identity and is bound to one organization; lost/compromised devices can be revoked centrally.
- **Transient buffering:** the device is capture-only and holds captures transiently (encrypted) until streamed to the paired app; no long-term record storage on the device.
- **Firmware update path:** device firmware updates are **cryptographically signed**; the device verifies the signature before applying and supports rollback. There are no model bundles on the device — inference models live in the cloud.
- **Mobile-app safety:** captures queued in the app remain encrypted until uploaded and confirmed; no silent data loss on a connectivity drop.
- **Tamper considerations:** restrict debug interfaces in production builds; verify app/runtime integrity at start.

## 4. Data protection

### 4.1 In transit & at rest
- All device↔cloud and dashboard↔cloud traffic over **TLS**.
- Cloud object storage and database **encrypted at rest**.
- No sensitive data in URLs/query strings.

### 4.2 Data classification
| Class | Examples | Handling |
|---|---|---|
| Crown-jewel | Trained models, labeled RGB-D training dataset | Strictest access; cloud-only (served in-cluster); not exportable by customers |
| Sensitive | Scan records, reports, dispute evidence, org/customer info | Tenant-isolated, encrypted, access-logged |
| Operational | Device telemetry, logs | Minimized, consented, retention-limited |
| Low-PII | Stone images themselves | Generally non-personal; treat metadata (operator, site) as sensitive |

Note: stone imagery is largely non-personal, but **operator identity, site, customer, and commercial grade data are sensitive** and may constitute personal/commercial data.

### 4.3 Retention & deletion
- Records retained per org policy; dispute-evidence records may need longer retention by agreement.
- Support per-org and per-record deletion requests; deletion is honored across primary stores and backups within a defined window.
- Field data reused for training only with **explicit org opt-in (FR-S7)**; opt-out stops future ingestion.

## 5. Record integrity (dispute evidence)

- Each per-slab record carries an **integrity hash** over its images, defects, grade, model/profile version, and timestamp (FR-R4).
- Records are **append-only / tamper-evident**: edits create new versions rather than overwriting; the audit trail is preserved.
- Exported reports embed the hash and metadata so a buyer can verify authenticity of a shared report.

## 6. Tenancy & isolation

- Every data access is scoped by `org_id`; no cross-tenant queries.
- Object-storage paths and DB rows are partitioned/filtered by tenant.
- Base inference models are shared across tenants (served in-cluster) but **per-org grading profiles and data are isolated**.

## 7. Audit logging

- Log security-relevant events: logins, role/permission changes, device enroll/revoke, profile changes, report exports/shares, data-opt-in toggles, deletions.
- Audit logs are tamper-evident and access-restricted to Owner/Admin (and internal security).

## 8. Network & infrastructure

- Principle-of-least-exposure: only the API gateway is public; internal services are private.
- Secrets in a managed secret store; no secrets in code or images.
- Regular dependency and image scanning; least-privilege service accounts.

## 9. Compliance considerations

- Likely in scope depending on markets: **India DPDP Act** (home market) and **GDPR** (EU buyers) for any personal data (operators, customer contacts).
- Maintain a data-processing inventory and a basic DPA template for customers.
- Export/trade data handled per applicable regulations; avoid storing customer financial credentials (out of product scope).

## 10. Incident response (baseline)

- Defined severity levels and an on-call owner.
- Containment via device/token/key revocation and tenant-scoped isolation.
- Customer notification process for breaches affecting their data, per legal obligations.
- Post-incident review with corrective actions.

## 11. Prohibited / out of scope

- StoneScan does **not** collect or store end-customer payment credentials, government IDs, or financial account data.
- No third-party ad tracking; field data is used only for the product and (with opt-in) model training.
