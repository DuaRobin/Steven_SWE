from config.app_settings import app_settings
from config.logger_config import setup_logger
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse
from google import genai
from google.genai import types
from models.chat_request import ChatRequest
import json

logger = setup_logger(__name__)
app = FastAPI(title=app_settings.app_name)
genai_client = genai.Client(
    vertexai=app_settings.google_genai_use_vertexai,
    project=app_settings.google_cloud_project,
    location=app_settings.google_cloud_location,
)
SYSTEM_INSTRUCTION = """
You are an assistant scoped to answer questions related to Medicare policy
using the CMS Benefits Policy Manual as your knowledge base.
When you don't know the answer, say you don't know. Do not make up an answer.
"""


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
        # Use the async SDK method as requested
        response_stream = await genai_client.aio.models.generate_content_stream(
            model=app_settings.model_name,
            contents=req.message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=app_settings.model_config_temprature,
                max_output_tokens=app_settings.model_config_max_output_tokens,
                safety_settings=[
                    types.SafetySetting(
                        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
                    )
                ],
            ),
        )

        # Iterate over the stream and yield SSE format
        async for chunk in response_stream:
            if chunk.text:
                data = json.dumps({"delta": chunk.text})
                yield f"data: {data}\n\n"

        # Terminate with [DONE]
        yield "data: [DONE]\n\n"

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
