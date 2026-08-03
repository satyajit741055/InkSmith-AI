from app.agent.state import AgentState, Plan, Task
from app.services.llm import llm_groq
from app.agent.prompts import WRITER_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.state_service import update_graph_progress


def writer(payload:dict)->dict:
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    thread_id = payload.get("thread_id")
    total_tasks = payload.get("total_tasks", 7)


    if thread_id:
        update_graph_progress(
            thread_id,
            "writing",
            f"Writing section {task.id} of {total_tasks}: {task.title}"
        )
    
    bullets_text = "\n".join(f"- {b}" for b in task.bullets)
    task_context = f"""Blog title: {plan.blog_title}
Audience: {plan.audience}
Tone: {plan.tone}
Blog kind: {plan.blog_kind}

Section Title: {task.title}
Section Type: {task.section_type}
Goal: {task.goal}
Target words: {task.target_words}
Requires code: {task.requires_code}

Bullets:
{bullets_text}"""

    section_content = llm_groq.invoke(
        [
            SystemMessage(content=WRITER_PROMPT),
            HumanMessage(
                content=task_context)
        ]
    ).content
    return {"sections": [(task.id, section_content)]}


    
    