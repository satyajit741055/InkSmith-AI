from app.database import sync_session_local
from app.models import BlogGeneration
import asyncio
import logging

logger = logging.getLogger(__name__)


def update_graph_progress(thread_id: str, status: str, current_step: str):
    """
    Update blog generation progress in database and broadcast via WebSocket.
    
    This is called from sync Celery tasks, so we use asyncio.run() to broadcast.
    """
    with sync_session_local() as db:
        blog = db.query(BlogGeneration).filter(BlogGeneration.thread_id == thread_id).first()
        try:
            if blog:
                blog.status = status
                blog.current_step = current_step
                db.commit()
                
                # ✅ Broadcast update via WebSocket
                _broadcast_status_update(thread_id, status, current_step)
        except Exception as e:
            logger.error(f"Error updating graph progress: {e}")
            if blog:
                blog.status = "failed"
                blog.current_step = f"Error: {str(e)}"
                db.commit()
            raise e


def _broadcast_status_update(thread_id: str, status: str, current_step: str):
    """Broadcast status update to all connected WebSocket clients."""
    try:
        # Import here to avoid circular imports
        from app.services.websocket_manager import manager
        
        message = {
            "thread_id": thread_id,
            "status": status,
            "current_step": current_step,
        }
        
        # Run async broadcast in sync context
        asyncio.run(manager.broadcast(thread_id, message))
    except Exception as e:
        logger.error(f"Error broadcasting WebSocket update: {e}")
        # Don't raise - we don't want WebSocket errors to break blog generation