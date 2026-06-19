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

# Send 100+ predictions, confirm ~90/10 in Cloud Logging, then ramp to 100.

# ramp the canary to 100 percent and drain v1.0 to 0
endpoint.update(traffic_split={v1_1_id: 100, v1_0_id: 0})

model_v1_1 = aiplatform.Model(
    f"projects/{PROJECT}/locations/{LOCATION}/models/claims_triage_{YOURID}"
)
model_v1_1.versioning_registry.add_version_aliases(
    new_aliases=["production"], version=model_v1_1.version_id
)  # move the alias

# roll back, send everything to v1.0, in this one update call
endpoint.update(traffic_split={v1_1_id: 0, v1_0_id: 100})
