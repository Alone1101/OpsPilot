import os
import logging
from dotenv import load_dotenv
from agents import gemini_client, ollama_client

load_dotenv()

logger = logging.getLogger(__name__)

LLM_PROVIDER = os.getenv("LLM_PROVIDER")

def classify_request(message: str):
    logger.info("LLM provider: %s", LLM_PROVIDER)

    if LLM_PROVIDER == "gemini":
        return gemini_client.classify_request(message)

    if LLM_PROVIDER == "ollama":
        return ollama_client.classify_request(message)

    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def decide_tool(message: str):
    logger.info("LLM provider: %s", LLM_PROVIDER)

    if LLM_PROVIDER == "gemini":
            return gemini_client.decide_tool(message)
    
    if LLM_PROVIDER == "ollama":
        return ollama_client.decide_tool(message)

    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def generate_text(prompt: str) -> str:
    logger.info("LLM provider: %s", LLM_PROVIDER)
    
    if LLM_PROVIDER == "gemini":
        return gemini_client.generate_text(prompt)
         
    if LLM_PROVIDER == "ollama":
        return ollama_client.generate_text(prompt)

    raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")