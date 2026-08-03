from app.agent.state import AgentState, Plan
from app.agent.prompts import ORCHESTRATOR_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm import llm_groq
from langchain_core.runnables import RunnableConfig

from app.services.state_service import update_graph_progress



def orchestrator(state: AgentState) -> AgentState:
    user_prompt = state['user_prompt']
    thread_id = state.get('thread_id')

    if thread_id:
        update_graph_progress(thread_id=thread_id, status="planning", current_step="Generating outline...")

    response = llm_groq.with_structured_output(Plan).invoke(
        [
            SystemMessage(content=ORCHESTRATOR_PROMPT),
            HumanMessage(content=user_prompt),
        ]
    )
    
    if thread_id:
        update_graph_progress(thread_id=thread_id, status="planning", current_step="Outline complete")

    return {
        "plan": response,
        "thread_id": thread_id  # Persist thread_id through the state
    }


