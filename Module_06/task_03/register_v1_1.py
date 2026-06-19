from google.cloud import aiplatform
from datetime import datetime

PROJECT = "project-1737319559746"
LOCATION = "us-east1"
YOURID = "rdua1"
build_id = datetime.now().strftime("%Y%m%d-%H%M")

aiplatform.init(project=PROJECT, location=LOCATION)

model_v1_1 = aiplatform.Model.upload(
    parent_model=(  # adds a version to the existing parent
        f"projects/{PROJECT}/locations/{LOCATION}/models/claims_triage_{YOURID}"
    ),
    display_name=f"claims_triage_{YOURID}",
    artifact_uri=f"gs://{YOURID}-stevens-swe-20049317/model_v1_1/",
    serving_container_image_uri=(
        "us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-7:latest"
    ),
    labels={"build_id": build_id, "run_id": "task3"},
)
print("Registered:", model_v1_1.resource_name)
print("Version:", model_v1_1.version_id)
