import pandas as pd, xgboost as xgb
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from pathlib import Path

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
OUTPUT_DIR: Path = Path(MODULE_DIR, "task_01", "starter_outputs")

df = fetch_openml(data_id=41214, as_frame=True).frame  # freMTPL2, public, no login
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

p = {"objective": "binary:logistic", "eval_metric": "auc", "max_depth": 4, "eta": 0.2}
booster = xgb.train(p, xgb.DMatrix(Xtr.values, label=ytr.values), num_boost_round=60)
booster.save_model(f"{OUTPUT_DIR}/model.bst")  # the model you evaluate
Xte.assign(fast_track=yte).to_csv(
    f"{OUTPUT_DIR}/holdout.csv", index=False
)  # the eval slice
print(f"Wrote {OUTPUT_DIR}/model.bst and {OUTPUT_DIR}/holdout.csv")
