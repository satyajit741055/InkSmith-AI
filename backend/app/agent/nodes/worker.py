from app.agent.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import worker_prompt

def worker(payload:dict)->dict:
    task = payload["task"]
    topic = payload["topic"]
    plan = payload["plan"]

    bullets_text = "\n- " + "\n- ".join(task.bullets)
    

    blog_title = plan.blog_title
    prompt = worker_prompt(plan, task, topic,bullets_text)


    section_content = llm.invoke(
        [
            SystemMessage(prompt.system),
            HumanMessage(prompt.human)
        ]
    ).content
   
    return {"sections": [section_content]}
    
