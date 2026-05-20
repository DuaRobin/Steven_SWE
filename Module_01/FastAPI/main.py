from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from models.credit_card_features import CreditCardFeatures
from config.app_settings import app_settings

app = FastAPI(title=app_settings.app_name)
bq_client = bigquery.Client()


@app.get("/health")
async def health_default() -> dict[str, str]:
    app_name = app_settings.app_name
    app_version = app_settings.app_version
    env = app_settings.environment

    if not all([app_name, app_version, env]):
        raise HTTPException(
            status_code=500,
            detail="Server configuration environment variables missing.",
        )

    return {
        "App Name": app_name,
        "App Version": app_version,
        "Running in Environment": env,
    }


@app.post("/predict")
async def predict_default(features: CreditCardFeatures):
    # Construct the ML.PREDICT query using parameterized inputs
    bq_query = f"""
    SELECT
        predicted_default_payment_next_month,
        predicted_default_payment_next_month_probs
    FROM ML.PREDICT(
      MODEL `{app_settings.ml_model_id}`,
      (
        SELECT 
          @limit_balance AS limit_balance,
          @sex AS sex,
          @education_level AS education_level,
          @marital_status AS marital_status,
          @age AS age,
          @pay_0 AS pay_0,
          @pay_2 AS pay_2,
          @pay_3 AS pay_3,
          @pay_4 AS pay_4,
          @pay_5 AS pay_5,
          @pay_6 AS pay_6,
          @bill_amt_1 AS bill_amt_1,
          @bill_amt_2 AS bill_amt_2,
          @bill_amt_3 AS bill_amt_3,
          @bill_amt_4 AS bill_amt_4,
          @bill_amt_5 AS bill_amt_5,
          @bill_amt_6 AS bill_amt_6,
          @pay_amt_1 AS pay_amt_1,
          @pay_amt_2 AS pay_amt_2,
          @pay_amt_3 AS pay_amt_3,
          @pay_amt_4 AS pay_amt_4,
          @pay_amt_5 AS pay_amt_5,
          @pay_amt_6 AS pay_amt_6
      )
    )
    """

    # Map Pydantic fields to BigQuery parameters to prevent SQL injection
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter(
                key, "STRING" if isinstance(value, str) else "FLOAT64", value
            )
            for key, value in features.model_dump().items()
        ]
    )

    try:
        # Execute the query (Expected latency 1-3 seconds)
        query_job = bq_client.query(query=bq_query, job_config=job_config)
        results = query_job.result()

        # Extract the prediction result
        for row in results:
            return {
                "predicted_label": row.predicted_default_payment_next_month,
                "predicted_probability": row.predicted_default_payment_next_month_probs,
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
