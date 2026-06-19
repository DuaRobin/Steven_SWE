from google.cloud import aiplatform

PROJECT = "project-1737319559746"
LOCATION = "us-east1"
YOURID = "rdua1"
aiplatform.init(project=PROJECT, location=LOCATION)
endpoint = aiplatform.Endpoint(endpoint_name="934085705330589696")
current_id = endpoint.list_models()[0].id  # the existing v1.0 DeployedModel
model_v1_1 = aiplatform.Model(
    f"projects/{PROJECT}/locations/{LOCATION}/models/claims_triage_{YOURID}"
)

endpoint.deploy(  # "0" here means the model deployed now
    model=model_v1_1,
    deployed_model_display_name=f"claims_v1_1_{YOURID}",
    machine_type="n1-standard-2",
    min_replica_count=1,
    max_replica_count=3,
    # 10 percent to the new model (Deployed Above), 90 to current. the note above explains the "0" key
    traffic_split={current_id: 90, "0": 10},
)