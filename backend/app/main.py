from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

# Import config first so LangSmith env vars are set before any LangChain clients import
import app.config  # noqa: F401
from fastapi import FastAPI, HTTPException, Response,Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.agent.graph import build_graph
from app.config import settings
import logfire

from slowapi import Limiter, _rate_limit_exceeded_handler 
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


from celery import Celery
from celery.result import AsyncResult


celery_app = Celery(
    "query",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    result_expires=3600,          
    task_track_started=True, 
)


_rag_agent = None

def get_rag_agent():
    global _rag_agent
    if _rag_agent is None:
        _rag_agent = build_graph()
    return _rag_agent


limiter = Limiter(key_func=get_remote_address)


_logfire_base_url = settings.LOGFIRE_BASE_URL
logfire.configure(
    token=settings.LOGFIRE_TOKEN,
    advanced=logfire.AdvancedOptions(base_url=_logfire_base_url) if _logfire_base_url else None,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag_agent = get_rag_agent()
    Path(settings.OUTPUT_DIR).mkdir(exist_ok=True)
    Path(settings.IMAGES_DIR).mkdir(exist_ok=True)
    yield


app = FastAPI(title="InkSmith AI Blog Generator", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

class QueryRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    thread_id: Optional[str] = "default"

class BlogResponse(BaseModel):
    status: str
    final: str | None = None
    file_name: str | None = None
    md_url: str | None = None
    pdf_url: str | None = None
    error: str | None = None

# Serve generated files directly
app.mount("/output", StaticFiles(directory=settings.OUTPUT_DIR), name="output")
app.mount("/images", StaticFiles(directory=settings.IMAGES_DIR), name="images")


@app.get("/")
def read_root(request: Request):
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

def _make_json_serializable(obj):
    """Recursively convert Pydantic models and other objects to JSON-safe types."""
    if isinstance(obj, BaseModel):
        return _make_json_serializable(obj.model_dump())
    if isinstance(obj, dict):
        return {k: _make_json_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_make_json_serializable(v) for v in obj]
    return obj


@celery_app.task
def run_agent(initial_state:dict,config:dict):
    agent = get_rag_agent()
    result = agent.invoke(initial_state, config)
    return _make_json_serializable(result)

@app.post("/query")
@limiter.limit("5/hour")
def query(request: Request, body: QueryRequest):
    """
    Generate a blog post from the given title.
    """
    with logfire.span("🔍 /query", request_id=body.thread_id):
        initial_state = {"title": body.title}
        config = {"configurable": {"thread_id": body.thread_id}}
        
        task = run_agent.delay(initial_state, config)
        
        return {"job_id": task.id}
        
@app.get("/job_status/{job_id}",response_model=BlogResponse)
def get_job_status(job_id: str):
    task = AsyncResult(job_id, app=celery_app)

    if task.state == "PENDING":
        return BlogResponse(status="pending")

    if task.state in ("STARTED", "RETRY"):
        return BlogResponse(status="running")

    if task.state == "FAILURE":
        return BlogResponse(status="failed", error=str(task.result))

    if task.state == "SUCCESS":
        result = task.result or {}
        file_name = result.get("file_name", "")
        md_url = f"/output/{file_name}" if file_name else None
        pdf_url = f"/files/{file_name.replace('.md', '.pdf')}" if file_name else None
        return BlogResponse(
            status="success",
            final=result.get("final", ""),
            file_name=file_name,
            md_url=md_url,
            pdf_url=pdf_url,
        )

    return BlogResponse(status=task.state.lower())


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