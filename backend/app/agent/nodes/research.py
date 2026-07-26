from app.agent.state import State,EvidencePack
from app.services.tavily_search import tavily_search
from langchain_core.messages import SystemMessage,HumanMessage
from app.agent.prompts import research_system_prompt
from app.agent.llm import llm
import logfire

def researcher(state:State)->dict:
    queries = (state.get("queries", []) or [])
    max_results = 6

    raw_results : list[dict] = []
    with logfire.span("Tavily Search Started"):
        for q in queries:
            raw_results.extend(tavily_search(q,max_results=max_results))
        logfire.info("Tavily fetched results", count=len(raw_results))

    if not raw_results:
        return {"evidence": []}
    
    with logfire.span("Processing Research Results"):
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
        
        logfire.info("Research completed", evidence_count=len(evidence))
        return {"evidence": evidence}

