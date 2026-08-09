import re
import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageChops
from markdown_pdf import MarkdownPdf, Section


def autocrop_whitespace(im: Image.Image, bg_tolerance: int = 235, pad: int = 12, label: str = "") -> Image.Image:
    """Trim uniform white/near-white borders around the actual content.

    bg_tolerance: pixel value (0-255) above which a pixel is considered
    "background". Lower = more aggressive cropping. Pure white = 255.
    """
    rgb = im.convert("RGB")
    # a pixel counts as "content" if any channel drops meaningfully below white
    gray = rgb.convert("L")
    # threshold: anything darker than bg_tolerance is content
    mask = gray.point(lambda p: 255 if p < bg_tolerance else 0)
    bbox = mask.getbbox()

    # if label:
    #     print(f"[{label}] original size={im.size} bbox={bbox}")

    if not bbox:
        return im  # nothing found darker than tolerance -> leave as-is
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(im.width, right + pad)
    bottom = min(im.height, bottom + pad)
    cropped = im.crop((left, top, right, bottom))

    # if label:
    #     print(f"[{label}] cropped size={cropped.size}")

    return cropped


def convert_to_pdf(path: str, target_width_px: int = 450, max_width_px: int = 480):
    path = Path(path)
    md = path.read_text(encoding="utf-8")

    def replacer(match):
        alt, rel_path = match.group(1), match.group(2)
        clean_rel = rel_path.lstrip("./").replace("../", "")
        img_path = (path.parent.parent / clean_rel).resolve()
        if not img_path.exists():
            # print(f"WARNING: missing {img_path}")
            return match.group(0)

        with Image.open(img_path) as im:
            cropped = autocrop_whitespace(im, label=img_path.name)
            w, h = cropped.size

            # never scale UP past native size, and cap width so landscape
            # images can't overflow the page
            width = min(target_width_px, max_width_px, w)
            height = round(width * h / w)

            buf = BytesIO()
            cropped.convert("RGB").save(buf, format="PNG")
            data = base64.b64encode(buf.getvalue()).decode()

        return (
            f'<img src="data:image/png;base64,{data}" '
            f'width="{width}" height="{height}" '
            f'style="display:block;margin:1em auto;" alt="{alt}"/>'
        )

    md = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replacer, md)

    css = """
    em { display: block; text-align: center; margin-top: -0.5em; }
    """

    pdf = MarkdownPdf(toc_level=0)
    pdf.add_section(Section(md), user_css=css)
    out = path.with_suffix(".pdf")
    pdf.save(out)
    return out.as_posix()


if __name__ == "__main__":
    result = convert_to_pdf(r'F:\GenAiProjects\blog_test\InkSmith-AI\backend\blogs\kimi_k3_open_source_model.md')
    print(result)