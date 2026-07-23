from app.agent.state import State,Plan
from app.agent.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import orchestrator_prompt




def orchestrator(state:State)->dict:
    prompt = orchestrator_prompt(state["title"])
    plan = llm.with_structured_output(Plan).invoke(
        [
            SystemMessage(prompt.system),
            HumanMessage(prompt.human)
        ]
    )
    return {"plan":plan}
