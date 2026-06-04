# Read PDF's Into Text
from pathlib import Path
from pypdf import PdfReader
import hashlib
import json
import os
import sys
import uuid

# Add workspace to system path for imports
MODULE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(f"{MODULE_DIR}/rag-assignment")
from models.pdf_data import PdfData, PdfPage
from config.logger_config import setup_logger

logger = setup_logger(__name__, log_file="ingest")

PDF_DIRECTORIES = [
    Path(MODULE_DIR, "corpus/benefits_policy_manual"),
    Path(MODULE_DIR, "corpus/claim_processing_manual"),
]


def extract_text_from_pdf(file_path: str) -> PdfData:
    """Reads a PDF file and returns its text content & metadata in schema: PdfData."""
    pdf_data = PdfData()
    pdf_data.source_doc_name = str(Path(file_path).relative_to(MODULE_DIR))
    pdf_data.source_doc_id = str(
        uuid.uuid5(
            namespace=uuid.NAMESPACE_OID,
            name=hashlib.sha256(pdf_data.source_doc_name.encode()).hexdigest(),
        )
    )
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        pdf_data.source_doc_hash = str(
            uuid.uuid5(
                namespace=uuid.NAMESPACE_OID,
                name=hashlib.sha256(file_bytes).hexdigest(),
            )
        )
        # Reset file pointer to the beginning after reading bytes for hashing
        f.seek(0)
        reader = PdfReader(f)
        for page_num, page in enumerate(reader.pages, start=1):
            pdf_page = PdfPage()
            pdf_page.page_number = page_num
            pdf_page.text = page.extract_text()
            pdf_data.pages.append(pdf_page)
    return pdf_data


def read_pdfs(folder_paths: list[Path]) -> list[PdfData]:
    """Loads all PDF files from a folder and returns a list of PdfData objects."""
    all_pdfs_data: list[PdfData] = []
    for folder_path in folder_paths:
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".pdf"):
                logger.info(f"Processing file: {file_name}")
                file_path = os.path.join(folder_path, file_name)
                pdf_data: PdfData = extract_text_from_pdf(file_path=file_path)
                all_pdfs_data.append(pdf_data)
            else:
                logger.warning(f"Skipping non-PDF file: {file_name}")
    return all_pdfs_data


if __name__ == "__main__":
    logger.info("Starting PDF ingestion process...")

    all_pdfs_data: list[PdfData] = read_pdfs(PDF_DIRECTORIES)

    with open(
        file=f"{MODULE_DIR}/output_data/all_pdfs_data.json", mode="w", encoding="utf-8"
    ) as f:
        json.dump(
            [pdf_data.model_dump() for pdf_data in all_pdfs_data],
            fp=f,
            indent=2,
            ensure_ascii=False,
        )

    logger.info(
        f"PDF ingestion completed successfully with {len(all_pdfs_data)} files."
    )
