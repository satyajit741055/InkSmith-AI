from app.agent.state import State
from app.services.pdf_converter import convert_to_pdf


def md_to_pdf(state:State)->dict:
    mdFilePath = state["mdFilePath"]
    pdfFilePath = convert_to_pdf(mdFilePath)
    return {"pdfFilePath": pdfFilePath}
