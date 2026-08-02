from app.agent.state import AgentState, Plan
from app.agent.prompts import ORCHESTRATOR_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm import llm_groq


def orchestrator(state: AgentState) -> AgentState:
    user_prompt = state['user_prompt']

    response = llm_groq.with_structured_output(Plan).invoke(
        [
            SystemMessage(content=ORCHESTRATOR_PROMPT),
            HumanMessage(content=user_prompt),
        ]
    )
    return {
        "plan": response
    }


