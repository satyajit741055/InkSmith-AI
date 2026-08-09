from app.agent.state import AgentState
def merge_content(state: AgentState) -> dict:
    plan = state["plan"]
    
    ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]
    body = "\n\n".join(ordered_sections).strip()
    merged_md = f"# {plan.blog_title}\n\n{body}\n"
    return {"merged_md": merged_md}
