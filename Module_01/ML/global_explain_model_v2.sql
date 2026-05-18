SELECT *
FROM 
  ML.GLOBAL_EXPLAIN(MODEL `rdua1_ml.default_risk_v2`)
ORDER BY 
  attribution DESC
LIMIT 5;