import random, time, pandas as pd
from google.cloud import aiplatform
from pathlib import Path

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
INPUT_DIR: Path = Path(MODULE_DIR, "pre_task", "starter_outputs")
PROJECT, LOCATION = "project-1737319559746", "us-east1"

aiplatform.init(project=PROJECT, location=LOCATION)
endpoint = aiplatform.Endpoint(endpoint_name="934085705330589696")
# same columns the model expects
base = pd.read_csv(f"{INPUT_DIR}/holdout.csv")  # 1100 Records
base.drop(columns=["fast_track"], inplace=True, errors="ignore")
# --- CONFIGURATION TOGGLE ---
SEND_SKEWED = True  # Set to False for normal traffic, True for the skew test
# ----------------------------
if SEND_SKEWED:
    print("🚀 Starting SKEWED data injection...")
    drivage_col = base.columns.get_loc("DrivAge")  # its position in the array
else:
    print("✅ Starting VALID (normal) data injection...")

end = time.time() + 600  # 10 minutes
while time.time() < end:
    row = base.sample(1).copy()
    if SEND_SKEWED:
        # Force young drivers to trigger the Vertex AI drift/skew alert
        row.iloc[0, drivage_col] = random.randint(1, 16)  # force young drivers → skew
    endpoint.predict(instances=row.values.tolist())
    time.sleep(1)
# for i in range(len(base)):
#     row = base.iloc[[i]].copy()
#     if SEND_SKEWED:
#         # Force young drivers to trigger the Vertex AI drift/skew alert
#         row.iloc[0, drivage_col] = random.randint(1, 16)  # force young drivers → skew
#     endpoint.predict(instances=row.values.tolist())
print("🏁 Data injection complete.")
