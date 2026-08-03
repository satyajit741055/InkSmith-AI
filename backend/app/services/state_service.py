from app.database import sync_get_db
from app.models import BlogGeneration

def update_graph_progress(thread_id: str, status: str, current_step: str):
    """Update blog generation progress in database."""
    get_db = sync_get_db()
    db = next(get_db)
    blog = db.query(BlogGeneration).filter(BlogGeneration.thread_id == thread_id).first()
    try:
        if blog:
            blog.status = status
            blog.current_step = current_step
            db.commit()
        
    except Exception as e:
        print(f"Error updating graph progress: {e}")
        if blog:
            blog.status = "failed"
            blog.current_step = f"Error: {str(e)}"
            db.commit()
        raise e
    finally:
        db.close()
