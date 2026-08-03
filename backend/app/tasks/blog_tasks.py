from app.celery_app import celery_app
from app.database import sync_get_db
from app.models import BlogGeneration
from app.agent.graph import graph

def run_blog_generation(user_prompt: str, blog_id: int) -> str:
    config = {"configurable": {"thread_id": f"{blog_id}"}}
    result = graph.invoke({"user_prompt": user_prompt}, config)
    return result 

@celery_app.task(name="generate_blog_task", bind=True)
def generate_blog_task(self, id: str):
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
        db.rollback()
        blog.status = "failed"
        blog.error_message = str(e)
        db.commit()
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise
    finally:
        db.close()
