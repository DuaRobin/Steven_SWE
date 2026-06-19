from google.cloud import aiplatform
from pathlib import Path
import json

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
INPUT_DIR: Path = Path(MODULE_DIR, "pre_task", "starter_outputs")

PROJECT = "project-1737319559746"
LOCATION = "us-east1"
YOURID = "rdua1"
aiplatform.init(project=PROJECT, location=LOCATION)
endpoint = aiplatform.Endpoint(endpoint_name="934085705330589696")
with open(f"{INPUT_DIR}/test_payload.json") as f:
    instances = json.load(f)
resp = endpoint.predict(instances=instances)
print(resp.predictions[:3])  # a list of fast-track probabilities
