CREATE TABLE IF NOT EXISTS document_chunks (
    chunk_id VARCHAR PRIMARY KEY,
    source_doc_id VARCHAR,
    source_doc_name VARCHAR,
    page_number INT,
    page_chunk_index INT,
    page_chunk_offset INT,
    text TEXT,
    chunker_version VARCHAR,
    embedding_model_version VARCHAR,
    embedding_timestamp TIMESTAMPTZ,
    embedding vector(768)
);