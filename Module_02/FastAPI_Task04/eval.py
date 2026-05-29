from config.app_settings import app_settings
from config.logger_config import setup_logger
from google import genai
from google.genai import types
from models.evaluation_score import EvaluationScore
from models.golden_questions import GoldenQuestion
from identity_token import get_identity_token
import json
import os
import requests

logger = setup_logger(__name__)

# Initialize the Gemini client for the judge model
eval_client = genai.Client(
    vertexai=app_settings.google_genai_use_vertexai,
    project=app_settings.google_cloud_project,
    location=app_settings.google_cloud_location,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def evaluate_system():
    results = []

    # 1. Load the golden dataset
    try:
        with open(f"{BASE_DIR}/golden.jsonl", "r") as f:
            golden_questions = [GoldenQuestion(**json.loads(line)) for line in f]
    except FileNotFoundError:
        logger.error(
            "Error: golden.jsonl not found. Please create it and paste the assignment contents."
        )
        return

    # 2. Hard-cap at 15 questions to prevent runaway costs
    max_questions = min(len(golden_questions), 15)

    total_factual = 0
    total_faithfulness = 0
    successful_evals = 0

    logger.info(f"Starting evaluation of {max_questions} questions...")

    for i in range(max_questions):
        record: GoldenQuestion = golden_questions[i]
        logger.info(f"\nEvaluating [{i+1}/{max_questions}]: {record.question}")

        # 3. Call your local /chat endpoint (Assuming it is running locally on port 8000)
        try:
            # We use stream=True to process the Server-Sent Events
            response = requests.post(
                url="https://rdua1-medicare-policy-chat-api-744841270406.us-east1.run.app/chat",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {get_identity_token()}",
                },
                json={"message": record.question},
                stream=True,
                timeout=30,  # Prevent hanging
            )

            generated_answer = ""
            citations = []

            # Parse the SSE stream to find the final structured JSON event
            for line in response.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        payload = decoded[6:]
                        if payload == "[DONE]":
                            break
                        try:
                            data_json = json.loads(payload)
                            # Our previous schema outputs "answer" and "citations" in the final event
                            if "answer" in data_json and "citations" in data_json:
                                generated_answer = data_json["answer"]
                                citations = data_json["citations"]
                        except json.JSONDecodeError:
                            pass

        except Exception as e:
            print(f"Failed to fetch from /chat endpoint: {e}")
            continue  # Do not loop or retry on failures as per requirements

        # 4. Use Gemini 2.5 Flash as the Judge
        prompt = f"""
        You are an expert evaluator grading an AI system's answer to a Medicare policy question.
        
        Question: {record.question}
        Reference Answer: {record.reference_answer}
        System Answer: {generated_answer}
        System Citations: {json.dumps(citations)}
        
        Score the System Answer on two rubrics from 0 to 5 (0 is worst, 5 is best):
        1. Factual accuracy: How accurate is the System Answer compared with the Reference Answer?
        2. Faithfulness: Does the System Answer only state what the System Citations support? If the system hallucinates details not in the citations, lower this score.
        """

        try:
            judge_response = eval_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=EvaluationScore,
                    temperature=0.0,
                ),
            )

            # Parse the structured JSON output from the judge
            evaluation_score = EvaluationScore.model_validate_json(judge_response.text)

            result_entry = {
                "question": record.question,
                "generated_answer": generated_answer,
                "factual_accuracy": evaluation_score.factual_accuracy,
                "faithfulness": evaluation_score.faithfulness,
                "reasoning": evaluation_score.reasoning,
            }
            results.append(result_entry)

            total_factual += evaluation_score.factual_accuracy
            total_faithfulness += evaluation_score.faithfulness
            successful_evals += 1

            logger.info(
                f"  -> Accuracy: {evaluation_score.factual_accuracy}/5, Faithfulness: {evaluation_score.faithfulness}/5"
            )

        except Exception as e:
            logger.error(f"Failed to evaluate answer using Gemini API: {e}")
            continue  # Do not retry

    # 5. Compute mean scores
    if successful_evals > 0:
        mean_factual = total_factual / successful_evals
        mean_faithfulness = total_faithfulness / successful_evals
    else:
        mean_factual = 0
        mean_faithfulness = 0

    summary = {
        "mean_factual_accuracy": round(mean_factual, 2),
        "mean_faithfulness": round(mean_faithfulness, 2),
        "total_evaluated": successful_evals,
        "results": results,
    }

    # 6. Save results to eval_results.json
    with open(f"{BASE_DIR}/eval_results.json", "w") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"\nEvaluation Complete! Saved to eval_results.json")
    logger.info(f"Mean Factual Accuracy: {summary['mean_factual_accuracy']}/5")
    logger.info(f"Mean Faithfulness: {summary['mean_faithfulness']}/5")


if __name__ == "__main__":
    evaluate_system()
