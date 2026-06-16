import pandas as pd, xgboost as xgb
from sklearn.metrics import roc_auc_score
from pathlib import Path

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
INPUT_DIR: Path = Path(MODULE_DIR, "pre_task", "starter_outputs")

hold_df = pd.read_csv(f"{INPUT_DIR}/holdout.csv")
y = hold_df.pop("fast_track")
booster = xgb.Booster()
booster.load_model(f"{INPUT_DIR}/model.bst")
preds = booster.predict(xgb.DMatrix(hold_df.values))  # plain array, matches training

# compute the top-line AUC from y and preds
auc_all = roc_auc_score(y_true=y, y_score=preds)

# mask the young-driver slice, DrivAge under 30, then score that slice
# DrivAge is preserved as a numeric column from the freMTPL2 dataset during the get_dummies encoding
mask = hold_df["DrivAge"] < 30
auc_young = roc_auc_score(y_true=y[mask], y_score=preds[mask])

print(f"AUC overall={auc_all:.3f}  AUC young={auc_young:.3f}")
