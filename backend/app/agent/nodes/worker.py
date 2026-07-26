from app.agent.llm import llm
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.prompts import worker_prompt
from app.agent.state import EvidenceItem, Task, Plan
import logfire


def worker(payload:dict)->dict:
    with logfire.span("worker", task_id=payload["task"]["id"], task_title=payload["task"]["title"]):
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


        try:
            section_content = llm.invoke(
                [
                    SystemMessage(prompt.system),
                    HumanMessage(prompt.human)
                ]
            ).content
        except Exception as e:
            logfire.error("Worker LLM call failed", task_id=task.id, task_title=task.title, error=str(e))
            raise

        logfire.info("Section written", task_id=task.id, title=task.title, word_count=len(section_content.split()))
        return {"sections": [(task.id, section_content)]}
        
