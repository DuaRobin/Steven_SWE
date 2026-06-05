from pydantic import BaseModel


class EvaluationScore(BaseModel):
    factual_accuracy: int
    faithfulness: int
    reasoning: str
