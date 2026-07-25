from app.agent.state import State
from app.services.image_bytes_generator import _hf_generate_image_bytes
from pathlib import Path
from app.config import settings
import re
import os
from datetime import datetime


def generate_and_place_images(state: State) -> dict:
    plan = state["plan"]
    md = state.get("md_with_placeholders") or state["merged_md"]
    image_specs = state.get("image_specs", []) or []

    
    # Sanitize filename: remove invalid Windows characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '', plan.blog_title)
    fileName = safe_title.lower().replace(" ","_")+".md"
    folder = Path(settings.OUTPUT_DIR) 
    output_path = folder / fileName
    if not image_specs:
        Path(output_path).write_text(md, encoding="utf-8")
        return {"final": md, "fileName": fileName, "mdFilePath": str(output_path)}
    
    images_dir = Path(settings.IMAGES_DIR)
    images_dir.mkdir(exist_ok=True)


    for spec in image_specs:
        placeholder = spec["placeholder"]
        filename = spec["filename"]
        out_path = images_dir / filename

        # generate only if needed
        if not out_path.exists():
            try:
                img_bytes = _hf_generate_image_bytes(spec["prompt"])
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
        

        rel_img_dir = os.path.relpath(settings.IMAGES_DIR, settings.OUTPUT_DIR).replace(os.sep, "/")
        img_md = f"![{spec['alt']}]({rel_img_dir}/{filename})\n*{spec['caption']}*"
        md = md.replace(placeholder, img_md)

    
    
    
    Path(settings.OUTPUT_DIR).mkdir(exist_ok=True)
    if output_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{output_path.stem}_{timestamp}{output_path.suffix}"
        output_path = output_path.with_name(new_name)
    
    output_path.write_text(md,encoding="utf-8")

    return {"final": md, "fileName": fileName, "mdFilePath": str(output_path)}
        
       

    
