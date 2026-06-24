from pathlib import Path
from sklearn.metrics import roc_auc_score
import pandas as pd, numpy as np, xgboost as xgb
import shap

MODULE_DIR: Path = Path(__file__).resolve().parents[1]
INPUT_DIR: Path = Path(MODULE_DIR, "task_01", "starter_outputs")
EVIDENCE_DIR: Path = Path(MODULE_DIR, "evidence")

hold = pd.read_csv(f"{INPUT_DIR}/holdout.csv")
y = hold.pop("fast_track")  # true label
booster = xgb.Booster()
booster.load_model(f"{INPUT_DIR}/model.bst")
score = booster.predict(xgb.DMatrix(hold.values))  # fast-track probability
pred = (score >= 0.5).astype(int)  # the triage decision

band = pd.cut(
    hold["DrivAge"],
    bins=[17, 25, 35, 50, 120],
    labels=["18-25", "26-35", "36-50", "51+"],
)  # proxy slice

def metrics(m):
    yt, yp, sc = y[m], pred[m], score[m]
    approval = yp.mean()  # share routed to fast-track
    # false-positive rate: predicted fast-track among the truly NOT fast-track
    fpr = yp[yt == 0].mean() if (yt == 0).sum() > 0 else float("nan")
    auc = roc_auc_score(yt, sc) if yt.nunique() > 1 else float("nan")
    return {"approval_rate": approval, "fpr": fpr, "auc": auc}

report = pd.DataFrame({b: metrics(band == b) for b in band.cat.categories}).T
# the gate: the max inter-slice gap in FPR across the bands
fpr_gap = report["fpr"].max() - report["fpr"].min()
# print(report.round(3))
print(report)
# print(f"FPR gap = {fpr_gap:.3f}  ->  gate {'PASS' if fpr_gap <= 0.10 else 'FAIL'}")
print(f"FPR gap = {fpr_gap}  ->  gate {'PASS' if fpr_gap <= 0.10 else 'FAIL'}")
report.to_csv(f"{EVIDENCE_DIR}/Task1_Slice_Metrics.csv")

# Find the top five drivers with SHAP
sample = hold.sample(200, random_state=42)
sv = shap.TreeExplainer(booster).shap_values(sample.values)
top5 = (
    pd.Series(np.abs(sv).mean(axis=0), index=hold.columns)
    .sort_values(ascending=False)
    .head(5)
)
print("Top 5 drivers:\n", top5.round(4))
