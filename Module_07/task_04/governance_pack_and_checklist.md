# Governance Pack & Attestation

## Step 1: EU AI Act High-Risk Mapping

**System Classification:** 
Automated claims triage sits in **Annex III as a high-risk system** because it determines access to essential private services (insurance) and directly affects individuals' financial outcomes and benefits. Under the EU AI Act, transparency, risk management, and explainability for such systems are enforceable obligations, not aspirational standards.

**Enforcement Deadline & Penalties:**
*   **Enforcement Deadline:** 2 August 2026
*   **Maximum Penalty:** €15M or 3% of global turnover for high-risk non-compliance. *(Note: The system falls into this tier as it is a non-compliant high-risk system, not a prohibited practice under Article 5, which would carry the €35M / 7% ceiling).*

**Obligations & Artifact Mapping:**
To satisfy the EU AI Act's high-risk obligations, the following controls have been mapped directly to our technical artifacts:
*   **Risk Management:** Satisfied by the **Task 2 Screening Gateway Threat Model**. It details how the screening layer places input and output shields to prevent prompt injection and PII leakage.
*   **Data Governance:** Satisfied by the **Task 1 Slice-Fairness Report**. Bias often enters the ML lifecycle through skewed sampling and historical inequity baked into the labels. The fairness report evaluates data and model bias across protected demographic slices before the model is built and gated.
*   **Technical Documentation:** Satisfied by the **Task 1 Model Card**. The Model Card travels with the registered model version to explicitly document intended use, known limits, and performance by protected slice.
*   **Human Oversight:** Satisfied by the **Task 1 Feature Attributions (SHAP)**. Denials need a documented, explainable reason. By emitting top contributing features alongside the triage decision, human adjusters can explain and verify the specific factors driving the model's output.
*   **Logging:** Satisfied by the **Task 3 Tamper-Evident Audit Record**. A regulator's inquiry into a specific decision requires joining audit logs and lineage. The chained, append-only JSONL log securely records the hashed input and the specific model version for every triage decision.

---

## Step 2: NAIC Governance Attestation

**Accountable Owner:** Lead Machine Learning Engineer / Chief Risk Officer

Aligned with the NAIC Model Bulletin on the Use of Algorithms, Predictive Models, and Artificial Intelligence Systems by Insurers, we attest to the following governance, testing, and operational posture:

*   **Testing & Validation Evidence:** 
    Algorithmic bias was proactively measured using the **Task 1 Slice-Fairness Report**. Recognizing that optimizing for aggregate accuracy can hide disparate impact on minority slices, we evaluated the False Positive Rate (FPR) gap across specific demographic bands. The release gate enforced an FPR gap of ≤ 0.10 across all slices prior to model promotion.
*   **Screening-Control Plan:** 
    Our runtime protection relies on the **Task 2 Screening Gateway Threat Model**, which outlines our defense-in-depth approach to application and agent risks. The plan specifies a managed gateway running concurrent filters (including Sensitive Data Protection for PII and prompt-injection detection) across both inbound prompts and outbound responses.
    *(Deployment Status: Designed, not deployed this term).*
*   **Ongoing Accountability Reference:** 
    To guarantee traceability of algorithmic decisions and continuous assurance, the system utilizes the **Task 3 Tamper-Evident Audit Log**. Every inference request is recorded with a cryptographic hash of the input, chained to the previous decision. This ensures that no individual can quietly rewrite the historical ledger if a model decision is ever contested by an applicant or auditor.
---
## Step 3: Trust Readiness Checklist

| Trust Readiness Item | Status? | Evidence Pointer Notes |
|:---------------------|:--------|:-----------------------|
|Model card published with slice metrics + fairness statement|☑|Task 01: Completed and documented in the Claims Triage Model Card.|
|Fairness gate (FPR gap ≤ 0.10) evaluated and recorded|☑|Task 01: Evaluated via [`fairness.py`](../task_01/fairness.py) and codified in the release gate.|
|Screening gateway threat-modeled with three filter families|☑|Task 02: Threat Model written covering Injection, PII, and Responsible-AI.|
|Out-screen blocks a PII leak in the model's reply (harness)|☑|Task 02: Verified in [`gateway.py`](../task_02/gateway.py) where `screen_out` catches SSN leaks.|
|Screening gateway deployment status stated honestly|☑|Task 02: The threat model explicitly states the managed gateway is "Designed, not deployed" this term.|
|Audit record stores input as a hash, never raw content|☑|Task 03: Implemented in [`audit.py`](../task_03/audit.py) using `hashlib.sha256` on the input vector.|
|Audit log chained and proven tamper-evident|☑|Task 03: Implemented in [`audit.py`](../task_03/audit.py) by linking records via the `prev_hash` field.|
|EU AI Act high-risk technical documentation prepared|☑|Task 04: Completed one-page mapping matrix inside the Governance Pack.|
|NAIC AI governance attestation on file|☑|Task 04: Completed with a named accountable owner inside the Governance Pack.|
---