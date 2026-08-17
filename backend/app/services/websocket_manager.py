"""
WebSocket connection manager for real-time blog status updates.
Handles multiple concurrent connections and broadcasts status changes.
"""
import json
import logging
from fastapi import WebSocket
from typing import Dict, List, Set

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for blog status updates."""
    
    def __init__(self):
        # Map of blog_id -> set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, blog_id: str, websocket: WebSocket):
        """Accept and register a new WebSocket connection."""
        await websocket.accept()
        
        if blog_id not in self.active_connections:
            self.active_connections[blog_id] = set()
        
        self.active_connections[blog_id].add(websocket)
        logger.info(f"WebSocket connected for blog {blog_id}. Active connections: {len(self.active_connections[blog_id])}")
    
    async def disconnect(self, blog_id: str, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if blog_id in self.active_connections:
            self.active_connections[blog_id].discard(websocket)
            
            # Clean up empty sets
            if not self.active_connections[blog_id]:
                del self.active_connections[blog_id]
            
            logger.info(f"WebSocket disconnected for blog {blog_id}")
    
    async def broadcast(self, blog_id: str, message: dict):
        """Broadcast a message to all connected clients for a blog."""
        if blog_id not in self.active_connections:
            return
        
        # Convert message to JSON
        message_json = json.dumps(message)
        
        # Send to all connected clients
        disconnected = set()
        for connection in self.active_connections[blog_id]:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                logger.error(f"Error sending message to WebSocket: {e}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            await self.disconnect(blog_id, connection)
    
    async def send_personal(self, websocket: WebSocket, message: dict):
        """Send a message to a specific client."""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
    
    def get_connection_count(self, blog_id: str) -> int:
        """Get number of active connections for a blog."""
        return len(self.active_connections.get(blog_id, set()))


# Global connection manager instance
manager = ConnectionManager()
