from app.agent.state import State,Plan
from app.agent.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage

def orchestrator(state:State)->dict:
    plan = llm.with_structured_output(Plan).invoke(
        [
            SystemMessage("Create a blog plan with 5-7 sections on the following topic."),
            HumanMessage(f'Topic: {state["title"]}')
        ]
    )
    return {"plan":plan}
