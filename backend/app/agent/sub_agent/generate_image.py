from app.agent.state import AgentState
from pathlib import Path,PurePosixPath
from app.services.generate_images import _generate_hf_image_bytes,_generate_openai_image_bytes
from app.config import settings
import re
from datetime import datetime
from app.services.mdToPDF import convert_to_pdf
from app.services.state_service import update_graph_progress


def generate_and_place_images(state: AgentState) -> dict:
    thread_id = state.get('thread_id')
    if thread_id:
        update_graph_progress(thread_id, "generating_images", "Generating images with AI...")

    plan = state["plan"]
    assert plan is not None

    md = state.get("md_with_placeholders") or state["merged_md"]
    image_specs = state.get("image_specs", []) or []

    # If no images requested, just write merged markdown
    if not image_specs:
        filename = f"{state["topic"]}.md"
        Path(filename).write_text(md, encoding="utf-8")
        return {"final": md}

    images_dir = Path("images2")
    images_dir.mkdir(exist_ok=True)

    for spec in image_specs:
        placeholder = spec["placeholder"]
        filename = PurePosixPath(spec["filename"]).name
        out_path = images_dir / filename

        # generate only if needed
        if not out_path.exists():
            try:
                img_bytes = _generate_openai_image_bytes(prompt=spec["prompt"],quality=spec["quality"],size=spec["size"])
                out_path.write_bytes(img_bytes)
            except Exception as e:
                # graceful fallback: keep doc usable
                prompt_block = (
                    f"> **[IMAGE GENERATION FAILED]** {spec.get('caption','')}\n>\n"
                    f"> **Alt:** {spec.get('alt','')}\n>\n"
                    f"> **Prompt:** {spec.get('prompt','')}\n>\n"
                    f"> **Error:** {e}\n"
                )
                md = md.replace(placeholder, prompt_block)
                continue

        img_md = f"![{spec['alt']}](../images2/{filename})\n*{spec['caption']}*"
        md = md.replace(placeholder, img_md)

    safe_title = re.sub(r'[<>:"/\\|?*]', '', state["topic"])
    file_path = Path(settings.OUTPUT_DIR) / f"{safe_title.replace(' ', '_').lower()}.md"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if file_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            file_path = file_path.with_name(new_name)
    file_path.write_text(md, encoding="utf-8")
    
    pdf_path = convert_to_pdf(str(file_path))
    
    
    state["pdf_path"] = pdf_path    
    state["final_content"] = md
    state["file_name"] = file_path.name
    state["file_path"] = str(file_path)

    if thread_id:
        update_graph_progress(thread_id, "completed", "Blog generation complete!")

    return state