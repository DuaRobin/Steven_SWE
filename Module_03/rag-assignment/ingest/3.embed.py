from datetime import datetime, timezone
from google import genai
from google.genai import types
from pathlib import Path
import asyncio
import json
import sys

# Add workspace to system path for imports
MODULE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(f"{MODULE_DIR}/rag-assignment")
from models.pdf_embedding import PdfEmbedding
from config.app_settings import app_settings
from config.logger_config import setup_logger

logger = setup_logger(name=__name__, log_file="embed")

genai_client = genai.Client(
    vertexai=app_settings.google_genai_use_vertexai,
    project=app_settings.google_cloud_project,
    location=app_settings.google_cloud_location,
)
semaphore = asyncio.Semaphore(5)  # Max 5 concurrent calls to avoid rate limits


async def generate_embedding(text: str) -> list[float]:
    """Generates an embedding for a single text chunk with retry logic."""
    async with semaphore:
        for attempt in range(5):
            try:
                response = await genai_client.aio.models.embed_content(
                    model=app_settings.embedding_model_name,  # "gemini-embedding-001" from .env
                    contents=text,
                    config=types.EmbedContentConfig(
                        # CRITICAL: Must be RETRIEVAL_DOCUMENT at ingestion time
                        task_type="RETRIEVAL_DOCUMENT",
                        # OPTIONAL: Truncate to 768 dimensions for storage efficiency
                        output_dimensionality=768,
                    ),
                )
                return response.embeddings[0].values
            except Exception as e:
                if attempt < 4:
                    delay = 15 * (2**attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    raise e


async def process_embeddings():
    with open(
        file=f"{MODULE_DIR}/output_data/all_pdfs_chunks.json",
        mode="r",
        encoding="utf-8",
    ) as f:
        # PdfEmbedding inherits from PdfChunk
        all_pdfs_embeddings: list[PdfEmbedding] = [
            PdfEmbedding.model_validate(pdf_chunk) for pdf_chunk in json.load(f)
        ]

    logger.info(f"Embedding {len(all_pdfs_embeddings)} chunks...")

    # Create coroutines for all chunks
    tasks = [
        generate_embedding(pdf_embedding.text) for pdf_embedding in all_pdfs_embeddings
    ]

    # Execute concurrently and gather results
    all_chunk_embeddings: list[list[float]] = await asyncio.gather(*tasks)

    # Map embeddings back to their respective chunks
    for pdf_embedding, chunk_embedding in zip(
        all_pdfs_embeddings, all_chunk_embeddings
    ):
        pdf_embedding.embedding = chunk_embedding
        pdf_embedding.embedding_model_version = app_settings.embedding_model_name
        pdf_embedding.embedding_timestamp = datetime.now(timezone.utc).isoformat()

    # Save The Embeddings
    with open(
        file=f"{MODULE_DIR}/output_data/all_pdfs_embeddings.json",
        mode="w",
        encoding="utf-8",
    ) as f:
        json.dump(
            [pdf_embedding.model_dump() for pdf_embedding in all_pdfs_embeddings],
            f,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    logger.info("Starting embedding process...")
    asyncio.run(process_embeddings())
    logger.info("All embeddings generated and saved successfully.")
