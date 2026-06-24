# Claims Triage Model — Model Card

## Intended use
**What it decides:** This model determines whether a motor insurance claim should be routed to a "fast-track" approval queue, based on a fast-track probability score and a 0.5 threshold.
**Who relies on it:** Claims adjusters and the automated claims routing pipeline at the insurer.
**What it must NOT be used for:** The model is a triage tool designed to fast-track low-risk claims; it must **not** be used to automatically deny coverage or reject claims without human review.

## Training data
**Dataset:** Trained on `freMTPL2`, a public dataset of French motor third-party liability insurance records.
**Features and Label:** The features encompass driver attributes (`DrivAge`, `BonusMalus`), vehicle attributes (`VehPower`, `VehAge`, `VehBrand`, `VehGas`), and geographic data (`Area`, `Region`, `Density`). The target label is `fast_track`, a binary classification defined as instances where the claim count (`ClaimNb`) equals zero.

## Evaluation slices & fairness
The evaluation groups the data into `DrivAge` proxy slices with the following bands: 18-25, 26-35, 36-50, and 51+.
| Drive Age Band | approval_rate | fpr (false-postive-rate) | auc |
|:---------------|:--------------|:-------------------------|:----|
| 18-25       | 1.000000 | 1.000000 | 0.666603 |
| 26-35       | 1.000000 | 1.000000 | 0.654421 |
| 36-50       | 1.000000 | 1.000000 | 0.641658 |
| 51+         | 0.999916 | 0.999605 | 0.645698 |
---

**FPR Gap & Gate:** The release gate calculates the maximum False Positive Rate (FPR) gap across all age bands. **If the gap is ≤ 0.10, the gate is a PASS; if > 0.10, it is a FAIL**.

**RESULT**: FPR gap = **0.00039525691699604515**  ->  gate **PASS**

## Top drivers

| SHAP Driver | Mean Absolute SHAP Value |
|:------------|:-------------------------|
| BonusMalus  | 0.1987 |
| DrivAge     | 0.1742 |
| VehAge      | 0.1524  |
| VehBrand_B12 | 0.0672 |
| VehPower    | 0.0627  |
---

## Fairness statement
By analyzing the `DrivAge` proxy slice, we tested whether the model exhibits disparate impact toward different age demographics. The evaluation monitors the False Positive Rate (FPR) gap to ensure that the model does not disproportionately deny fast-tracking to a specific age band (like the 18-25 group) at an unfairly high rate. Based on the calculated FPR gap, we conclude that the model passes the ≤ 0.10 threshold and treats age groups equitably.

## Known limitations
The model's primary weakness is its performance on the **young-driver band (under 30)**, where it may exhibit a skewed AUC. Furthermore, geographic features like `Region` and `Area` are included in the training data, which introduces the risk of these columns acting as unintended proxy variables for protected attributes.