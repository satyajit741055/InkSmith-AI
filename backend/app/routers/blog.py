from typing import Annotated
from app.services.auth_service import current_user
from app.database import get_db
from app.utils.threadId import generate_id
from app.models import BlogGeneration, User
from app.tasks.blog_tasks import generate_blog_task
from fastapi import APIRouter,Depends
from app.schemas import UserPrompt, BlogGenerationId, BlogGenerationResponse
from app.agent.graph import graph
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from pathlib import Path


router = APIRouter()

@router.post(
    "/",
    response_model=BlogGenerationId
)
async def generate_blog(
    prompt:UserPrompt,
    current_user:current_user,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    prompt_text = prompt.prompt
    user_id = current_user.id
    thread_id = generate_id()
    
    new_entry = BlogGeneration(
        user_id=user_id,
        thread_id=thread_id,
        prompt=prompt_text,
    )
    
    db.add(new_entry)
    await db.commit()
    await db.refresh(new_entry)
    
    generate_blog_task.delay(thread_id)
    return BlogGenerationId(thread_id=thread_id)


@router.get("/{blog_id}", response_model=BlogGenerationResponse)
async def get_blog_status(
    blog_id: str,
    current_user: current_user,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    result = await db.execute(select(BlogGeneration).where(BlogGeneration.thread_id == blog_id))

    entry = result.scalar_one_or_none()
    if not entry or entry.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Not found")
    return BlogGenerationResponse(
        thread_id=entry.thread_id,
        status=entry.status,
        pdf_url=f"/blogs/{Path(entry.pdf_path).name}" if entry.pdf_path else None,
        error_message=entry.error_message if entry.status == "failed" else None,
    )