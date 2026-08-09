from app.agent.state import AgentState,RouterDecision
from app.services.llm import llm_groq
from langchain_core.messages import SystemMessage,HumanMessage
from app.agent.prompts import ROUTER_SYSTEM

def router(state: AgentState) -> dict:
    decider = llm_groq.with_structured_output(RouterDecision)
    decision = decider.invoke(
        [
            SystemMessage(content=ROUTER_SYSTEM),
            HumanMessage(content=f"prompt: {state['user_prompt']}"),
        ]
    )

    if decision.mode == "open_book":
        recency_days = 7
    elif decision.mode == "hybrid":
        recency_days = 45
    else:
        recency_days = 3650

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
        "recency_days": recency_days,
        "topic" : decision.topic
    }