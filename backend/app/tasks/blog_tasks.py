from app.celery_app import celery_app
from app.database import sync_get_db, sync_session_local
from app.models import BlogGeneration
from app.agent.graph import get_graph
from app.services.storage import storage
from sqlalchemy import update



def run_blog_generation(thread_id: str,
                        user_prompt: str | None = None, 
                        is_retry: bool = False) -> str:
    """Run the blog generation graph and return the result."""
    config = {"configurable": {"thread_id": thread_id}}
    _agent = get_graph()

    if is_retry:
        snapshot = _agent.get_state(config)
        if snapshot and snapshot.values:
            result = _agent.invoke(None, config)
        else:
            result = _agent.invoke({"user_prompt": user_prompt, "thread_id": thread_id}, config)
    else:
        result = _agent.invoke(
            {"user_prompt": user_prompt, "thread_id": thread_id}, config
        )
    return result

@celery_app.task(name="generate_blog_task", bind=True)
def generate_blog_task(self, thread_id: str, is_retry: bool = False):
    """
    Generate a blog post asynchronously with idempotency guarantees.
    
    Uses optimistic locking to ensure the task only runs once even if:
    - Redis delivers the message twice (network partition)
    - Celery worker crashes and retries
    - Multiple workers pick up the same task
    
    Errors are logged to the database with status="failed", not retried.
    This allows the user to see what went wrong via the API.
    """
    with sync_session_local() as db:
        blog = db.query(BlogGeneration).filter(BlogGeneration.thread_id == thread_id).first()
        if not blog:
            raise ValueError("Blog not found")

        # Only update status to "processing" if currently "pending"
        # If another process already changed it, this returns 0 rows updated
        if not is_retry:
            stmt = (
                update(BlogGeneration)
                .where(BlogGeneration.thread_id == thread_id)
                .where(BlogGeneration.status == "pending")  # Only if pending!
                .values(status="processing")
            )
            result = db.execute(stmt)
            db.commit()

            if result.rowcount == 0:
                print(f"Blog {thread_id} already being processed or completed, skipping duplicate task")
                db.close()
                return

        try:
            # Fetch fresh state after status update
            blog = db.query(BlogGeneration).filter(BlogGeneration.thread_id == thread_id).first()
            
            content = run_blog_generation(thread_id=thread_id, user_prompt=blog.prompt, is_retry=is_retry)
            pdf_path = content["pdf_path"]
            final_content = content["final_content"]
            
            
            stmt = (
                update(BlogGeneration)
                .where(BlogGeneration.thread_id == thread_id)
                .values(
                    status="completed",
                    content=final_content,
                    pdf_path=storage.save(pdf_path)
                )
            )
            db.execute(stmt)
            db.commit()
            print(f"Blog {thread_id} generation completed successfully")
            
        except Exception as e:
            db.rollback()
            stmt = (
                update(BlogGeneration)
                .where(BlogGeneration.thread_id == thread_id)
                .values(
                    status="failed",
                    error_message=str(e)
                )
            )
            db.execute(stmt)
            db.commit()
            print(f"Blog generation failed for thread_id={thread_id}: {type(e).__name__}: {e}")
            # Don't raise - Celery will mark this task as SUCCESS
            # The error is persisted in the DB for the user to see via GET /api/v1/blog/{id}
            
        finally:
            db.close()
