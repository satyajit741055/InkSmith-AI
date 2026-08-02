from typing import Annotated
from app.services.auth_service import current_user
from app.database import get_db
from app.utils.threadId import generate_id
from app.models import BlogGeneration, User
from fastapi import APIRouter,Depends
from app.schemas import UserPrompt, BlogResponse
from app.agent.graph import graph
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from pathlib import Path


router = APIRouter()

@router.post(
    "/",
    response_model=BlogResponse
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
    
    config = {"configurable": {"thread_id": thread_id}}
    try:
        result = graph.invoke({"user_prompt": prompt_text}, config=config)
        pdf_path = result["pdf_path"]
        final_content = result["final_content"]
        
        new_entry.status = "completed"
        new_entry.pdf_path = pdf_path
        new_entry.content = final_content
        await db.commit()
        await db.refresh(new_entry)
    except Exception as e:
        new_entry.status = "failed"
        new_entry.error_message = str(e)
        await db.commit()

        print(f"Error generating blog: {e}")
        raise HTTPException(status_code=500, detail="Blog generation failed")
    
    
    
    return BlogResponse(pdf_url=f"/blogs/{Path(pdf_path).name}")