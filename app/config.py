import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    gemini_api_key=os.getenv("GEMINI_API_KEY")

    llm_api_key=os.getenv("OPENROUTER_API_KEY")
    llm_model="openai/gpt-oss-20b:free"
    llm_model_api_base="https://openrouter.ai/api/v1"

    qdrant_api_key=os.getenv("QDRANT_API_KEY")
    qdrant_url=os.getenv("QDRANT_CLUSTER_ENDPOINT")
    qdrant_collection="rag-chatbot"

    groq_api_key=os.getenv("GROQ_API_KEY")

    CHUNK_SIZE=800
    CHUNK_OVERLAP=350


    portkey_api_key=os.getenv("PORTKEY_API_KEY")
    portkey_config_id=os.getenv("PORTKEY_CONFIG_ID")

    GROQ_SLUG_1 =  "api1" 
    OPENROUTER_SLUG_2 =  "api2"    
  



settings=Settings()



