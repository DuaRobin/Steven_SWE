from config.app_settings import app_settings
from config.logger_config import setup_logger
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from google import genai
from google.genai import types
from models.chat_request import ChatRequest
from models.chat_response import Citation, GroundedResponse
import json

logger = setup_logger(__name__)
app = FastAPI(title=app_settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

genai_client = genai.Client(
    vertexai=app_settings.google_genai_use_vertexai,
    project=app_settings.google_cloud_project,
    location=app_settings.google_cloud_location,
)
SYSTEM_INSTRUCTION = """
Use only the provided context from the CMS Medicare Benefits Policy Manual.
If the answer is not in the context, say you don't know."
"""

DATASTORE_PATH = f"projects/{app_settings.google_cloud_project}/locations/{app_settings.data_store_region}/collections/default_collection/dataStores/{app_settings.data_store_id}"
GROUNDING_TOOL = types.Tool(
    retrieval=types.Retrieval(
        vertex_ai_search=types.VertexAISearch(datastore=DATASTORE_PATH)
    )
)


@app.get("/health")
async def health_default() -> Response:
    app_name = app_settings.app_name
    app_version = app_settings.app_version
    env = app_settings.environment

    if not all([app_name, app_version, env]):
        raise HTTPException(
            status_code=500,
            detail="Server configuration environment variables missing.",
        )

    response_data = {
        "App Name": app_name,
        "App Version": app_version,
        "Running in Environment": env,
    }
    return Response(content=json.dumps(response_data), media_type="application/json")


@app.post("/chat")
async def chat_default(req: ChatRequest):
    async def event_generator():
        try:
            # Use the async SDK method as requested
            response_stream = await genai_client.aio.models.generate_content_stream(
                model=app_settings.model_name,
                contents=req.message,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=app_settings.model_config_temprature,
                    max_output_tokens=app_settings.model_config_max_output_tokens,
                    tools=[GROUNDING_TOOL],
                    safety_settings=[
                        types.SafetySetting(
                            category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                            threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                        )
                    ],
                ),
            )

            full_answer = ""
            grounding_metadata: types.GroundingMetadata = None

            # 1: Iterate over the stream and yield SSE format, While Accumulating the full answer and
            #    capturing grounding metadata when it arrives (typically in the final chunk) for later processing
            async for chunk in response_stream:
                if chunk.text:
                    full_answer += chunk.text
                    yield f"data: {json.dumps({'delta': chunk.text})}\n\n"
                # Capture grounding metadata (typically arrives in the final chunk)
                if chunk.candidates and chunk.candidates[0].grounding_metadata:
                    grounding_metadata = chunk.candidates[0].grounding_metadata

            # 2. Extract structured citation data from grounding_metadata
            citations = []
            confidence_scores = []
            is_grounded = True

            if grounding_metadata and grounding_metadata.grounding_supports:
                chunks = grounding_metadata.grounding_chunks or []
                supports = grounding_metadata.grounding_supports or []

                for support in supports:
                    # Accumulate confidence scores
                    if support.confidence_scores:
                        confidence_scores.extend(support.confidence_scores)

                    # Extract segment text (the quote)
                    quote = support.segment.text if support.segment else ""

                    # Map chunk indices to source URIs
                    if support.grounding_chunk_indices and chunks:
                        for idx in support.grounding_chunk_indices:
                            uri = "unknown"
                            if idx < len(chunks):
                                chunk_obj = chunks[idx]
                                if (
                                    chunk_obj.retrieved_context
                                    and chunk_obj.retrieved_context.uri
                                ):
                                    uri = chunk_obj.retrieved_context.uri
                                elif chunk_obj.web and chunk_obj.web.uri:
                                    uri = chunk_obj.web.uri
                            citations.append(Citation(source_uri=uri, quote=quote))
                    else:
                        citations.append(Citation(source_uri="unknown", quote=quote))

            # 3. Calculate mean confidence
            # Testing/Debugging Is Showing that we get grounding metadata with no confidence scores, but we do have citations.
            # In those cases, we will assume a default confidence of 1.0 if there are citations but no confidence scores, and 0.0 confidence if there are no citations at all.
            mean_confidence = (
                sum(confidence_scores) / len(confidence_scores)
                if confidence_scores
                else 1.0 if len(citations) > 0 else 0.0
            )

            # 4. Confidence-based fallback logic
            if not grounding_metadata or mean_confidence < 0.5:
                logger.warning(
                    "Fallback triggered: No grounding metadata found in the response OR confidence score low (< 0.5)"
                )
                is_grounded = False
                full_answer = "I don't have enough information from the Medicare Benefits Policy Manual to answer that question."

            # 5. Validate with Pydantic
            final_response = GroundedResponse(
                answer=full_answer,
                citations=citations,
                confidence=mean_confidence,
                is_grounded=is_grounded,
            )

            # 6. Emit the full structured response as the final SSE event
            yield f"data: {json.dumps(final_response.model_dump())}\n\n"

            # Terminate stream
            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Error during content generation: {e}")
            yield f"data: [ERROR] {str(e)}\n\n"

    # Return as text/event-stream with headers required for Cloud Run streaming
    return StreamingResponse(
        content=event_generator(),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no", "Cache-Control": "no-cache"},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
    logger.info(f"Started {app_settings.app_name}, Listening on http://0.0.0.0:8080")
