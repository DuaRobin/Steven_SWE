from pydantic import BaseModel


class Citation(BaseModel):
    source_uri: str
    quote: str


class GroundedResponse(BaseModel):
    answer: str
    citations: list[Citation]
    confidence: float
    is_grounded: bool
