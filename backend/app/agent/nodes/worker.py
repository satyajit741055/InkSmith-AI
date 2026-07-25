from app.agent.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import worker_prompt
from app.agent.state import EvidenceItem, Task, Plan


def worker(payload:dict)->dict:
    task = Task(**payload["task"])
    plan = Plan(**payload["plan"])
    evidence = [EvidenceItem(**e) for e in payload.get("evidence", [])]
    topic = payload["topic"]
    mode = payload.get("mode", "closed_book")

    bullets_text = "\n- " + "\n- ".join(task.bullets)    
    evidence_text = ""
    if evidence:
        evidence_text = "\n".join(
            f"- {e.title} | {e.url} | {e.published_at or 'date:unknown'}".strip()
            for e in evidence[:20]
        )


    prompt = worker_prompt(plan, task, topic, bullets_text, mode, evidence_text)


    section_content = llm.invoke(
        [
            SystemMessage(prompt.system),
            HumanMessage(prompt.human)
        ]
    ).content
   
    return {"sections": [(task.id, section_content)]}
    
