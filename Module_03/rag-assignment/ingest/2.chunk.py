from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys
import uuid

# Add workspace to system path for imports
MODULE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(f"{MODULE_DIR}/rag-assignment")
from models.pdf_data import PdfData
from models.pdf_chunk import PdfChunk
from config.logger_config import setup_logger

logger = setup_logger(name=__name__, log_file="chunk")

# The embedding model (gemini-embedding-001) has a 2,048-token input limit
# Target ~1000 characters to stay safely under the ~ 1200 including overlap text
CHUNK_MAX_CHARS = 1000
OVERLAP_CHARS = 200

all_pdfs_chunks: list[PdfChunk] = []


def get_sub_paragraphs(p: str) -> list[str]:
    sub_paragraphs = []
    while len(p) > CHUNK_MAX_CHARS:
        # Try to split at the last space within the limit
        split_point = p.rfind(" ", 0, CHUNK_MAX_CHARS)
        if split_point == -1:
            split_point = CHUNK_MAX_CHARS
        sub_paragraphs.append(p[:split_point])
        p = p[split_point:].strip()
    if p:
        sub_paragraphs.append(p)
    return sub_paragraphs


def add_chunk(
    pdf_data: PdfData,
    page_chunk_index: int,
    page_chunk_offset: int,
    current_chunk: str,
    current_chunk_start_page: int,
) -> None:
    chunk_id_str = (
        f"{pdf_data.source_doc_id}-{current_chunk_start_page}-{page_chunk_offset}"
    )
    chunk_id = str(
        uuid.uuid5(
            namespace=uuid.NAMESPACE_OID,
            name=hashlib.sha256(data=chunk_id_str.encode()).hexdigest(),
        )
    )
    pdf_chunk = PdfChunk(
        chunk_id=chunk_id,
        source_doc_id=pdf_data.source_doc_id,
        source_doc_name=pdf_data.source_doc_name,
        page_number=current_chunk_start_page,
        page_chunk_index=page_chunk_index,
        page_chunk_offset=page_chunk_offset,
        text=current_chunk.strip(),
        text_length=len(current_chunk.strip()),
        ingest_timestamp=datetime.now(timezone.utc).isoformat(),
        chunker_version=f"fixed_size_{CHUNK_MAX_CHARS}_{OVERLAP_CHARS}",
    )
    all_pdfs_chunks.append(pdf_chunk)


def build_pdf_chunks_fixed_size(pdf_data: PdfData) -> None:
    """Splits the text of a PDF document into its chunks based on character limits."""

    # Ensure pages are sorted sequentially
    pdf_data.pages.sort(key=lambda x: x.page_number)

    current_chunk = ""
    page_chunk_index = 0
    page_chunk_offset = 0
    current_chunk_start_page = pdf_data.pages[0].page_number if pdf_data.pages else 1

    for pdf_page in pdf_data.pages:
        paragraphs = pdf_page.text.split("\n\n")

        for p in paragraphs:
            p = p.strip()
            if not p:
                continue

            # Split large paragraphs to ensure they don't exceed the max size
            sub_paragraphs = get_sub_paragraphs(p)

            for sp in sub_paragraphs:
                # exactly once (first chunk)
                if not current_chunk:
                    current_chunk_start_page = pdf_page.page_number
                    current_chunk = sp
                else:
                    # Check if adding this paragraph would exceed the chunk limit
                    if len(current_chunk) + len(sp) <= CHUNK_MAX_CHARS:
                        current_chunk += "\n\n" + sp
                    else:
                        # Save the current chunk first before starting a new one
                        page_chunk_index += 1
                        add_chunk(
                            pdf_data=pdf_data,
                            page_chunk_index=page_chunk_index,
                            page_chunk_offset=page_chunk_offset,
                            current_chunk=current_chunk,
                            current_chunk_start_page=current_chunk_start_page,
                        )

                        # Start the next chunk with the overlap
                        overlap_text = (
                            current_chunk[-OVERLAP_CHARS:]
                            if len(current_chunk) > OVERLAP_CHARS
                            else current_chunk
                        )
                        current_chunk_start_page = pdf_page.page_number
                        page_chunk_offset += len(current_chunk) - len(overlap_text)
                        current_chunk = overlap_text + "\n\n" + sp

    # Catch the final chunk for the document
    if current_chunk.strip():
        page_chunk_index += 1
        add_chunk(
            pdf_data=pdf_data,
            page_chunk_index=page_chunk_index,
            page_chunk_offset=page_chunk_offset,
            current_chunk=current_chunk,
            current_chunk_start_page=current_chunk_start_page,
        )


def process_all_pdfs_data_for_chunks(file_path: Path) -> None:
    with open(file=file_path, mode="r", encoding="utf-8") as f:
        all_pdfs_data: list[PdfData] = [
            PdfData.model_validate(pdf_data) for pdf_data in json.load(f)
        ]
    for pdf_data in all_pdfs_data:
        previous_chunks_count = len(all_pdfs_chunks)
        build_pdf_chunks_fixed_size(pdf_data)
        logger.info(
            f"Created {len(all_pdfs_chunks) - previous_chunks_count} chunks for PDF '{pdf_data.source_doc_name}'."
        )


if __name__ == "__main__":
    logger.info("Starting PDF chunking process...")
    process_all_pdfs_data_for_chunks(
        file_path=Path(MODULE_DIR, "output_data/all_pdfs_data.json")
    )
    with open(
        file=f"{MODULE_DIR}/output_data/all_pdfs_chunks.json",
        mode="w",
        encoding="utf-8",
    ) as f:
        json.dump(
            [pdf_chunk.model_dump() for pdf_chunk in all_pdfs_chunks],
            f,
            ensure_ascii=False,
            indent=2,
        )
    logger.info(
        f"PDF chunking completed successfully, created {len(all_pdfs_chunks)} chunks."
    )
