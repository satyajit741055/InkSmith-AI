from app.agent.state import AgentState, Plan, Task
from pathlib import Path
import re
from datetime import datetime
from app.config import settings
from app.services.mdToPDF import convert_to_pdf
from app.services.state_service import update_graph_progress

def reducer(state: AgentState) -> AgentState:
    thread_id = state.get('thread_id')
    if thread_id:
        update_graph_progress(thread_id, "assembling", "Converting to PDF...")
    sections = sorted(state["sections"], key=lambda x: x[0])
    body = "\n\n".join(content for _, content in sections)
    final_content = f"# {state['plan'].blog_title}\n\n" + body
    safe_title = re.sub(r'[<>:"/\\|?*]', '', state["plan"].blog_title)

    file_path = Path(settings.OUTPUT_DIR) / f"{safe_title.replace(' ', '_').lower()}.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if file_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        file_path = file_path.with_name(new_name)
    file_path.write_text(final_content, encoding="utf-8")

    pdf_path = convert_to_pdf(str(file_path))


    state["pdf_path"] = pdf_path    
    state["final_content"] = final_content
    state["file_name"] = file_path.name
    state["file_path"] = str(file_path) 

    if thread_id:
        update_graph_progress(thread_id, "completed", "Blog generation complete!")
    
    return state


    
    

