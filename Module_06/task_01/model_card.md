# Model Card: claims_triage (fast_track)

**🚨 ON-CALL EMERGENCY SUMMARY: If this model is degrading, emitting errors, or causing an incident, DO NOT attempt to debug the XGBoost artifacts. Immediately roll back traffic to the previous version by moving the `production` alias in the Vertex AI Model Registry.**

### 1. What This Model Predicts
This is an XGBoost binary classification model used for motor insurance claim routing. It predicts the `fast_track` label, which identifies if an incoming claim is expected to result in a zero-dollar payout (`ClaimNb == 0`). 

### 2. Performance Metrics
Based on our baseline holdout evaluation:
*   **Overall AUC:** 0.650
*   **Young Driver Slice AUC (DrivAge < 30):** 0.674

### 3. Intended Use
This model is used to automatically triage and route low-risk/zero-dollar claims away from manual adjusters. Claims that score highly for `fast_track` bypass the standard human-in-the-loop queue.

### 4. Known Weaknesses (Young-Driver Slice)
The model exhibits a known performance skew on the young-driver demographic (drivers under 30 years old). Because the AUC for young drivers (0.674) diverges from the overall population (0.650), the model is highly sensitive to distribution shifts in this demographic. **On-call action:** If Model Monitoring v2 triggers a prediction drift alert, immediately check the `DrivAge` feature distributions, as young-driver misclassifications are the most likely culprit.

### 5. Rollback Version & Procedure
*   **Rollback Target:** Revert to the baseline version (v1.0 `model.bst`).
*   **Rollback Procedure:** Do not rebuild the container or redeploy the endpoint. Rollback is an atomic server-side alias move. Run the following to strip the `production` alias from the broken version and reassign it to the previous stable version:
    ```python
    from google.cloud import aiplatform
    # Retrieve the previous stable version (e.g., v1.0) and move the alias
    model = aiplatform.Model("projects/.../models/claims_triage@<PREVIOUS_VERSION_ID>")
    model.versioning_registry.add_version_aliases(new_aliases=["production"], version=model.version_id)
    ```

**Note:** Under Task-1, Being the candidate, currently no traffic is routed to it, and being the version 1, there is no previous version to roll back to.