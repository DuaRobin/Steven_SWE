from datetime import datetime
from pathlib import Path
from pgvector.asyncpg import register_vector
import asyncio
import asyncpg
import json
import os
import sys

# Add workspace to system path for imports
MODULE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(f"{MODULE_DIR}/rag-assignment")
from models.pdf_embedding import PdfEmbedding
from config.logger_config import setup_logger

logger = setup_logger(__name__, log_file="store")


def read_sql_file(file_path: Path) -> str:
    with open(file_path, mode="r", encoding="utf-8") as f:
        return f.read()


async def store_embeddings_to_db() -> None:
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

    pool: asyncpg.Pool | None = None
    try:
        pool = await _get_pool()
        async with pool.acquire() as conn:
            logger.info("✅ Database Pool Initialized Successfully.")

            # Capture PostgreSQL notices/warnings directly to your logger
            conn.add_log_listener(
                lambda connection, message: logger.info(f"🐘 DB Notice: {message}")
            )

            # Enable Extension vector, if needed.
            r = await conn.execute(
                read_sql_file(
                    f"{MODULE_DIR}/rag-assignment/ingest/sql/create_extension_vector.sql"
                )
            )
            logger.info(f"🛠️ Extension (vector) creation status: {r}")
            # Register Vector Type - It helps educate database drive (asyncpg)
            # about data types including vector
            await register_vector(conn)
            # Create Table if not exists
            r = await conn.execute(
                read_sql_file(
                    f"{MODULE_DIR}/rag-assignment/ingest/sql/create_table_document_chunks.sql"
                )
            )
            logger.info(f"📄 Table creation status: {r}")
            # Load Embedded Chunks
            with open(
                file=f"{MODULE_DIR}/output_data/all_pdfs_embeddings.json", mode="r"
            ) as f:
                all_pdfs_embeddings: list[PdfEmbedding] = [
                    PdfEmbedding.model_validate(pdf_embedding)
                    for pdf_embedding in json.load(f)
                ]
            # Insert Each Chunk with Embedding & Metadata into DB
            records = [
                (
                    pdf_embedding.chunk_id,
                    pdf_embedding.source_doc_id,
                    pdf_embedding.source_doc_name,
                    pdf_embedding.page_number,
                    pdf_embedding.page_chunk_index,
                    pdf_embedding.page_chunk_offset,
                    pdf_embedding.text,
                    pdf_embedding.chunker_version,
                    pdf_embedding.embedding_model_version,
                    datetime.fromisoformat(pdf_embedding.embedding_timestamp),
                    pdf_embedding.embedding,
                )
                for pdf_embedding in all_pdfs_embeddings
            ]
            async with conn.transaction():
                await conn.executemany(
                    read_sql_file(
                        f"{MODULE_DIR}/rag-assignment/ingest/sql/insert_document_chunks.sql"
                    ),
                    records,
                )
                logger.info(f"✅ Successfully inserted {len(records)} document chunks.")
            # create index
            r = await conn.execute(
                read_sql_file(
                    f"{MODULE_DIR}/rag-assignment/ingest/sql/create_index_on_embedding.sql"
                )
            )
            logger.info(f"📄 Index creation status: {r}")

    except Exception as e:
        logger.error(f"❌ Database Pool Initialization Failed: {e}")
        raise e
    finally:
        if pool:
            await pool.close()
            logger.info("🏊🏻 DB Pool Closed.")


# endregion

if __name__ == "__main__":
    logger.info("🪂 Starting Embedding Store Process...")
    asyncio.run(store_embeddings_to_db())
    logger.info("🪂 Embedding Process Completed Successfully...")
