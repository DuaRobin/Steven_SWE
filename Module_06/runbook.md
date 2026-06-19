<div id="header" align="center" style="color: #23d4c5;">

| R U N B O O K |
---
</div>

* **Roll Back:** In case of production issue, we can divert all traffic to previous stable model.
    ```
    from google.cloud import aiplatform

    PROJECT = "project-1737319559746"
    LOCATION = "us-east1"
    YOURID = "rdua1"
    aiplatform.init(project=PROJECT, location=LOCATION)
    endpoint = aiplatform.Endpoint(endpoint_name="934085705330589696")

    for m in endpoint.list_models():
        if m.display_name == f"claims_v1_0_{YOURID}":
            v1_0_id: str = m.id
        elif m.display_name == f"claims_v1_1_{YOURID}":
            v1_1_id: str = m.id
    # roll back, send everything to v1.0
    endpoint.update(traffic_split={v1_1_id: 0, v1_0_id: 100})
    ```

* **Incident Note** An input skew on DrivAge indicates that the age distribution of drivers in our live serving traffic has significantly diverged from the fixed training_data.csv baseline. 
    * I recommend holding the model in production rather than initiating an immediate rollback. Although the input distribution has shifted, our Task 1 evaluation demonstrated that the model actually performs slightly better on the young-driver slice (AUC 0.674) compared to the overall population (AUC 0.650)
    * Since feature skew is an early warning rather than a proven accuracy drop, we can safely hold the rollout and monitor the prediction drift before deciding to intervene.


* **Production Readiness Checklist**

| Category | Item | Done? | Notes |
| :--- | :--- | :--- | :--- |
| Model | Registered with eval metadata, AUC + young slice | ☑ | Executed the registration scripts to upload the model artifact to Vertex AI Registry. Attached the overall AUC (0.650) and young-driver AUC (0.674) as metadata labels for lineage. |
| Model | Model card published, one page | ☑ | Documented the model's intended use for fast-track claims routing, its training baseline, and its limitations. This ensures stakeholders understand performance context before it routes real claims. |
| Model | Rollback version pinned | ☑ | Leveraged the Model Registry to separate the immutable model artifact from its movable aliases. The previous stable version (v1.0) is kept warm so we can instantly roll back by updating endpoint traffic split and reassigning the `production` alias. |
| Serving | Endpoint sized and autoscale tested | ☑ | Deployed the endpoint on `n1-standard-2` hardware with a `min_replica_count` of 1 to prevent cold starts. Configured a `max_replica_count` of 3 to automatically provision additional replicas during traffic spikes. |
| Serving | Online prediction verified | ☑ | Validated the `/predict` route using a smoke test with `test_payload.json`, which successfully returned fast-track probabilities. Also verified live prediction capability by sending continuous traffic during the 10-minute skew injection. |
| Serving | Traffic plan documented, canary to ramp to rollback | ☑ | Documented a canary rollout strategy routing 10% of traffic to the candidate model using `traffic_split`. Once stable, we ramp up to 100% or execute a rollback by shifting traffic back to the prior `deployed_model_id`. |
| Observability | Structured logs to Cloud Logging | ☑ | Prediction requests, backend errors, and system metrics are natively integrated with Google Cloud Logging. This ensures all endpoint invocations and background monitoring jobs produce an auditable, structured log trail. |
| Observability | Latency and error SLOs defined | ☑ | Established a 99.5% latency Service-Level Objective (SLO) for the claims-routing endpoint. This metric is strictly monitored during the canary phase to track the error budget before authorizing a full traffic ramp-up. |
| Observability | Skew monitoring active with a training baseline | ☑ | Enabled Model Monitoring v2 with a 1-hour interval, referencing the fixed `training_data.csv` baseline in Cloud Storage. Successfully verified the configuration by injecting a burst of skewed `DrivAge` data to trigger an alert. |
| Ops | Runbook linked from alerts, literal rollback command | ☑ | Added an incident note to `RUNBOOK.md` advising to "hold" rather than rollback on `DrivAge` skew since young-driver AUC remains strong. Included the literal `endpoint.update(traffic_split=...)` command to ensure atomic rollbacks during an incident. |
| Ops | On-call rotation set | ☑ | If a monitoring alert fires, a designated engineer will acknowledge it, ensuring production failures do not become orphan incidents. |
| Ops | Budget alert in place | ☑ | Configured per-project (per-environment) billing alerts at 50%, 75%, and 100% thresholds. This crucial software-engineering-controlled cost lever ensures that runaway autoscaling or long-running jobs are caught before producing a surprise bill. |