import os
from dotenv import load_dotenv
from google import genai
from sqlalchemy.orm import Session
from services.retrieval_service import retrieve_policies

load_dotenv()

client = genai.Client(api_key = os.getenv("GEMINI_API_KEY"))

def answer_policy_question(db: Session, question: str) -> str:
    policies = retrieve_policies(
        db = db,
        query = question,
        limit = 3
    )

    context = "\n\n".join(policy.content for policy in policies)

    prompt = f"""
    You are a customer operations assitant.

    Answer the user's question using only the policy context provided below.

    If the policy context does not contain enough information to answer the question, say that the available policy does not provide enough information.

    POLICY CONTEXT:
    {context}

    USER QUESTION:
    {question}
    """

    response = client.models.generate_content(
        model = "gemini-3.6-flash",
        contents = prompt
    )

    return response.text