INSERT INTO document_chunks (
    chunk_id, source_doc_id, source_doc_name, page_number,
    page_chunk_index, page_chunk_offset, text, chunker_version,
    embedding_model_version, embedding_timestamp, embedding)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    ON CONFLICT (chunk_id) DO NOTHING;