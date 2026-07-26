from app.agent.state import State,Plan
from app.agent.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import orchestrator_prompt
import logfire



def orchestrator(state:State)->dict:
    
    with logfire.span("Orchestrator"):
        prompt = orchestrator_prompt(state["title"])
        evidence = state.get("evidence", [])
        mode = state.get("mode", "closed_book")

        plan = llm.with_structured_output(Plan).invoke(
            [
                SystemMessage(prompt.system),
                HumanMessage(content= (f"Topic: {state['title']}\n"
                        f"Mode: {mode}\n\n"
                        f"Evidence (ONLY use for fresh claims; may be empty):\n"
                        f"{evidence[:16]}"))
            ]
        )
        logfire.info("Orchestrator plan generated", plan=plan)
        return {"plan":plan}
