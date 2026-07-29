from app.agents.state import AgentState
from app.config import settings
from langchain_openai import ChatOpenAI
import logfire

llm = ChatOpenAI(
    model=settings.llm_model, 
    openai_api_base=settings.llm_model_api_base,
    openai_api_key=settings.llm_api_key,
    temperature=0.3,
    max_tokens=512,
)


def planner_node(state: AgentState):
    """The Planner determines if a search is neede based on the Entire conversation"""

    # Get the converstation history (excluding the last message)

    history=""
    for msg in state["messages"][:-1]:
        role= "User" if msg["role"]=="user" else "Assistant"
        history +=f"{role}: {msg['content']}\n"

    user_message=state["messages"][-1]["content"] if state["messages"] else ""

    prompt = f"""
    You are an intelligent Assistant Planner. 
    Analyze the conversation history and the latest user message.
    
    CONVERSATION HISTORY:
    {history}
    
    LATEST MESSAGE:
    "{user_message}"
    
    Task:
    1. If the latest message is a greeting (hi, hello) or a question that can be answered using ONLY the conversation history above (e.g., "what is my name"), respond with 'CONVERSATIONAL'.
    2. If it is a technical question about Kubernetes, Intel, or Networking that requires fresh documentation, output a refined search query.
    
    Output ONLY 'CONVERSATIONAL' or the search query.
    """
    with logfire.span("🧠 Planning Decision"):
        decision=llm.invoke(prompt).content.strip()
        logfire.info(f"Intent identified: {decision}")


    if decision=="CONVERSATIONAL":
        return{
            "current_query":"CONVERSATIONAL",
            "status":"Handling conversationally (using memory)...",
            "plan":["Intent: Conversational/Memory", "Retrieval: Skipped"]
        }

    return{
        "current_query":decision,
        "status":f"Techinal research needed. Searching for: {decision}",
        "plan":["Intent: Technical", f"Search Term:{decision}"]
    }





