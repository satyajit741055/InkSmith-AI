from fastapi import APIRouter
from app.schemas import UserPrompt, BlogResponse
from app.agent.graph import graph

router = APIRouter()

@router.post(
    "/blog",
    response_model=BlogResponse
)
def generate_blog(prompt:UserPrompt):
    prompt_text = prompt.prompt
    config = {"configurable": {"thread_id": "1"}}
    result = graph.invoke({"user_prompt": prompt_text}, config=config)
    return BlogResponse(pdf_url=result["pdf_path"])