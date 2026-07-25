from app.agent.state import State


def merge_content(state:State)->dict:

    title = state["title"]
    ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]

    body = "\n\n".join(ordered_sections).strip()

    finalMd = f"# {title}\n\n{body}\n\n"

    return {"merged_md": finalMd}