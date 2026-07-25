from app.agent.state import State
from app.services.image_bytes_generator import _hf_generate_image_bytes
from pathlib import Path


def generate_and_place_images(state: State) -> dict:
    plan = state["plan"]
    assert plan is not None

    md = state.get("md_with_placeholders") or state["merged_md"]
    image_specs = state.get("image_specs", []) or []

    print(image_specs)

    if not image_specs:
        filename = f"{plan.blog_title}.md"
        Path(filename).write_text(md, encoding="utf-8")
        return {"final": md}
    
    images_dir = Path("images")
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
        

        img_md = f"![{spec['alt']}](../images/{filename})\n*{spec['caption']}*"
        md = md.replace(placeholder, img_md)
        test_file  = "test.md"
        Path(test_file).write_text(md, encoding="utf-8")


    
    import re
    # Sanitize filename: remove invalid Windows characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '', plan.blog_title)
    fileName = safe_title.lower().replace(" ","_")+".md"
    folder = Path("output") 
    output_path = folder / fileName
    folder.mkdir(exist_ok=True)
    if output_path.exists():
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{output_path.stem}_{timestamp}{output_path.suffix}"
        output_path = output_path.with_name(new_name)
    
    output_path.write_text(md,encoding="utf-8")

    print("fileName : ",fileName)

    return {"final": md}
        
       

    
