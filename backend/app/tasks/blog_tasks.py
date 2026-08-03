from app.celery_app import celery_app
from app.database import sync_get_db
from app.models import BlogGeneration
from app.agent.graph import graph

def run_blog_generation(user_prompt: str, thread_id: str) -> str:
    """Run the blog generation graph and return the result."""
    config = {"configurable": {"thread_id": thread_id}}
    result = graph.invoke({"user_prompt": user_prompt, "thread_id": thread_id}, config)
    return result

@celery_app.task(name="generate_blog_task", bind=True)
def generate_blog_task(self, id: str):
    """
    Generate a blog post asynchronously.
    
    Errors are logged to the database with status="failed", not retried.
    This allows the user to see what went wrong via the API.
    """
    db_gen = sync_get_db() 
    db = next(db_gen)
    blog = db.query(BlogGeneration).filter(BlogGeneration.thread_id == id).first()
    if not blog:
        raise ValueError("Blog not found")

    try:
        blog.status = "processing"
        db.commit()

        content = run_blog_generation(blog.prompt, id)
        pdf_path = content["pdf_path"]
        final_content = content["final_content"]
        
        blog.status = "completed"
        blog.content = final_content
        blog.pdf_path = pdf_path
        db.commit()
        
    except Exception as e:
        # Graceful failure: persist error to DB instead of crashing Celery
        db.rollback()
        blog.status = "failed"
        blog.error_message = str(e)
        db.commit()
        print(f"Blog generation failed for thread_id={id}: {type(e).__name__}: {e}")
        # Don't raise - Celery will mark this task as SUCCESS
        # The error is persisted in the DB for the user to see via GET /api/v1/blog/{id}
        
    finally:
        db.close()
