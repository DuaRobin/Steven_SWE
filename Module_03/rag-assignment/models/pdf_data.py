from pydantic import BaseModel


class PdfPage(BaseModel):
    page_number: int = 0
    text: str = ""


class PdfData(BaseModel):
    source_doc_id: str = ""
    source_doc_name: str = ""
    source_doc_hash: str = ""
    pages: list[PdfPage] = []
