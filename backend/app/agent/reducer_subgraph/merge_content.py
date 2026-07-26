from app.agent.state import State
import logfire

def merge_content(state:State)->dict:
    with logfire.span("Merging content"):
        title = state["title"]
        ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]

        body = "\n\n".join(ordered_sections).strip()

        finalMd = f"# {title}\n\n{body}\n\n"
        logfire.info("Content merged", title=title, section_count=len(ordered_sections), total_length=len(finalMd))

        return {"merged_md": finalMd}