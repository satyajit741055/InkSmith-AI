from app.agent.state import State,EvidencePack
from app.services.tavily_search import tavily_search
from langchain_core.messages import SystemMessage,HumanMessage
from app.agent.prompts import research_system_prompt
from app.agent.llm import llm

def researcher(state:State)->dict:
    queries = (state.get("queries", []) or [])
    max_results = 6

    raw_results : list[dict] = []

    for q in queries:
        raw_results.extend(tavily_search(q,max_results=max_results))

    if not raw_results:
        return {"evidence": []}
    
    # Return raw results directly without LLM processing for now
    # Convert to EvidenceItem format
    evidence = []
    for r in raw_results:
        evidence.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("snippet", "")[:200] + "..." if len(r.get("snippet", "")) > 200 else r.get("snippet", ""),
            "published_at": r.get("published_at") or "",
            "source": r.get("source") or ""
        })
    
    return {"evidence": evidence}

