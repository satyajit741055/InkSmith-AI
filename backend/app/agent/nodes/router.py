from app.agent.llm import llm
from app.agent.state import State,RouterDecision
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import routerPrompt


def router(state:State):
    topic  = state["title"]
    decision = llm.with_structured_output(RouterDecision).invoke(
        [
            SystemMessage(content=routerPrompt()),
            HumanMessage(f"Topic : {topic}")
        ]
    )

    return {
        "needs_research": decision.needs_research,
        "mode": decision.mode,
        "queries": decision.queries,
    }