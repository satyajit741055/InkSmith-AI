from langchain_tavily import TavilySearch
from app.config import settings
def _tavily_search(query: str, max_results: int = 5) -> list[dict]:
    
    try:
          
        tool = TavilySearch(max_results=max_results)
        results = tool.invoke({"query": query})
        out: list[dict] = []
        for r in results or []:
            out.append(
                {
                    "title": r.get("title") or "",
                    "url": r.get("url") or "",
                    "content": r.get("content") or r.get("snippet") or "",
                }
            )
        return out
    except Exception:
        return []