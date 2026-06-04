from .pdf_chunk import PdfChunk


class PdfEmbedding(PdfChunk):
    embedding_model_version: str = ""
    embedding_timestamp: str = ""
    embedding: list[float] = []
