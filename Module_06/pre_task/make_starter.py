import json, subprocess, pandas as pd, xgboost as xgb
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from pathlib import Path

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
OUTPUT_DIR: Path = Path(MODULE_DIR, "pre_task", "starter_outputs")
YOURID = "rdua1"
BUCKET = f"gs://{YOURID}-stevens-swe-20049317"  # I already had a bucket, didn't create new one.

df = fetch_openml(data_id=41214, as_frame=True).frame  # freMTPL2, public
df["fast_track"] = (df["ClaimNb"].astype(float) == 0).astype(int)
RAW = [
    "Area",
    "VehPower",
    "VehAge",
    "DrivAge",
    "BonusMalus",
    "VehBrand",
    "VehGas",
    "Density",
    "Region",
]
X = pd.get_dummies(df[RAW], columns=["Area", "VehBrand", "VehGas", "Region"], dtype=int)
y = df["fast_track"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)


def train(spw):  # spw recalibrates the threshold
    p = {
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "max_depth": 4,
        "eta": 0.2,
        "scale_pos_weight": spw,
    }
    return xgb.train(p, xgb.DMatrix(Xtr.values, label=ytr.values), num_boost_round=60)


train(1.0).save_model(f"{OUTPUT_DIR}/model.bst")  # v1.0 baseline
train(1.3).save_model(f"{OUTPUT_DIR}/model_v1_1.bst")  # v1.1 recalibrated

Xtr.to_csv(f"{OUTPUT_DIR}/training_data.csv", index=False)
Xte.assign(fast_track=yte).to_csv(f"{OUTPUT_DIR}/holdout.csv", index=False)
json.dump(
    Xte.head(20).values.tolist(),
    open(f"{OUTPUT_DIR}/test_payload.json", "w"),
)

subprocess.run(
    ["gcloud", "storage", "buckets", "create", BUCKET, "--location=us-east1"]
)
for src, dst in [
    (f"{OUTPUT_DIR}/model.bst", "model/model.bst"),
    (f"{OUTPUT_DIR}/model_v1_1.bst", "model_v1_1/model.bst"),
    (f"{OUTPUT_DIR}/training_data.csv", "training_data.csv"),
    (f"{OUTPUT_DIR}/holdout.csv", "holdout.csv"),
    (f"{OUTPUT_DIR}/test_payload.json", "test_payload.json"),
]:
    subprocess.run(["gcloud", "storage", "cp", src, f"{BUCKET}/{dst}"], check=True)
print("Starter ready and uploaded to", BUCKET)
