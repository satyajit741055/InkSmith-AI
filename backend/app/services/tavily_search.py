from langchain_tavily import TavilySearch
from app.config import settings


def tavily_search(query:str,max_results:int=5)-> list[dict]:
    tool = TavilySearch(max_results=max_results, tavily_api_key=settings.TAVILY_API_KEY)
    results = tool.invoke({"query": query})
    
    # Access the actual search results from the 'results' key
    search_results = results.get('results', [])
    
    # Normalize the results
    normalized: List[dict] = []
    for r in search_results or []:
        normalized.append(
            {
                "title": r.get("title") or "",
                "url": r.get("url") or "",
                "snippet": r.get("content") or r.get("snippet") or "",
                "published_at": r.get("published_date") or r.get("published_at"),
                "source": r.get("source"),
            }
        )
    return normalized


    
