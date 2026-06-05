from google import genai
from google.genai.types import Content, Part, GenerateContentConfig
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
from serve.retrieve import genai_client, retrieve_top_chunks

logger = setup_logger(name=__name__, log_file="generate")

# Define the strict system instruction per your requirements
SYSTEM_PROMPT = """
You are a helpful expert CMS Policy Assistant. Follow these strict rules:
1. Only answer based on the provided context.
2. Say "I don't have enough information" if the context doesn't cover the question.
3. Include inline citations in the format [source: filename, page_number].
"""


async def generate_answer(user_question: str) -> str:
    """Sends the retrieved chunks and user question to Gemini to generate a grounded answer."""

    # -------------------------------------------------------------------------
    # STEP 1: Retrieve chunks from database based on distance search, then create context
    # -------------------------------------------------------------------------
    retrieved_chunks: list[PdfEmbedding] = await retrieve_top_chunks(
        user_question=user_question
    )
    context_parts = [Part.from_text(text="Context:\n")]
    for chunk in retrieved_chunks:
        # We explicitly label the filename and section (using page_number)
        # so the LLM can properly format the requested inline citations.
        formatted_chunk = Part.from_text(
            text=(
                f"filename: {chunk.source_doc_name}\n"
                f"page_number: page {chunk.page_number}\n"
                f"text: {chunk.text}\n---\n"
            )
        )
        context_parts.append(formatted_chunk)

    # Add the user question as the final part
    context_parts.append(Part.from_text(text=f"User Question: {user_question}"))

    # Assemble the final prompt payload using the Content model
    prompt = Content(role="user", parts=context_parts)

    # -------------------------------------------------------------------------
    # STEP 2: Call Gemini 2.5 Flash with specific configurations
    # -------------------------------------------------------------------------
    response = await genai_client.aio.models.generate_content(
        model=app_settings.model_name,  # gemini-2.5-flash from .env,
        contents=prompt,
        config=GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            max_output_tokens=800,
        ),
    )
    return response.text.strip()


# Example execution
if __name__ == "__main__":
    question = "Is flood damage covered?"
    question = "When can Part B payment be made for hospital inpatient services after a Part A denial?"
    answer = asyncio.run(generate_answer(question))
    logger.info(f"Question: {question}")
    logger.info(f"Answer: {answer}")
