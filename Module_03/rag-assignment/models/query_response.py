from pydantic import BaseModel


class QueryResponse(BaseModel):
    answer: str
    citations: list[str]
    retrieved_chunks: list[str]
