from app.agent.state import AgentState, Plan
from app.agent.prompts import ORCHESTRATOR_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.llm import get_llm
from langchain_core.runnables import RunnableConfig

from app.services.state_service import update_graph_progress

llm = get_llm()

def orchestrator(state: AgentState) -> AgentState:
    user_prompt = state['user_prompt']
    thread_id = state.get('thread_id')
    evidences = state.get('evidence', [])

    if thread_id:
        update_graph_progress(thread_id=thread_id, status="planning", current_step="Generating outline...")

    # Format evidence nicely for the LLM
    evidence_text = ""
    if evidences:
        evidence_text = "\n\nAvailable Research Evidence:\n"
        for i, e in enumerate(evidences, 1):
            evidence_text += f"{i}. {e.title}\n   URL: {e.url}\n"
    else:
        evidence_text = "\n\n(No research evidence available - use general knowledge)"

    response = llm.with_structured_output(Plan).invoke(
        [
            SystemMessage(content=ORCHESTRATOR_PROMPT),
            HumanMessage(content=f"{user_prompt}{evidence_text}"),
        ]
    )
    
    if thread_id:
        update_graph_progress(thread_id=thread_id, status="planning", current_step="Outline complete")

    return {
        "plan": response,
        "thread_id": thread_id,  # Persist thread_id through the state
        "evidence": evidences
    }


