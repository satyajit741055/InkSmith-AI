
from app.agent.state import AgentState,EvidencePack
from app.services.llm import get_llm
from langchain_core.messages import SystemMessage,HumanMessage
from app.agent.prompts import RESEARCH_SYSTEM
from app.services.search_tool import _tavily_search
from app.services.state_service import update_graph_progress

def research(state: AgentState) -> dict:
    llm = get_llm()
    thread_id = state.get('thread_id')
    if thread_id:
        update_graph_progress(thread_id, "researching", "Searching the web for sources...")

    queries = (state.get("queries") or [])[:10]
    raw: list[dict] = [] 
    for q in queries:
        raw.extend(_tavily_search(q, max_results=6))

    if not raw:
        return {"evidence": []}

    extractor = llm.with_structured_output(EvidencePack)
    pack = extractor.invoke(
        [
            SystemMessage(content=RESEARCH_SYSTEM),
            HumanMessage(
                content=(
                    f"Recency days: {state['recency_days']}\n\n"
                    f"Raw results:\n{raw}"
                )
            ),
        ]
    )

    dedup = {}
    for e in pack.evidence:
        if e.url:
            dedup[e.url] = e
    evidence = list(dedup.values())

    return {"evidence": evidence}