from google.cloud import aiplatform
from datetime import datetime

PROJECT = "project-1737319559746"
LOCATION = "us-east1"
YOURID = "rdua1"
build_id = datetime.now().strftime("%Y%m%d-%H%M")

aiplatform.init(project=PROJECT, location=LOCATION)

model = aiplatform.Model.upload(
    model_id=f"claims_triage_{YOURID}",  # creates the parent + version 1
    display_name=f"claims_triage_{YOURID}",
    artifact_uri=f"gs://{YOURID}-stevens-swe-20049317/model/",
    serving_container_image_uri=(
        "us-docker.pkg.dev/vertex-ai/prediction/xgboost-cpu.1-7:latest"
    ),
    version_aliases=["candidate"],
    labels={
        "build_id": build_id,
        "run_id": "task1",
        "auc": "0_650",  # '.' not allowed in labels, real numbers from evaluate.py
        "auc_young": "0_674",  # '.' not allowed in labels, real numbers from evaluate.py
    },
)
print("Registered:", model.resource_name)
print("Version:", model.version_id)
