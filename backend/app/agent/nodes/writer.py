from app.agent.state import  Plan, Task,EvidenceItem
from app.services.llm import get_llm
from app.agent.prompts import WRITER_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from app.services.state_service import update_graph_progress
llm = get_llm()

def writer(payload:dict)->dict:
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    thread_id = payload.get("thread_id")
    total_tasks = payload.get("total_tasks", 7)
    evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]

    if thread_id:
        update_graph_progress(
            thread_id,
            "writing",
            f"Writing section {task.id} of {total_tasks}: {task.title}"
        )
    evidence_text = "\n".join(
        f"- {e.title} | {e.url}"
        for e in evidence[:20]
    )
    bullets_text = "\n".join(f"- {b}" for b in task.bullets)
    task_context = f"""Blog title: {plan.blog_title}
Audience: {plan.audience}
Tone: {plan.tone}
Blog kind: {plan.blog_kind}
Topic: {payload['topic']}
Mode: {payload.get('mode')}
requires_research: {task.requires_research}
requires_citations: {task.requires_citations}
requires_code: {task.requires_code}
Section Title: {task.title}
Section Type: {task.section_type}
recency_days={payload.get('recency_days')})
Goal: {task.goal}
Evidence (ONLY cite these URLs):\n{evidence_text}
Target words: {task.target_words}
Requires code: {task.requires_code}

Bullets:
{bullets_text}"""

    section_content = llm.invoke(
        [
            SystemMessage(content=WRITER_PROMPT),
            HumanMessage(
                content=task_context)
        ]
    ).content
    return {"sections": [(task.id, section_content)]}


    
    