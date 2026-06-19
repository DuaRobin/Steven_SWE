<div id="header" align="center" style="color: #23d4c5;">

| R E F L E C T I O N |
---
</div>

* At Hartford scale, 
    1. the first production change I would implement is replacing manual, notebook-driven model training with scheduled Vertex AI Pipelines. A notebook prototype lacks a service-level agreement, cannot be easily reproduced, and leaves no auditable trace of which dataset version produced a specific model
        1. To fix this, I would refactor our XGBoost script into containerized components using the @dsl.component decorator and orchestrate them via a @dsl.pipeline function.
        2. I would then schedule a weekly retraining job using job.create_schedule(cron="0 6 * * 1", ...) while pinning the input dataset URI to an exact snapshot date rather than pointing it at a "latest" file.

        This code pattern ensures every run is automatically linked by the Vertex Metadata Service, allowing engineers and auditors to trace any deployed model version back to its exact pipeline run ID and data

    2. Second, I would replace our basic Endpoint deployments with an automated Canary rollout strategy. Pushing a model to 100% of traffic immediately exposes the business to unacceptable risk if there are tokenizer regressions or cold-start issues. 
        1. Instead, using the Vertex AI SDK, I would deploy the candidate model alongside the current version by calling endpoint.deploy() with a 10% canary split, utilizing the configuration traffic_split={current_id: 90, "0": 10}
        2. We would then monitor the new DeployedModel for latency SLOs and prediction drift. Once stability is proven under live traffic, we would execute the atomic endpoint.update(traffic_split={candidate_id: 100, current_id: 0}) to ramp up to full capacity

* If forced to roll back to a pre-2026 toolchain featuring Container Registry and the old vertexai SDK, several components of our architecture would instantly break. Primarily, any code using the unified google-genai SDK for inference would fail, as the legacy vertexai.generative_models library reached its end-of-life on June 24, 2026
    1. To fix this, I would have to rewrite our generation requests to use the deprecated vertexai.init() and GenerativeModel() initialization patterns
    2. Additionally, our deployment pipelines would fail to pull serving images; I would need to update all Cloud Build definitions and serving_container_image_uri paths from the modern Artifact Registry format (us-docker.pkg.dev) back to the legacy Container Registry gcr.io structure

* Throughout these lessons/assignment, 
    1. I could not find a way to confirm what higher versions of xgboost container was available instead of pinning it to xgboost-cpu.1-7. Python Library had its latest version at 3.2.0 but was pinned at 1.7.6.
    2. I also struggled with Model Monitoring Job Alert. Leaving default monitoring frequency at 24 hours or changing it to 1 hour in the hope of alert triggering faster, both did not work, even though job configuration had training_data.csv as the baseline and skewed data injection for generating drift. None of students were able to generate an alert from Model Monitoring Job. 