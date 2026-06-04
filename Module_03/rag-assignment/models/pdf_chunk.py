from pydantic import BaseModel


class PdfChunk(BaseModel):
    chunk_id: str = ""
    source_doc_id: str = ""
    source_doc_name: str = ""
    page_number: int = 0
    page_chunk_index: int = 0
    page_chunk_offset: int = 0
    text: str = ""
    text_length: int = 0
    ingest_timestamp: str = ""
    chunker_version: str = ""
