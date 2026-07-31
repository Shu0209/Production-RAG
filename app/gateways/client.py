import logfire
from langchain_openai import ChatOpenAI
from portkey_ai import (
    PORTKEY_GATEWAY_URL,
    createHeaders,
)

from app.config import settings


# -------------------------------------------------------------------
# Portkey Gateway Configuration
# -------------------------------------------------------------------

# This is Our Gateway Config with we paste in portkey
                 

# GATEWAY_CONFIG = {
#     "strategy": {
#         "mode": "fallback"
#     },

#     "cache": {
#         "mode": "simple"
#     },

#     "retry": {
#         "attempts": 3,
#         "on_status_codes": [
#             429,
#             500,
#             502,
#             503,
#             504,
#         ],
#     },

#     "targets": [
#         {
#             "override_params": {
#                 "model": f"@{settings.GROQ_SLUG_1}/llama-3.1-8b-instant"
#             }
#         },
#         {
#             "override_params": {
#                 "model": f"@{settings.OPENROUTER_SLUG_2}/openai/gpt-oss-20b:free"
#             }
#         },
#     ],
# }


# -------------------------------------------------------------------
# Shared LLM Factory
# -------------------------------------------------------------------

def get_langchain_llm(feature: str = "rag",temperature: float = 0,max_tokens: int = 1024,) -> ChatOpenAI:
    """
    Returns a production-ready LangChain LLM using the Portkey Gateway.

    Gateway handles:
    - Provider routing
    - Retry
    - Cache
    - Fallback
    """

    return ChatOpenAI(
        api_key=settings.portkey_api_key,

        base_url=PORTKEY_GATEWAY_URL,

        # Initial target.
        # If this provider fails Portkey automatically
        # follows the fallback chain defined above.
        model=f"@{settings.GROQ_SLUG_1}/llama-3.1-8b-instant",

        temperature=temperature,

        max_tokens=max_tokens,

        timeout=60,

        max_retries=0,

        default_headers=createHeaders(
            api_key=settings.portkey_api_key,

            config=settings.portkey_config_id,

            metadata={
                "service": "blockcost-chatbot",
                "environment": "production",
                "feature": feature,
                "_user": "rag-system",
            },
        ),
    )


# -------------------------------------------------------------------
# Utility
# -------------------------------------------------------------------

def extract_cache_status(response) -> str:
    """
    Returns Portkey cache status.

    HIT
    MISS
    BYPASS
    """

    for attr in ("_raw_response","_response","_http_response"):
        raw = getattr(response, attr, None)

        if raw is None:
            continue

        headers = getattr(raw, "headers", None)

        if headers:
            status = headers.get("x-portkey-cache-status")
            if status:
                return status.upper()

    return "MISS"