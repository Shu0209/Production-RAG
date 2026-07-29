import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    gemini_api_key=os.getenv("GEMINI_API_KEY")

    llm_api_key=os.getenv("LLM_API_KEY")
    llm_model="openai/gpt-oss-20b:free"
    llm_model_api_base="https://openrouter.ai/api/v1"

    qdrant_api_key=os.getenv("QDRANT_API_KEY")
    qdrant_url=os.getenv("QDRANT_CLUSTER_ENDPOINT")
    qdrant_collection="rag-chatbot"

    CHUNK_SIZE=800
    CHUNK_OVERLAP=350



settings=Settings()



