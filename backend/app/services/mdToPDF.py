
from markdown_pdf import MarkdownPdf, Section
from pathlib import Path


def convert_to_pdf(path:str):
    with open(path, "r", encoding="utf-8") as f:
        md = f.read()
    
    pdf = MarkdownPdf()
    pdf.add_section(Section(md))
    # pdf.save(path.replace(".md", ".pdf"))
    pdf.save(Path(path).with_suffix(".pdf"))

    return Path(path).with_suffix(".pdf").as_posix()