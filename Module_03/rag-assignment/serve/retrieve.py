import asyncio
import json
import os
import sys
from pathlib import Path
import asyncpg
from pgvector.asyncpg import register_vector
from google import genai
from google.genai import types

# Add workspace to system path for imports
MODULE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(f"{MODULE_DIR}/rag-assignment")
from models.pdf_embedding import PdfEmbedding
from config.app_settings import app_settings
from config.logger_config import setup_logger

logger = setup_logger(name=__name__, log_file="retrieve")

genai_client = genai.Client(
    vertexai=app_settings.google_genai_use_vertexai,
    project=app_settings.google_cloud_project,
    location=app_settings.google_cloud_location,
)


async def retrieve_top_chunks(user_question: str) -> list[PdfEmbedding]:
    """Embeds the user's question, searches pgvector, and returns metadata-rich chunks."""

    async def _get_pool() -> asyncpg.Pool | None:
        db_creds_raw: str = os.getenv("DB_Creds", None)
        if not db_creds_raw:
            raise SystemError(
                "Database Credentials Not Found in Environment Variables."
            )
        try:
            db_creds: dict[str, str] = json.loads(db_creds_raw)
            logger.info("Database Credentials Retrived Successfully.")
            # connection is via cloud-sql-proxy listening on 127.0.0.1 (localhost)
            return await asyncpg.create_pool(
                host="localhost",
                port=5432,
                user=db_creds.get("username", ""),
                password=db_creds.get("password", ""),
                database="rdua1_ragdb",
            )
        except Exception as e:
            raise SystemError(f"Failed to init DB pool: {e}") from e

    # -------------------------------------------------------------------------
    # STEP 1: Embed the question using gemini-embedding-001
    # -------------------------------------------------------------------------
    # CRITICAL: task_type MUST be "RETRIEVAL_QUERY" at search time.
    # Mismatching this causes recall to silently drop by 30-40 points.
    response = await genai_client.aio.models.embed_content(
        model="gemini-embedding-001",
        contents=user_question,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768,  # Must match the DB index dimensionality
        ),
    )
    query_embedding = response.embeddings[0].values
    logger.info("Query Embedding Generated Successfully.")

    # -------------------------------------------------------------------------
    # STEP 2: Search the database using pgvector's <=> operator [cosine distance]
    # -------------------------------------------------------------------------
    # Retrieve Database Credentials from environment variables
    pool: asyncpg.Pool | None = None
    try:
        pool = await _get_pool()
        logger.info("✅ Database Pool Initialized Successfully.")
        async with pool.acquire() as conn:
            await register_vector(conn)
            rows = await conn.fetch(
                """
                SELECT
                    chunk_id, source_doc_id, source_doc_name, page_number,
                    page_chunk_index, page_chunk_offset, text
                FROM document_chunks
                ORDER BY embedding <=> $1
                LIMIT 5;
                """,
                query_embedding,
            )
    finally:
        if pool:
            await pool.close()
            logger.info("🏊🏻 DB Pool Closed.")

    # -------------------------------------------------------------------------
    # STEP 3: Return chunks and source metadata
    # -------------------------------------------------------------------------
    # Map the resulting SQL records back to the PdfChunk Pydantic schema
    top_pdf_embeddings: list[PdfEmbedding] = []
    for row in rows:
        pdf_embedding = PdfEmbedding(
            chunk_id=row["chunk_id"],
            source_doc_id=row["source_doc_id"],
            source_doc_name=row["source_doc_name"],
            page_number=row["page_number"],
            page_chunk_index=row["page_chunk_index"],
            page_chunk_offset=row["page_chunk_offset"],
            text=row["text"],
        )
        top_pdf_embeddings.append(pdf_embedding)

    return top_pdf_embeddings


# Example execution
if __name__ == "__main__":
    question = "What is the policy for flood damage?"
    pdf_embeddings = asyncio.run(retrieve_top_chunks(user_question=question))
    logger.info(f"Question: '{question}'")
    logger.info(f"Retrieved {len(pdf_embeddings)} chunks:")
    logger.info(
        json.dumps(
            [
                pdf_embedding.model_dump(exclude_unset=True)
                for pdf_embedding in pdf_embeddings
            ],
            indent=2,
        )
    )
