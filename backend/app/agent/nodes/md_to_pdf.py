from app.agent.state import State
from app.services.pdf_converter import convert_to_pdf
import logfire

def md_to_pdf(state:State)->dict:
    with logfire.span("Converting Markdown to PDF"):
        mdFilePath = state["mdFilePath"]
        pdfFilePath = convert_to_pdf(mdFilePath)
        logfire.info("Markdown converted to PDF", md_file_path=mdFilePath, pdf_file_path=pdfFilePath)
        return {"pdfFilePath": pdfFilePath}
