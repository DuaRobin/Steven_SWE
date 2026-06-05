from fastapi import FastAPI
from pathlib import Path
import sys
import uvicorn

# Add workspace to system path for imports
MODULE_DIR = Path(__file__).resolve().parents[2]
sys.path.append(f"{MODULE_DIR}/rag-assignment")
# Import the schema and functions from your existing modules
from models.pdf_embedding import PdfEmbedding
from models.query_request import QueryRequest
from models.query_response import QueryResponse
from config.logger_config import setup_logger
from serve.retrieve import retrieve_top_chunks
from serve.generate import generate_answer

logger = setup_logger(name=__name__, log_file="api")

# Initialize the FastAPI app
app = FastAPI(title="CMS Policy Assistant API")


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest):
    logger.info(f"Processing query: '{req.question}'")

    # 1. Retrieve the top chunks for the user's question
    pdf_embeddings: list[PdfEmbedding] = await retrieve_top_chunks(
        user_question=req.question
    )

    # 2. Extract chunk texts and format citations using the chunk metadata
    retrieved_chunks = [pdf_embedding.text for pdf_embedding in pdf_embeddings]

    # Use a set to deduplicate citations, formatted as "filename, page_number"
    citations = list(
        set(
            [
                f"{pdf_embedding.source_doc_name}, Page {pdf_embedding.page_number}"
                for pdf_embedding in pdf_embeddings
            ]
        )
    )

    # 3. Generate the answer using Gemini
    answer = await generate_answer(req.question)

    # 4. Return the structured JSON response
    return QueryResponse(
        answer=answer, citations=citations, retrieved_chunks=retrieved_chunks
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
