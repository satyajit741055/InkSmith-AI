from markdown_pdf import MarkdownPdf, Section


def convert_to_pdf(path:str):
    with open(path, "r", encoding="utf-8") as f:
        md = f.read()
    
    pdf = MarkdownPdf()
    pdf.add_section(Section(md))
    pdf.save(path.replace(".md", ".pdf"))

    return path.replace(".md", ".pdf")


convert_to_pdf(r"F:\GenAiProjects\InkSmith-AI\backend\output\understanding_the_hare_krishna_movement_principles_and_practices.md")