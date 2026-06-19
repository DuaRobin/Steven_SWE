from google.cloud import aiplatform

PROJECT = "project-1737319559746"
LOCATION = "us-east1"
YOURID = "rdua1"
aiplatform.init(project=PROJECT, location=LOCATION)
model = aiplatform.Model(
    f"projects/{PROJECT}/locations/{LOCATION}/models/claims_triage_{YOURID}"
)

endpoint = aiplatform.Endpoint.create(
    display_name=f"claims-prod-{YOURID}", location=LOCATION
)

endpoint.deploy(
    model=model,  # the version from Task 1
    deployed_model_display_name=f"claims_v1_0_{YOURID}",
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=3,
)
print("Endpoint:", endpoint.resource_name)
