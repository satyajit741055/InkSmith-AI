from app.agent.state import State
from app.services.pdf_converter import convert_to_pdf
import logfire

def md_to_pdf(state:State)->dict:
    with logfire.span("Converting Markdown to PDF"):
        md_file_path = state["md_file_path"]
        pdf_file_path = convert_to_pdf(md_file_path)
        logfire.info("Markdown converted to PDF", md_file_path=md_file_path, pdf_file_path=pdf_file_path)
        return {"pdf_file_path": pdf_file_path}
