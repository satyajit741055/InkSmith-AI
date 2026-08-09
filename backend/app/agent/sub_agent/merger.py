from app.agent.state import AgentState
from app.services.state_service import update_graph_progress

def merge_content(state: AgentState) -> dict:
    thread_id = state.get('thread_id')
    if thread_id:
        update_graph_progress(thread_id, "merging", "Combining all sections...")

    plan = state["plan"]
    
    ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]
    body = "\n\n".join(ordered_sections).strip()
    merged_md = f"# {plan.blog_title}\n\n{body}\n"
    return {"merged_md": merged_md}
