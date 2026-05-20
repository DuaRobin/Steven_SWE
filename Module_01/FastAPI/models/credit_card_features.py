from pydantic import BaseModel


# Following Model from Public Dataset - bigquery-public-data.ml_datasets.credit_card_default
class CreditCardFeatures(BaseModel):
    limit_balance: float
    sex: str
    education_level: str
    marital_status: str
    age: float
    pay_0: float
    pay_2: float
    pay_3: float
    pay_4: float
    pay_5: str
    pay_6: str
    bill_amt_1: float
    bill_amt_2: float
    bill_amt_3: float
    bill_amt_4: float
    bill_amt_5: float
    bill_amt_6: float
    pay_amt_1: float
    pay_amt_2: float
    pay_amt_3: float
    pay_amt_4: float
    pay_amt_5: float
    pay_amt_6: float
