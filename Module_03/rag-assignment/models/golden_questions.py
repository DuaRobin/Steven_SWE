from pydantic import BaseModel


class GoldenQuestion(BaseModel):
    id: int
    question: str
    reference_answer: str
    source: str
