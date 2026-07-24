from pathlib import Path 
from app.agent.state import State

def reducer(state:State) -> dict:
    title = state["title"]
    ordered_sections = [md for _, md in sorted(state["sections"], key=lambda x: x[0])]

    body = "\n\n".join(ordered_sections).strip()

    finalMd = f"# {title}\n\n{body}\n\n"

    # ---- Save to File ---- 
    fileName = title.lower().replace(" ","_")+".md"
    folder = Path("output") 
    output_path = folder / fileName
    folder.mkdir(exist_ok=True)
    if output_path.exists():
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{output_path.stem}_{timestamp}{output_path.suffix}"
        output_path = output_path.with_name(new_name)
    
    output_path.write_text(finalMd,encoding="utf-8")
    
    return {
        "final": finalMd
    }