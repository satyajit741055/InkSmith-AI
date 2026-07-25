from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.agent.graph import build_graph
from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag_agent = build_graph()
    Path(settings.OUTPUT_DIR).mkdir(exist_ok=True)
    Path(settings.IMAGES_DIR).mkdir(exist_ok=True)
    yield


app = FastAPI(title="InkSmith AI Blog Generator", lifespan=lifespan)


class QueryRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    thread_id: Optional[str] = "default"

class BlogResponse(BaseModel):
    file_name: str
    md_url: str | None
    pdf_url: str | None

# Serve generated files directly
app.mount("/output", StaticFiles(directory=settings.OUTPUT_DIR), name="output")
app.mount("/images", StaticFiles(directory=settings.IMAGES_DIR), name="images")


@app.get("/")
def read_root():
    return {"message": "InkSmith AI Blog Generator"}


@app.get("/build_graph")
def get_graph_image():
    """
    Returns the Mermaid image of the agent's workflow.
    """
    try:
        png_bytes = app.state.rag_agent.get_graph().draw_mermaid_png()
        return Response(content=png_bytes, media_type="image/png")
    except Exception as e:
        return {"error": f"Could not generate graph image: {e}"}


@app.post("/query")
def query(request: QueryRequest):
    """
    Generate a blog post from the given title.
    """
    initial_state = {"title": request.title}
    config = {"configurable": {"thread_id": request.thread_id}}
    result = app.state.rag_agent.invoke(initial_state, config)

    file_name = result.get("fileName", "")
    md_url = f"/output/{file_name}" if file_name else None
    pdf_url = md_url.replace(".md", ".pdf") if md_url else None

    return BlogResponse(
        file_name=file_name,
        md_url=md_url,
        pdf_url=pdf_url,
    )

@app.get("/files/{file_path:path}")
def get_file(file_path: str):
    """
    Serve a generated file by path. Only serves files inside OUTPUT_DIR.
    """
    base_dir = Path(settings.OUTPUT_DIR).resolve()
    target = (base_dir / file_path).resolve()

    # Prevent path traversal outside OUTPUT_DIR
    if not str(target).startswith(str(base_dir)) or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(target, filename=target.name,content_disposition_type="inline")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)