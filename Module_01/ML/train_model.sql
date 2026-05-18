CREATE OR REPLACE MODEL `rdua1_ml.default_risk_v1`
OPTIONS(
  model_type = 'BOOSTED_TREE_CLASSIFIER',
  input_label_cols = ['default_payment_next_month'],
  data_split_method = 'RANDOM',
  data_split_eval_fraction = 0.2,
  ENABLE_GLOBAL_EXPLAIN = TRUE
) AS
SELECT
  limit_balance,
  sex,
  education_level,
  marital_status,
  age,
  pay_0,
  pay_2,
  pay_3,
  pay_4,
  pay_5,
  pay_6,
  bill_amt_1,
  bill_amt_2,
  bill_amt_3,
  bill_amt_4,
  bill_amt_5,
  bill_amt_6,
  pay_amt_1,
  pay_amt_2,
  pay_amt_3,
  pay_amt_4,
  pay_amt_5,
  pay_amt_6,
  default_payment_next_month
FROM
  `bigquery-public-data.ml_datasets.credit_card_default`;