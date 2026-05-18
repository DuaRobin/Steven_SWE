SELECT
  accuracy,
  precision,
  recall,
  roc_auc
FROM
  ML.EVALUATE(MODEL `rdua1_ml.default_risk_v2`);

SELECT 
  accuracy,
  precision,
  recall,
  roc_auc
FROM ML.EVALUATE(MODEL `rdua1_ml.default_risk_v2`,
  (
    SELECT *
    FROM `bigquery-public-data.ml_datasets.credit_card_default`
  ),
  STRUCT(0.50 AS threshold)
);
