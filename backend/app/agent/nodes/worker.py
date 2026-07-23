from app.agent.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage


def worker(payload:dict)->dict:
    task = payload["task"]
    topic = payload["topic"]
    plan = payload["plan"]
    

    blog_title = plan.blog_title

    section_content = llm.invoke(
        [
            SystemMessage(content="Write one Clean Markedown Section"),
            HumanMessage(content=
                f"Blog: {blog_title}\n\n"
                f"topic: {topic}\n\n"
                f"section: {task.title}\n\n"
                f"Breif: {task.brief}\n\n"
                "return only the section conent in markdown format")
        ]
    ).content
   
    return {"sections": [section_content]}
    
