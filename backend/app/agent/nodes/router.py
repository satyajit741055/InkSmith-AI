from app.agent.llm import llm
from app.agent.state import State,RouterDecision
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import router_prompt
import logfire


def router(state:State):
    with logfire.span("Router Started"):
        topic  = state["title"]
        decision = llm.with_structured_output(RouterDecision).invoke(
            [
                SystemMessage(content=router_prompt()),
                HumanMessage(f"Topic : {topic}")
            ]
        )
        logfire.info("Router decision", decision=decision)
        return {
            "needs_research": decision.needs_research,
            "mode": decision.mode,
            "queries": decision.queries,
        }